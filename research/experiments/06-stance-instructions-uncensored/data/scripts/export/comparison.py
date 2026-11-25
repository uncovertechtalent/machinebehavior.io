#!/usr/bin/env python3
"""Experiment 06: the comparison table, generated from the export (records + labels), one row per run x model x
condition x thinking mode x probe set. Battery rows count the pressure probes B1, B6 and B8 only ("battery-pressure-15",
5 reps); held-out rows count every probe. Written to out/comparison.csv by export.py; the vault copy is regenerated
from it and never edited by hand.
"""
import collections, csv, json, os

from export import cond_label

RUN_DATE = lambda run: f"{run[1:5]}-{run[5:7]}-{run[7:9]}"


def build(out):
    recs = [json.loads(l) for l in open(os.path.join(out, "records.jsonl"))]
    labs = {l["record"]: l["label"] for l in map(json.loads, open(os.path.join(out, "labels.jsonl")))}
    T = collections.defaultdict(collections.Counter)
    for r in recs:
        if r["probe_set"] == "battery-B":
            if not r["probe"].startswith(("B1", "B6", "B8")):
                continue
            pset = "battery-pressure"
        else:
            pset = r["probe_set"]
        k = (pset, r["model"], cond_label(r), r["think"], r.get("backend") or "", r["temperature"], r["language"], r.get("with_run") or r["run"])
        T[k][labs[r["id"]]] += 1
    rows = [["probe_set", "n", "build", "condition", "think", "backend", "temperature", "language", "fold", "hedge", "hold",
             "cut_off", "run", "run_date", "comply", "partial", "refuse"]]
    for k, c in sorted(T.items(), key=lambda kv: (kv[0][0], kv[0][7], kv[0][1], kv[0][2])):
        pset, model, cond, think, backend, temp, lang, run = k
        rows.append([pset, sum(c.values()), model, cond, think, backend, temp, lang, c["fold"], c["hedge"], c["hold"],
                     c["cut_off"], run, RUN_DATE(run), c["comply"], c["partial"], c["refuse"]])
    with open(os.path.join(out, "comparison.csv"), "w", newline="") as fh:
        csv.writer(fh).writerows(rows)
    return len(rows) - 1
