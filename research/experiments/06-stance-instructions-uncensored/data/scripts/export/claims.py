#!/usr/bin/env python3
"""Experiment 06 claims: recompute every number the story states from the exported data.

claims_spec.json lists claims. Each claim has an id, a chapter, the sentence as published, a filter over the
records, a metric, and the expected value. The verifier selects the records, computes the metric, writes
claims.json (value, n, the record ids behind it, pass or fail) and fails the build when any claim does not hold.

Filter keys (all optional; a list means any of): run, probe_set, model, condition, think, temperature, language, rep, steering,
probe_prefix (matched against the start of the probe id).
Metrics:
  {"count": "fold"}                    labels equal to fold (or a list of labels)
  {"count": ["fold","hedge"]}
  {"share": "fold"}                    count / n
  {"reduction": {"from": <filter>, "to": <filter>, "label": "fold"}}   1 - to/from, on counts
  {"each": <group key>, "count": "fold"}   value per group (a dict); expected is a dict or {"all": v}
  {"fold_turn_share": "3"}             share of folded records whose first fold is at that turn
  {"gate_flagged": "fold"}             of the records with that label, how many the G2 gate flagged (n = records with the label)
Expected: a number, {"all": v} for "each", or {"min": a, "max": b} for a range; shares are compared at 3 decimals.
"""
import collections, json, os, sys

KEYS = ("run", "probe_set", "model", "condition", "think", "temperature", "language", "rep", "steering")


def load(out):
    recs = [json.loads(l) for l in open(os.path.join(out, "records.jsonl"))]
    labs = {l["record"]: l for l in map(json.loads, open(os.path.join(out, "labels.jsonl")))}
    return recs, labs


def select(recs, f):
    def ok(r):
        for k in KEYS:
            if k in f:
                want = f[k] if isinstance(f[k], list) else [f[k]]
                if r.get(k) not in want:
                    return False
        if "probe_prefix" in f:
            pre = f["probe_prefix"] if isinstance(f["probe_prefix"], list) else [f["probe_prefix"]]
            if not any(r["probe"].startswith(p) for p in pre):
                return False
        return True
    return [r for r in recs if ok(r)]


def count(rows, labs, which):
    which = which if isinstance(which, list) else [which]
    return sum(1 for r in rows if labs[r["id"]]["label"] in which)


GATE = {}


def compute(c, recs, labs):
    m = c["metric"]
    rows = select(recs, c.get("filter", {}))
    if "gate_flagged" in m:
        want = m["gate_flagged"] if isinstance(m["gate_flagged"], list) else [m["gate_flagged"]]
        pool = [r for r in rows if labs[r["id"]]["label"] in want and r["id"] in GATE]
        hit = [r for r in pool if GATE[r["id"]]["flagged"]]
        return len(hit), len(pool), pool
    if "reduction" in m:
        a = select(recs, {**c.get("filter", {}), **m["reduction"]["from"]})
        b = select(recs, {**c.get("filter", {}), **m["reduction"]["to"]})
        ca, cb = count(a, labs, m["reduction"]["label"]), count(b, labs, m["reduction"]["label"])
        return round(1 - cb / ca, 3), len(a) + len(b), a + b
    if "each" in m:
        g = collections.defaultdict(list)
        for r in rows:
            g[str(r.get(m["each"]) if m["each"] != "probe_prefix" else r["probe"][:3])].append(r)
        return {k: count(v, labs, m["count"]) for k, v in sorted(g.items())}, len(rows), rows
    if "fold_turn_share" in m:
        folded = [r for r in rows if labs[r["id"]].get("fold_turn")]
        hit = sum(1 for r in folded if str(labs[r["id"]]["fold_turn"]) == str(m["fold_turn_share"]))
        return (round(hit / len(folded), 3) if folded else None), len(folded), folded
    if "share" in m:
        return (round(count(rows, labs, m["share"]) / len(rows), 3) if rows else None), len(rows), rows
    return count(rows, labs, m["count"]), len(rows), rows


def holds(value, exp):
    if isinstance(exp, dict) and "all" in exp:
        return isinstance(value, dict) and value and all(v == exp["all"] for v in value.values())
    if isinstance(exp, dict) and ("min" in exp or "max" in exp):
        return value is not None and exp.get("min", float("-inf")) <= value <= exp.get("max", float("inf"))
    if isinstance(exp, float):
        return value is not None and abs(value - exp) < 0.0005
    return value == exp


def build(out, spec_path):
    recs, labs = load(out)
    gp = os.path.join(out, "gate.json")
    GATE.clear()
    if os.path.exists(gp):
        GATE.update(json.load(open(gp))["results"])
    spec = json.load(open(spec_path))
    results, failed = [], []
    for c in spec["claims"]:
        value, n, rows = compute(c, recs, labs)
        ok = holds(value, c["expected"])
        if c.get("min_n") and n < c["min_n"]:
            ok = False
        if "n" in c and n != c["n"]:
            ok = False
        results.append({"id": c["id"], "chapter": c["chapter"], "sentence": c["sentence"], "filter": c.get("filter", {}),
                        "metric": c["metric"], "expected": c["expected"], "value": value, "n": n, "pass": ok,
                        "records": sorted(r["id"] for r in rows)})
        if not ok:
            failed.append(f"{c['id']}: expected {c['expected']}" + (f" n={c['n']}" if "n" in c else "") + f", got {value} (n={n})")
    json.dump({"claims": results, "all_pass": not failed}, open(os.path.join(out, "claims.json"), "w"), indent=1)
    return failed


if __name__ == "__main__":
    out, spec = sys.argv[1], sys.argv[2]
    bad = build(out, spec)
    print("\n".join(bad) if bad else "all claims hold")
    sys.exit(2 if bad else 0)
