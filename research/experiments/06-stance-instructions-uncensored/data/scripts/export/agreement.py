#!/usr/bin/env python3
"""Experiment 06: recompute every label-agreement check from the label files and write agreement.json.
Each entry in sources.json "agreement": dir, a (label CSVs of reader A, merged), b (label CSVs of reader B) or
b_key_field (reader B's label taken from blind_key.json), and an optional name. Compared on the bids reader B has."""
import csv, json, os


def kappa(pairs):
    n = len(pairs); ag = sum(a == b for a, b in pairs); cats = set(x for p in pairs for x in p)
    pe = sum((sum(a == c for a, _ in pairs) / n) * (sum(b == c for _, b in pairs) / n) for c in cats)
    return ag, n, round(((ag / n) - pe) / (1 - pe), 3) if pe < 1 else 1.0


def build(out, runs, entries):
    res = []
    for e in entries:
        d = os.path.join(runs, e["dir"])
        A = {}
        for f in e["a"]:
            for r in csv.DictReader(open(os.path.join(d, f))):
                A[r["bid"]] = r["label"]
        if "b_key_field" in e:
            key = json.load(open(os.path.join(d, "blind_key.json")))
            B = {b: v[e["b_key_field"]] for b, v in key.items()}
        else:
            B = {}
            for f in e["b"]:
                for r in csv.DictReader(open(os.path.join(d, f))):
                    B[r["bid"]] = r["label"]
        pairs = [(A[b], B[b]) for b in B if b in A]
        ag, n, k = kappa(pairs)
        res.append({"name": e["name"], "agree": ag, "n": n, "kappa": k, "what": e.get("what", "")})
    json.dump(res, open(os.path.join(out, "agreement.json"), "w"), indent=1)
    return res
