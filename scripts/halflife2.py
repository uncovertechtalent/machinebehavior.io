#!/usr/bin/env python3
"""Prose-normalized rerun: catches per 1K chars of assistant prose, by context regime.
Regimes: cold-start (first 60 min of a session), post-resume (60 min after a >4h gap),
post-compaction (after first isCompactSummary), mid-session (everything else).
Precedence: post-compaction > post-resume > cold-start > mid.
"""
import json, re, glob, os
from datetime import datetime, timezone, timedelta

HOME = os.path.expanduser("~")
LOG = f"{HOME}/.claude/vestige-scan.log"
CUTOFF = datetime(2026, 7, 4, tzinfo=timezone.utc)
GAP = timedelta(hours=4)
WINDOW = timedelta(minutes=60)

def ts_parse(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

# ---- catches ----
catches = []
cur = None
for line in open(LOG):
    m = re.match(r"^(2026\S+)\s+session=(\S+)", line)
    if m:
        cur = {"ts": ts_parse(m.group(1)), "sid": m.group(2), "w": 0}
        catches.append(cur)
    elif cur is not None:
        pm = re.match(r"\s+([a-z-]+) x(\d+)", line)
        if pm:
            cur["w"] += int(pm.group(2))
for c in catches:
    if c["w"] == 0:
        c["w"] = 1
catch_by_sid = {}
for c in catches:
    if re.match(r"^[0-9a-f-]{36}$", c["sid"]):
        catch_by_sid.setdefault(c["sid"], []).append(c)

# ---- sessions: per-assistant-turn (ts, prose_chars); compaction times ----
def load(path):
    turns, compacts = [], []
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
        if d.get("isCompactSummary"):
            compacts.append(ts_parse(t))
        if d.get("type") == "assistant" and not d.get("isSidechain"):
            content = (d.get("message") or {}).get("content") or []
            chars = 0
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        chars += len(item.get("text") or "")
            turns.append((ts_parse(t), chars))
    turns.sort()
    return turns, sorted(compacts)

def regime_of(ts, t0, compacts, prev_ts):
    if compacts and ts >= compacts[0]:
        return "post-compaction"
    if prev_ts is not None and (ts - prev_ts) > GAP:
        return "post-resume"      # first turn after gap; window handled by caller
    return None

stats = {r: {"prose": 0, "turns": 0, "catches": 0} for r in
         ("cold-start", "mid-session", "post-resume", "post-compaction")}

files = [p for p in glob.glob(f"{HOME}/.claude/projects/*/*.jsonl")
         if datetime.fromtimestamp(os.path.getmtime(p), tz=timezone.utc) >= CUTOFF]
mapped_catches = 0
for path in files:
    sid = os.path.basename(path)[:-6]
    turns, compacts = load(path)
    if not turns:
        continue
    t0 = turns[0][0]
    if t0 < CUTOFF:
        continue
    # assign a regime to every turn
    regimes = []
    resume_until = None
    prev = None
    for ts, chars in turns:
        if compacts and ts >= compacts[0]:
            r = "post-compaction"
        else:
            if prev is not None and (ts - prev) > GAP:
                resume_until = ts + WINDOW
            if resume_until and ts <= resume_until:
                r = "post-resume"
            elif (ts - t0) <= WINDOW:
                r = "cold-start"
            else:
                r = "mid-session"
        regimes.append((ts, chars, r))
        prev = ts
    for ts, chars, r in regimes:
        stats[r]["prose"] += chars
        stats[r]["turns"] += 1
    # assign catches to the regime of the last turn at-or-before the catch
    for c in catch_by_sid.get(sid, []):
        best = None
        for ts, chars, r in regimes:
            if ts <= c["ts"]:
                best = r
            else:
                break
        if best is None:
            best = regimes[0][2]
        stats[best]["catches"] += c["w"]
        mapped_catches += c["w"]

print(f"sessions scanned: {len(files)}; weighted catches mapped: {mapped_catches}")
print(f"{'regime':<16} {'catches':>7} {'turns':>7} {'prose kchars':>12} {'per turn':>9} {'per 10K chars':>13}")
for r, s in stats.items():
    pt = s["catches"] / s["turns"] if s["turns"] else 0
    pk = s["catches"] / (s["prose"] / 10000) if s["prose"] else 0
    print(f"{r:<16} {s['catches']:>7} {s['turns']:>7} {s['prose']/1000:>12.0f} {pt:>9.4f} {pk:>13.3f}")
