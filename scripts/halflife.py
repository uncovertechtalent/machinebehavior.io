#!/usr/bin/env python3
"""Half-life experiment: vestige relapse position vs session length,
conditioned on instruction residency (compaction as the residency boundary).
Data: ~/.claude/vestige-scan.log + session transcripts in ~/.claude/projects/*/.
"""
import json, re, glob, os
from datetime import datetime, timezone

HOME = os.path.expanduser("~")
LOG = f"{HOME}/.claude/vestige-scan.log"

def ts_parse(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

# ---- 1. parse the catch log ----
catches = []  # (ts, sid, [(pattern, count)])
cur = None
for line in open(LOG):
    m = re.match(r"^(2026\S+)\s+session=(\S+)", line)
    if m:
        cur = {"ts": ts_parse(m.group(1)), "sid": m.group(2), "patterns": []}
        catches.append(cur)
    elif cur is not None:
        pm = re.match(r"\s+([a-z-]+) x(\d+)", line)
        if pm:
            cur["patterns"].append((pm.group(1), int(pm.group(2))))

real = [c for c in catches if re.match(r"^[0-9a-f-]{36}$", c["sid"])]
print(f"catch events: {len(catches)} total, {len(real)} with real session ids")

# ---- 2. index transcripts ----
def find_jsonl(sid):
    hits = glob.glob(f"{HOME}/.claude/projects/*/{sid}.jsonl")
    return hits[0] if hits else None

# ---- 3. per-session analysis ----
session_cache = {}
def load_session(sid):
    if sid in session_cache:
        return session_cache[sid]
    path = find_jsonl(sid)
    if not path:
        session_cache[sid] = None
        return None
    turns = []      # assistant turn timestamps
    compacts = []   # compaction timestamps
    for line in open(path):
        if '"timestamp"' not in line:
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        t = d.get("timestamp")
        if not t:
            continue
        if d.get("type") == "assistant" and not d.get("isSidechain"):
            turns.append(ts_parse(t))
        if d.get("isCompactSummary"):
            compacts.append(ts_parse(t))
    turns.sort()
    session_cache[sid] = {"turns": turns, "compacts": sorted(compacts)}
    return session_cache[sid]

rows = []
missing = []
for c in real:
    s = load_session(c["sid"])
    if not s or not s["turns"]:
        missing.append(c["sid"])
        continue
    t0, tN = s["turns"][0], s["turns"][-1]
    total_min = (tN - t0).total_seconds() / 60
    elapsed = (c["ts"] - t0).total_seconds() / 60
    idx = sum(1 for t in s["turns"] if t <= c["ts"])
    n = len(s["turns"])
    p = idx / n if n else 0
    post_compact = bool(s["compacts"] and c["ts"] >= s["compacts"][0])
    weight = sum(k for _, k in c["patterns"]) or 1
    rows.append({"sid": c["sid"][:8], "elapsed_min": elapsed, "total_min": total_min,
                 "turn_idx": idx, "n_turns": n, "p": p, "post_compact": post_compact,
                 "weight": weight, "patterns": c["patterns"]})

print(f"catch events mapped to transcripts: {len(rows)}; unmapped sessions: {len(set(missing))}")

# ---- 4. position distribution ----
ps = sorted(r["p"] for r in rows)
def q(v, f):
    return v[int(f * (len(v) - 1))]
if ps:
    print("\n== normalized position p = turn_idx / n_turns (uniform relapse -> mean 0.5) ==")
    print(f"n={len(ps)} mean={sum(ps)/len(ps):.3f} q25={q(ps,.25):.3f} median={q(ps,.5):.3f} q75={q(ps,.75):.3f}")
    ews = sorted(r["elapsed_min"] for r in rows)
    print(f"elapsed minutes at catch: median={q(ews,.5):.0f} q75={q(ews,.75):.0f} max={max(ews):.0f}")

# ---- 5. compaction conditioning (sessions that have catches AND compaction) ----
sids = {r["sid"] for r in rows}
pre_c = post_c = 0
pre_turns = post_turns = 0
for c in real:
    s = session_cache.get(c["sid"])
    if not s:
        continue
for sid_full in {c["sid"] for c in real}:
    s = session_cache.get(sid_full)
    if not s or not s["turns"] or not s["compacts"]:
        continue
    fc = s["compacts"][0]
    pre_turns += sum(1 for t in s["turns"] if t < fc)
    post_turns += sum(1 for t in s["turns"] if t >= fc)
    for c in real:
        if c["sid"] != sid_full:
            continue
        w = sum(k for _, k in c["patterns"]) or 1
        if c["ts"] >= fc:
            post_c += w
        else:
            pre_c += w
print("\n== compaction conditioning (only sessions with >=1 compaction and >=1 catch) ==")
print(f"pre-compaction:  {pre_c} catches over {pre_turns} assistant turns -> {pre_c/pre_turns if pre_turns else 0:.4f} per turn")
print(f"post-compaction: {post_c} catches over {post_turns} assistant turns -> {post_c/post_turns if post_turns else 0:.4f} per turn")

# ---- 6. exposure baseline: all sessions since 2026-07-04, catch rate by session-elapsed bucket ----
all_jsonl = glob.glob(f"{HOME}/.claude/projects/*/*.jsonl")
cutoff = datetime(2026, 7, 4, tzinfo=timezone.utc)
bucket_turns = {}  # bucket (30-min) -> exposure turns
for path in all_jsonl:
    if datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc) < cutoff:
        continue
    sid = os.path.basename(path)[:-6]
    s = load_session(sid)
    if not s or not s["turns"]:
        continue
    t0 = s["turns"][0]
    if t0 < cutoff:
        continue
    for t in s["turns"]:
        b = int((t - t0).total_seconds() / 60 // 30)
        bucket_turns[b] = bucket_turns.get(b, 0) + 1
bucket_catch = {}
for r in rows:
    b = int(r["elapsed_min"] // 30)
    bucket_catch[b] = bucket_catch.get(b, 0) + r["weight"]
print("\n== catch rate per assistant turn by session-age bucket (30-min buckets, all sessions since 07-04 as exposure) ==")
for b in sorted(bucket_turns):
    if bucket_turns[b] < 50:
        continue
    c = bucket_catch.get(b, 0)
    print(f"  {b*30:>4}-{b*30+30:<4} min: {c:>3} catches / {bucket_turns[b]:>5} turns = {c/bucket_turns[b]:.4f}")
