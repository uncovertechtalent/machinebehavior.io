#!/usr/bin/env python3
"""Exemplar-seeding evaluation (experiment 02).

Same prose-normalized regime pipeline as halflife2.py, but every session is
split at the SessionStart exemplar-seed install boundary:
    2026-08-07T18:28+02:00 = 2026-08-07T16:28:00Z
A session's arm is decided by its first assistant turn (t0):
    pre-install  = control    (no seed resident)
    post-install = treatment  (two corrected-output exemplar pairs at start)

Pre-registered prediction (2026-08-07, replication post redd.it/1vi586n):
    post-install cold-start per-10K-prose falls from ~2.89 toward 0.42;
    mid-session holds flat pre/post (drift check).
Pre-registered outcomes: a drop supports the momentum mechanism, no change
weakens it at this dose, a rise indicts bad-example leakage from the BAD halves.

Reproduce: python3 scripts/exemplar.py
Data: ~/.claude/vestige-scan.log (catches) + ~/.claude/projects/*/*.jsonl (prose).
"""
import json, re, glob, os
from datetime import datetime, timezone, timedelta

HOME = os.path.expanduser("~")
LOG = f"{HOME}/.claude/vestige-scan.log"
CUTOFF = datetime(2026, 7, 4, tzinfo=timezone.utc)
INSTALL = datetime(2026, 8, 7, 16, 28, 0, tzinfo=timezone.utc)
GAP = timedelta(hours=4)
WINDOW = timedelta(minutes=60)

def ts_parse(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

# ---- catches from the stop-hook log ----
catches, cur = [], None
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
            chars = sum(len(i.get("text") or "") for i in content
                        if isinstance(i, dict) and i.get("type") == "text") \
                    if isinstance(content, list) else 0
            turns.append((ts_parse(t), chars))
    turns.sort()
    return turns, sorted(compacts)

def blank():
    return {r: {"prose": 0, "turns": 0, "catches": 0} for r in
            ("cold-start", "mid-session", "post-resume", "post-compaction")}
arms = {"pre-install": blank(), "post-install": blank()}
sess_count = {"pre-install": 0, "post-install": 0}
mapped = {"pre-install": 0, "post-install": 0}

files = [p for p in glob.glob(f"{HOME}/.claude/projects/*/*.jsonl")
         if datetime.fromtimestamp(os.path.getmtime(p), tz=timezone.utc) >= CUTOFF]
for path in files:
    sid = os.path.basename(path)[:-6]
    turns, compacts = load(path)
    if not turns:
        continue
    t0 = turns[0][0]
    if t0 < CUTOFF:
        continue
    arm = "pre-install" if t0 < INSTALL else "post-install"
    stats = arms[arm]
    sess_count[arm] += 1
    regimes, resume_until, prev = [], None, None
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
    for c in catch_by_sid.get(sid, []):
        best = None
        for ts, chars, r in regimes:
            if ts <= c["ts"]:
                best = r
            else:
                break
        best = best or regimes[0][2]
        stats[best]["catches"] += c["w"]
        mapped[arm] += c["w"]

def rate(s):
    return s["catches"] / (s["prose"] / 10000) if s["prose"] else 0
for arm in ("pre-install", "post-install"):
    print(f"\n=== {arm}  (sessions={sess_count[arm]}, weighted catches mapped={mapped[arm]}) ===")
    print(f"{'regime':<16}{'catches':>8}{'turns':>7}{'prose kchars':>13}{'per turn':>10}{'per 10K':>9}")
    for r, s in arms[arm].items():
        pt = s["catches"] / s["turns"] if s["turns"] else 0
        print(f"{r:<16}{s['catches']:>8}{s['turns']:>7}{s['prose']/1000:>13.0f}{pt:>10.4f}{rate(s):>9.3f}")
print("\n--- headline ---")
print(f"cold-start  pre {rate(arms['pre-install']['cold-start']):.3f}  post "
      f"{rate(arms['post-install']['cold-start']):.3f}  per 10K   (control ~2.89, predicted toward 0.42)")
print(f"mid-session pre {rate(arms['pre-install']['mid-session']):.3f}  post "
      f"{rate(arms['post-install']['mid-session']):.3f}  per 10K   (drift check, want flat)")
