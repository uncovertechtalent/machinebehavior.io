#!/usr/bin/env python3
"""Exemplar-seeding eval v2. Fixes the control-contamination bug the reviewer caught.

v1 assigned each session to an arm by its first turn (t0). A session that started
before install but ran for days then donated its later mid-session turns to the
"pre-install" arm, so the control drifted as long-lived sessions accumulated. That
is why pre-install mid-session read 0.83 here but 0.42 on experiment 01 (frozen
2026-08-07).

v2 partitions by each TURN's own timestamp vs the install boundary. A session that
spans install contributes its pre-install turns to the control and its post-install
turns to the treatment. Control is frozen at the install date.

Also: per-pattern cold-start breakdown, to test the priming hypothesis directly
(priming predicts the rise is carried by em-dash, the seeded pattern).
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

# ---- catches, now keeping per-pattern weights ----
catches, cur = [], None
for line in open(LOG):
    m = re.match(r"^(2026\S+)\s+session=(\S+)", line)
    if m:
        cur = {"ts": ts_parse(m.group(1)), "sid": m.group(2), "w": 0, "pat": {}}
        catches.append(cur)
    elif cur is not None:
        pm = re.match(r"\s+([a-z-]+) x(\d+)", line)
        if pm:
            cur["w"] += int(pm.group(2))
            cur["pat"][pm.group(1)] = cur["pat"].get(pm.group(1), 0) + int(pm.group(2))
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
arms = {"pre": blank(), "post": blank()}
# per-pattern cold-start catches by arm
cs_pat = {"pre": {}, "post": {}}
sess_all = set()

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
    sess_all.add(sid)
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
    # prose/turns by TURN timestamp arm
    for ts, chars, r in regimes:
        arm = "pre" if ts < INSTALL else "post"
        arms[arm][r]["prose"] += chars
        arms[arm][r]["turns"] += 1
    # catches: regime of last turn at-or-before catch; arm by catch ts
    for c in catch_by_sid.get(sid, []):
        best = None
        for ts, chars, r in regimes:
            if ts <= c["ts"]:
                best = r
            else:
                break
        best = best or regimes[0][2]
        arm = "pre" if c["ts"] < INSTALL else "post"
        arms[arm][best]["catches"] += c["w"]
        if best == "cold-start":
            for p, w in c["pat"].items():
                cs_pat[arm][p] = cs_pat[arm].get(p, 0) + w

def rate(s):
    return s["catches"] / (s["prose"] / 10000) if s["prose"] else 0
print(f"sessions: {len(sess_all)}  (turn-level arm split at {INSTALL.isoformat()})")
for arm in ("pre", "post"):
    print(f"\n=== {arm}-install ===")
    print(f"{'regime':<16}{'catches':>8}{'turns':>7}{'prose k':>9}{'per10K':>8}")
    for r, s in arms[arm].items():
        print(f"{r:<16}{s['catches']:>8}{s['turns']:>7}{s['prose']/1000:>9.0f}{rate(s):>8.3f}")
cs_pre, cs_post = arms["pre"]["cold-start"], arms["post"]["cold-start"]
print("\n--- cold-start headline ---")
print(f"pre  {rate(cs_pre):.3f}   post {rate(cs_post):.3f}   per 10K")
print(f"mid  pre {rate(arms['pre']['mid-session']):.3f}  post {rate(arms['post']['mid-session']):.3f}  (control should ~match exp01 0.42)")
# Poisson 95% CI on post cold-start rate
import math
n = cs_post["catches"]; denom = cs_post["prose"]/10000
if denom:
    lo = (n - 1.96*math.sqrt(n))/denom; hi = (n + 1.96*math.sqrt(n))/denom
    print(f"post cold-start 95% CI (Poisson on {n} counts): {lo:.2f} to {hi:.2f} per 10K")
print("\n--- cold-start per-pattern (priming test: em-dash should carry the rise) ---")
pk_pre = cs_pre["prose"]/10000; pk_post = cs_post["prose"]/10000
allp = sorted(set(cs_pat["pre"]) | set(cs_pat["post"]))
print(f"{'pattern':<26}{'pre/10K':>9}{'post/10K':>10}")
for p in allp:
    rp = cs_pat['pre'].get(p,0)/pk_pre if pk_pre else 0
    rq = cs_pat['post'].get(p,0)/pk_post if pk_post else 0
    print(f"{p:<26}{rp:>9.3f}{rq:>10.3f}")
