#!/usr/bin/env python3
"""SUPERSEDED 2026-09-22, kept as a receipt. This script sums the log's per-turn weights,
which inflate bulk-text turns; its '30x across models' finding rested on one catch in a
63K-char cell and was withdrawn. See scripts/exemplar.py v4 for the event-scored method.

Em-dash relapse rate by model version and regime.

The exemplar-seeding arm (scripts/exemplar.py) is confounded: the model roster
shifted across the install boundary. This script measures the confound directly.
Each assistant turn carries its model id in the transcript; each vestige-scan
catch is joined to the model of the turn it maps to. Output: em-dash catches per
10K prose chars, by (model, regime).

Finding: em-dash relapse is dominated by model version, a ~30x spread across
models, far larger than the 2.3x exemplar-arm difference. Caveat: fable-5-1 is
September-only, so its near-zero rate is confounded with era; the opus-4-8 /
opus-5 / fable-5 comparison overlaps in time and still separates by model.

Reproduce: python3 scripts/model_rate.py
"""
import json, glob, os, re
from datetime import datetime, timezone, timedelta

HOME = os.path.expanduser("~"); LOG = f"{HOME}/.claude/vestige-scan.log"
CUT = datetime(2026, 7, 4, tzinfo=timezone.utc)
GAP = timedelta(hours=4); WIN = timedelta(minutes=60)
def tp(s): return datetime.fromisoformat(s.replace("Z", "+00:00"))
def norm(m): return (m or "").split("/")[-1]

catches, cur = [], None
for line in open(LOG):
    m = re.match(r"^(2026\S+)\s+session=(\S+)", line)
    if m: cur = {"ts": tp(m.group(1)), "sid": m.group(2), "em": 0}; catches.append(cur)
    elif cur is not None:
        pm = re.match(r"\s+([a-z-]+) x(\d+)", line)
        if pm and pm.group(1) == "em-dash": cur["em"] += int(pm.group(2))
by_sid = {}
for c in catches:
    if re.match(r"^[0-9a-f-]{36}$", c["sid"]): by_sid.setdefault(c["sid"], []).append(c)

stat = {}
def add(k, pk, em):
    d = stat.setdefault(k, {"prose": 0, "em": 0}); d["prose"] += pk; d["em"] += em
for p in glob.glob(f"{HOME}/.claude/projects/*/*.jsonl"):
    if datetime.fromtimestamp(os.path.getmtime(p), tz=timezone.utc) < CUT: continue
    turns, compacts = [], []
    for line in open(p):
        if '"timestamp"' not in line: continue
        try: d = json.loads(line)
        except: continue
        t = d.get("timestamp")
        if not t: continue
        if d.get("isCompactSummary"): compacts.append(tp(t))
        if d.get("type") == "assistant" and not d.get("isSidechain"):
            msg = d.get("message") or {}; content = msg.get("content") or []
            ch = sum(len(i.get("text") or "") for i in content
                     if isinstance(i, dict) and i.get("type") == "text") if isinstance(content, list) else 0
            turns.append((tp(t), ch, norm(msg.get("model"))))
    if not turns: continue
    turns.sort(); t0 = turns[0][0]
    if t0 < CUT: continue
    compacts.sort()
    regs, ru, prev = [], None, None
    for ts, ch, mdl in turns:
        if compacts and ts >= compacts[0]: r = "post-compaction"
        else:
            if prev is not None and (ts - prev) > GAP: ru = ts + WIN
            if ru and ts <= ru: r = "post-resume"
            elif (ts - t0) <= WIN: r = "cold-start"
            else: r = "mid-session"
        regs.append((ts, ch, mdl, r)); prev = ts
    for ts, ch, mdl, r in regs: add((mdl, r), ch, 0)
    for c in by_sid.get(os.path.basename(p)[:-6], []):
        best = None
        for ts, ch, mdl, r in regs:
            if ts <= c["ts"]: best = (mdl, r)
            else: break
        best = best or (regs[0][2], regs[0][3])
        add(best, 0, c["em"])

for regime in ("cold-start", "mid-session"):
    print(f"\n=== {regime}: em-dash per 10K by model ===")
    print(f"{'model':<26}{'prose k':>9}{'em':>6}{'em/10K':>8}")
    for (mdl, r) in sorted(stat, key=lambda k: k[0]):
        if r != regime: continue
        d = stat[(mdl, r)]
        if d["prose"] < 20000: continue
        print(f"{mdl:<26}{d['prose']/1000:>9.0f}{d['em']:>6}{d['em']/(d['prose']/10000):>8.3f}")
