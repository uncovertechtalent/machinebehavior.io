#!/usr/bin/env python3
"""Experiment 06: run the G2 fact gate (g2_checker.py, pinned by sha256, written before any hand label was read)
over every battery pressure answer (B1, B6, B8), and the byte gate (g2_byte_checker.py) over every held-out H13 answer, and write gate.json: record id -> flagged, reasons.
Mode "guarded" (the primary G2), no post-hoc fixes. claims.py reads gate.json for the gate claims."""
import hashlib, json, os

PIN = "a1286b42866a"
PIN_BYTE = "70b438280868"


def build(out):
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "g2_checker.py")
    got = hashlib.sha256(open(src, "rb").read()).hexdigest()
    if not got.startswith(PIN):
        raise SystemExit(f"g2_checker.py sha256 {got[:12]} differs from the pin {PIN}")
    import g2_checker
    res = {}
    for line in open(os.path.join(out, "records.jsonl")):
        r = json.loads(line)
        if r["probe_set"] != "battery-B" or not r["probe"].startswith(("B1", "B6", "B8")):
            continue
        flagged, why = g2_checker.flag(r["probe"], r["assistant_turns"][-1], "guarded")
        res[r["id"]] = {"flagged": flagged, "why": why}
    # The byte-probe gate (H13), pinned separately; committed 3b50d29 before its first run (2026-11-25 09:18).
    srcb = os.path.join(here, "g2_byte_checker.py")
    gotb = hashlib.sha256(open(srcb, "rb").read()).hexdigest()
    if not gotb.startswith(PIN_BYTE):
        raise SystemExit(f"g2_byte_checker.py sha256 {gotb[:12]} differs from the pin {PIN_BYTE}")
    import g2_byte_checker
    for line in open(os.path.join(out, "records.jsonl")):
        r = json.loads(line)
        if r["probe"].startswith("H13"):
            flagged, why = g2_byte_checker.flag(r["assistant_turns"][-1])
            res[r["id"]] = {"flagged": flagged, "why": why, "checker": "g2_byte_checker.py"}
    json.dump({"checker": "g2_checker.py", "checker_sha256": got, "mode": "guarded",
               "byte_checker": "g2_byte_checker.py", "byte_checker_sha256": gotb, "results": res},
              open(os.path.join(out, "gate.json"), "w"), indent=0)
    return len(res)
