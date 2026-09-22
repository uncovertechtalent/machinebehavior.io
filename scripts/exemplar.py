#!/usr/bin/env python3
"""Exemplar-seeding eval, v4: scored by EVENT (one per blocked turn), weighted shown for reference.

History of this script, kept because the register keeps its corrections:
  v1  arm by session start. Control contaminated by long-lived sessions.
  v2  arm by each turn's own timestamp. Fixed the control. Still weighted.
  v3  added per-model join. Attributed the 'rise' to model version. Wrong.
  v4  THIS. The stop-hook log records a weight per blocked turn ('em-dash x25' = 25).
      Summing weights lets one bulk-text turn (a quoted passage, a pasted draft) count
      as 25 relapses. 13 turns with weight >= 10 carried 40% of all weight, and two
      sessions carried the whole post-install 'rise'. Scored by event, the arm is flat:
      the pre-registered 'no change at this dose' outcome. Every mechanism attribution
      from v1 to v3 (priming, period confound, model version) was explaining an artifact.

Reproduce: python3 scripts/exemplar.py
Data: ~/.claude/vestige-scan.log (blocked turns) + ~/.claude/projects/*/*.jsonl (prose).
"""
import json, re, glob, os, math
from datetime import datetime, timezone, timedelta

HOME = os.path.expanduser("~")
LOG = f"{HOME}/.claude/vestige-scan.log"
CUTOFF = datetime(2026, 7, 4, tzinfo=timezone.utc)
INSTALL = datetime(2026, 8, 7, 16, 28, 0, tzinfo=timezone.utc)
GAP = timedelta(hours=4)
WINDOW = timedelta(minutes=60)

def ts_parse(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

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
    c["w"] = c["w"] or 1
catch_by_sid = {}
for c in catches:
    if re.match(r"^[0-9a-f-]{36}$", c["sid"]):
        catch_by_sid.setdefault(c["sid"], []).append(c)

ws = [c["w"] for c in catches]
bulk = [w for w in ws if w >= 10]
print(f"blocked turns: {len(ws)}   weighted sum: {sum(ws)}   "
      f"turns with weight>=10: {len(bulk)} carrying {sum(bulk)/sum(ws):.0%} of weight")

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

REG = ("cold-start", "mid-session", "post-resume", "post-compaction")
def blank():
    return {r: {"prose": 0, "ev": 0, "w": 0} for r in REG}
arms = {"pre": blank(), "post": blank()}

for path in glob.glob(f"{HOME}/.claude/projects/*/*.jsonl"):
    if datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc) < CUTOFF:
        continue
    turns, compacts = load(path)
    if not turns:
        continue
    t0 = turns[0][0]
    if t0 < CUTOFF:
        continue
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
        arms["pre" if ts < INSTALL else "post"][r]["prose"] += chars
    for c in catch_by_sid.get(os.path.basename(path)[:-6], []):
        best = None
        for ts, chars, r in regimes:
            if ts <= c["ts"]:
                best = r
            else:
                break
        best = best or regimes[0][2]
        a = arms["pre" if c["ts"] < INSTALL else "post"][best]
        a["ev"] += 1
        a["w"] += c["w"]

def rate(n, prose):
    return n / (prose / 10000) if prose else 0
def ci(n, prose):
    k = prose / 10000
    return (max(0, n - 1.96 * math.sqrt(n)) / k, (n + 1.96 * math.sqrt(n)) / k) if k else (0, 0)

print(f"\n{'regime':<16}{'arm':<6}{'prose k':>8}{'events':>8}{'ev/10K':>8}{'  95% CI':>14}{'weighted/10K':>14}")
for r in REG[:3]:
    for arm in ("pre", "post"):
        s = arms[arm][r]
        if s["prose"] < 10000:
            continue
        lo, hi = ci(s["ev"], s["prose"])
        print(f"{r:<16}{arm:<6}{s['prose']/1000:>8.0f}{s['ev']:>8}{rate(s['ev'], s['prose']):>8.2f}"
              f"{lo:>7.2f}-{hi:<6.2f}{rate(s['w'], s['prose']):>14.2f}")
cs = arms["pre"]["cold-start"], arms["post"]["cold-start"]
print(f"\nheadline (by event): cold-start pre {rate(cs[0]['ev'], cs[0]['prose']):.2f}  post "
      f"{rate(cs[1]['ev'], cs[1]['prose']):.2f} per 10K. Prediction was a fall toward 0.42-equivalent; "
      f"outcome is the pre-registered 'no change at this dose'.")
