#!/usr/bin/env python3
"""Experiment 06 export: build the public data folder from the run folders.

usage: export.py --runs <runs> --vault <vault clone> --out <dir> [--sources sources.json]

Reads every run listed in sources.json, joins answers to their labels (blind hand labels where they exist,
the battery's automatic label otherwise, marked as such), and writes:
  records.jsonl  labels.jsonl  probes.json  conditions/  models.json  results.csv  coverage.json  SHA256SUMS
Fails (exit 2) if any output file contains a private pattern (LAN addresses, host names, home paths).
Model answers are copied as recorded; only whitelisted metadata fields are emitted.
Standard library only.
"""
import argparse, ast, collections, csv, glob, hashlib, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PRIVATE = [r"(?!)"]  # the private host and path patterns are kept off the public copy; this one never matches
TEMP_DEFAULT = 0.3


def literal(path, name):
    """A module-level literal (list/dict/str) from a Python file, without importing it."""
    tree = ast.parse(open(path).read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise KeyError(f"{name} not in {path}")


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def cond_label(r):
    """The condition column: the condition id, plus the control-vector setting for steering-sweep records."""
    s = r.get("steering")
    if not s:
        return r["condition"]
    return f"{r['condition']}, control-vector sweep baseline (no vector)" if s == "none" else f"{r['condition']} + control vector {s}"


class Export:
    def __init__(self, a, src):
        self.a, self.src = a, src
        self.records, self.labels, self.probes, self.conditions = [], [], {}, {}
        self.gaps = collections.defaultdict(list)
        self.seen_models = set()

    # ---- shared pieces -------------------------------------------------------------------------------
    def condition(self, cid, text):
        text = text.strip()
        if cid in self.conditions and self.conditions[cid] != text:
            raise SystemExit(f"condition {cid} has two different texts")
        self.conditions[cid] = text

    def add(self, run, rec, label, labeller, blind, auto_label=None, fold_turn=None):
        rid = f"{run['id']}:{len(self.records):05d}"
        rec = {"id": rid, "run": run["id"], **rec}
        self.records.append(rec)
        self.seen_models.add(rec["model"])
        self.labels.append({"record": rid, "label": label, "labeller": labeller, "blind": blind,
                            "auto_label": auto_label, "fold_turn": fold_turn or None})

    def model_of(self, tag):
        for pat, name in self.src["models"].items():
            if re.search(pat, tag):
                return name
        self.gaps["unmapped_model_tags"].append(tag)
        return tag

    # ---- battery runs (probe.py axis B) ------------------------------------------------------------------
    def battery_probes(self, run):
        path = os.path.join(self.a.runs, run["probe_py"])
        for p in literal(path, "AXIS_B"):
            turns = [p["turn1"], p["turn2"]] if p.get("two_turn") else [p["prompt"]]
            self.probes.setdefault(p["id"], {"id": p["id"], "set": "battery-B", "user_turns": turns,
                                             "truth": self.src["battery_truths"].get(p["id"])})
        self.condition("neutral", literal(path, "NEUTRAL_SYS"))
        self.condition("good-chad", literal(path, "GOODCHAD_SYS"))

    def battery(self, run):
        self.battery_probes(run)
        for cid, rel in run.get("condition_files", {}).items():
            self.condition(cid, open(os.path.join(self.a.runs, rel)).read())
        hand = {}
        if run.get("hand_csv"):
            path = os.path.join(self.a.vault, "_inbox", run["hand_csv"])
            for r in csv.DictReader(open(path)):
                hv = f"{r['model']}_{r['variant'].replace('-', '_')}" if run.get("hand_key") == "model_variant" else r["variant"]
                hand[(hv, int(r["idx"]))] = r
        else:
            self.gaps["runs_without_hand_labels"].append(run["id"])
        for f in sorted(glob.glob(os.path.join(self.a.runs, run["glob"]))):
            m = re.search(run["variant_re"], os.path.basename(f))
            if not m:
                continue
            variant = m.group(1)
            raw = m.group(2) if m.lastindex and m.lastindex > 1 else ""
            cmap = {**self.src["conditions"], **run.get("condition_map", {})}
            cond = run.get("condition") or cmap.get(raw, raw or "neutral")
            for idx, line in enumerate(open(f)):
                x = json.loads(line)
                if x.get("axis") not in (None, "B"):
                    continue
                answers = [x["first_turn"], x["answer"]] if x.get("first_turn") else [x["answer"]]
                h = hand.get((variant, idx))
                rec = {"probe": x["probe"], "probe_set": "battery-B", "model": self.model_of(variant), "model_tag": variant,
                       "condition": cond, "think": run.get("think", "off"), "temperature": run.get("temperature", TEMP_DEFAULT),
                       "rep": x.get("rep"), "language": "en", "assistant_turns": answers,
                       "backend": next((b for pat, b in run.get("backend_map", {}).items() if re.search(pat, variant)), run.get("backend"))}
                if h:
                    self.add(run, rec, h["hand_call"], "hand (main session)", False, auto_label=x.get("label"))
                else:
                    self.add(run, rec, None, None, False, auto_label=x.get("label"))

    # ---- held-out runs (heldout.py, heldout2.py, heldout3.py) --------------------------------------------
    def heldout(self, run):
        d = os.path.join(self.a.runs, run["dir"])
        for name in ("PROBES", "PROBES_DE"):
            try:
                for p in literal(os.path.join(d, run["probe_py"]), name):
                    lang = "de" if name == "PROBES_DE" else "en"
                    pid = p["id"] + ("_de" if lang == "de" else "")
                    self.probes.setdefault(pid, {"id": pid, "set": run["probe_set"], "kind": p.get("kind"),
                                                 "truth": p.get("truth"), "user_turns": p["turns"], "language": lang})
            except KeyError:
                pass
        for cid, rel in run.get("condition_files", {}).items():
            self.condition(cid, open(os.path.join(d, rel)).read())
        key_labels = json.load(open(os.path.join(d, "labels_unblinded.json")))
        by = {(v["arm"], v["probe"], int(v["rep"])): v for v in key_labels.values()}
        for line in open(os.path.join(d, "results.jsonl")):
            x = json.loads(line)
            m = re.match(run["arm_re"], x["arm"]) if run.get("arm_re") else None
            short, cond = (m.group("short"), m.group("cond")) if m else x["arm"].split("-", 1)
            rf = run.get("record_fields", False)
            lang = x.get("lang", "en") if rf else "en"
            temp = x.get("temp", run.get("temperature", TEMP_DEFAULT)) if rf else run.get("temperature", TEMP_DEFAULT)
            turns = x.get("turn_answers") or ([x["first_turn"], x["answer"]] if x.get("first_turn") else [x["answer"]])
            rec = {"probe": x["probe"] + ("_de" if lang == "de" else ""), "probe_set": run["probe_set"], "model": self.model_of(short), "model_tag": x["model"],
                   "condition": {**self.src["conditions"], **run.get("condition_map", {})}.get(cond, cond), "think": run.get("think_map", {}).get(short, "off"), "temperature": temp,
                   "rep": x["rep"], "language": lang, "assistant_turns": turns, "finish": x.get("finish"), "backend": run.get("backend_map", {}).get(short, "ollama")}
            lab = by.get((x["arm"], x["probe"], int(x["rep"])))
            if lab is None:
                self.gaps["unlabelled_records"].append(f"{run['id']} {x['arm']} {x['probe']} {x['rep']}")
                self.add(run, rec, None, None, False)
            else:
                self.add(run, rec, lab["label"], run["labeller"], True, fold_turn=lab.get("fold_turn"))
        for f in run.get("agreement_files", []):
            self.gaps.setdefault("agreement_sources", []).append(f"{run['id']}:{f}")

    # ---- control-vector sweep (cv_record.py on llama.cpp) ------------------------------------------------
    def cv(self, run):
        self.battery_probes(run)
        d = os.path.join(self.a.runs, run["dir"])
        key_labels = json.load(open(os.path.join(d, "labels_unblinded.json")))
        by = {(v["setting"], v["probe"], int(v["rep"])): v for v in key_labels.values()}
        vec_sha = {n: hashlib.sha256(open(os.path.join(d, "vectors", n), "rb").read()).hexdigest()
                   for n in sorted(os.listdir(os.path.join(d, "vectors")))}
        for line in open(os.path.join(d, "results.jsonl")):
            x = json.loads(line)
            s = run["settings"][x["setting"]]
            detail = {"setting": x["setting"], **s}
            if s.get("vector"):
                detail["vector_sha256"] = vec_sha[s["vector"]]
            answers = [x["first_turn"], x["answer"]] if x.get("first_turn") else [x["answer"]]
            rec = {"probe": x["probe"], "probe_set": "battery-B", "model": self.model_of(run["model_tag"]),
                   "model_tag": run["model_tag"], "condition": "neutral", "steering": x["setting"], "steering_detail": detail,
                   "think": "off", "temperature": run.get("temperature", TEMP_DEFAULT), "rep": x["rep"], "language": "en",
                   "assistant_turns": answers, "finish": x.get("finish"), "backend": run["backend"]}
            lab = by.get((x["setting"], x["probe"], int(x["rep"])))
            if lab is None:
                self.gaps["unlabelled_records"].append(f"{run['id']} {x['setting']} {x['probe']} {x['rep']}")
                self.add(run, rec, None, None, False)
            else:
                self.add(run, rec, lab["label"], run["labeller"], True)

    # ---- benign refusal checks (refusal_check.py and the battery's benign cell) -----------------------------
    def benign(self, run):
        """Two requests a cautious model may refuse (R1 own lock, R2 insult me), asked alongside earlier runs.
        Each source names the run it was asked with; condition, thinking, temperature and backend come from that run.
        Labels come from one blind label folder (two full reads, a main-session sample, adjudication)."""
        d = os.path.join(self.a.runs, run["dir"])
        lab = json.load(open(os.path.join(d, "labels_unblinded.json")))
        for pid, text in run["prompts"].items():
            self.probes.setdefault(pid, {"id": pid, "set": "benign", "kind": "benign", "truth": None, "user_turns": [text]})
        runs = {r["id"]: r for r in self.src["runs"]}
        for s in json.load(open(os.path.join(d, run["sources"]))):
            base = runs[s["with_run"]]
            cmap = {**self.src["conditions"], **base.get("condition_map", {})}
            for f in sorted(glob.glob(os.path.join(self.a.runs, s["glob"]))):
                rel = os.path.relpath(f, self.a.runs)
                for idx, line in enumerate(open(f)):
                    x = json.loads(line)
                    if s.get("tag_from") == "record":
                        variant, raw = s["tag_map"][x["model"]], ""
                    else:
                        m = re.search(s["variant_re"], os.path.basename(f))
                        variant = m.group(1)
                        raw = m.group(2) if m.lastindex and m.lastindex > 1 else ""
                    rec = {"probe": x["probe"], "probe_set": "benign", "model": self.model_of(variant), "model_tag": variant,
                           "condition": base.get("condition") or cmap.get(raw, raw or "neutral"), "think": base.get("think", "off"),
                           "temperature": base.get("temperature", TEMP_DEFAULT), "rep": x.get("rep"), "language": "en",
                           "assistant_turns": [x["answer"]],
                           "backend": next((b for pat, b in base.get("backend_map", {}).items() if re.search(pat, variant)), base.get("backend")),
                           "with_run": s["with_run"]}
                    l = lab.get(f"{rel}#{idx}")
                    if l is None:
                        self.gaps["unlabelled_records"].append(f"{run['id']} {rel}#{idx}")
                        self.add(run, rec, None, None, False, auto_label=x.get("label"))
                    else:
                        self.add(run, rec, l["label"], run["labeller"], True, auto_label=x.get("label"))

    # ---- later blind relabels (keyed by record id) -----------------------------------------------------
    def apply_relabels(self):
        by_id = {l["record"]: l for l in self.labels}
        for rl in self.src.get("relabels", []):
            d = os.path.join(self.a.runs, rl["dir"])
            key = json.load(open(os.path.join(d, rl["key"])))
            n = 0
            for r in csv.DictReader(open(os.path.join(d, rl["labels"]))):
                rid = key[r["bid"]]["record"]
                if rid not in by_id:
                    raise SystemExit(f"relabel {r['bid']} points at unknown record {rid}: record ids changed, rebuild the blind set")
                by_id[rid].update(label=r["label"], labeller=rl["labeller"], blind=True)
                n += 1
            self.gaps.setdefault("relabels_applied", []).append(f"{rl['dir']}: {n}")

    # ---- outputs -------------------------------------------------------------------------------------
    def results(self):
        T = collections.defaultdict(collections.Counter)
        for r, l in zip(self.records, self.labels):
            T[(r["probe_set"], r["model"], cond_label(r), r["think"], r["temperature"], r["language"],
               "hand" if l["label"] else "auto")][l["label"] or l["auto_label"] or "none"] += 1
        rows = [["probe_set", "model", "condition", "think", "temperature", "language", "label_source", "n",
                 "fold", "hedge", "hold", "cut_off", "comply", "partial", "refuse"]]
        for k, c in sorted(T.items(), key=lambda kv: tuple(str(x) for x in kv[0])):
            rows.append([*k, sum(c.values()), c["fold"], c["hedge"], c["hold"], c["cut_off"], c["comply"], c["partial"], c["refuse"]])
        return rows

    def write(self):
        o = self.a.out
        os.makedirs(os.path.join(o, "conditions"), exist_ok=True)
        with open(os.path.join(o, "records.jsonl"), "w") as fh:
            for r in self.records:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        with open(os.path.join(o, "labels.jsonl"), "w") as fh:
            for l in self.labels:
                fh.write(json.dumps(l) + "\n")
        json.dump(sorted(self.probes.values(), key=lambda p: p["id"]), open(os.path.join(o, "probes.json"), "w"), indent=1, ensure_ascii=False)
        index = {}
        for cid, text in sorted(self.conditions.items()):
            open(os.path.join(o, "conditions", f"{cid}.txt"), "w").write(text + "\n")
            index[cid] = {"file": f"conditions/{cid}.txt", "sha256": sha(text), "words": len(text.split())}
        json.dump(index, open(os.path.join(o, "conditions", "index.json"), "w"), indent=1)
        meta = self.src.get("model_meta", {})
        models = [{"name": m, **meta.get(m, {"status": "metadata missing"})} for m in sorted(self.seen_models)]
        for m in models:
            if m.get("status") == "metadata missing":
                self.gaps["models_without_pins"].append(m["name"])
        json.dump(models, open(os.path.join(o, "models.json"), "w"), indent=1)
        with open(os.path.join(o, "results.csv"), "w", newline="") as fh:
            csv.writer(fh).writerows(self.results())
        cov = {"records": len(self.records),
               "labelled_by_hand": sum(1 for l in self.labels if l["label"]),
               "auto_only": sum(1 for l in self.labels if not l["label"]),
               "by_run": collections.Counter(r["run"] for r in self.records),
               **{k: sorted(set(v)) for k, v in self.gaps.items()}}
        json.dump(cov, open(os.path.join(o, "coverage.json"), "w"), indent=1)
        return cov

    def scrub_check(self):
        hits = []
        rx = re.compile("|".join(PRIVATE))
        for root, _, files in os.walk(self.a.out):
            for f in files:
                p = os.path.join(root, f)
                for n, line in enumerate(open(p, errors="replace"), 1):
                    m = rx.search(line)
                    if m:
                        hits.append(f"{os.path.relpath(p, self.a.out)}:{n}: {m.group(0)}")
        return hits

    def checksums(self):
        lines = []
        for root, _, files in os.walk(self.a.out):
            for f in sorted(files):
                if f == "SHA256SUMS":
                    continue
                p = os.path.join(root, f)
                lines.append(f"{hashlib.sha256(open(p, 'rb').read()).hexdigest()}  {os.path.relpath(p, self.a.out)}")
        open(os.path.join(self.a.out, "SHA256SUMS"), "w").write("\n".join(sorted(lines, key=lambda l: l[66:])) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True); ap.add_argument("--vault", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--sources", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "sources.json"))
    a = ap.parse_args()
    a.runs, a.vault, a.out = (os.path.expanduser(p) for p in (a.runs, a.vault, a.out))
    src = json.load(open(a.sources))
    ex = Export(a, src)
    for run in src["runs"]:
        getattr(ex, run["kind"])(run)
    ex.apply_relabels()
    cov = ex.write()
    import agreement
    agreement.build(a.out, a.runs, src.get("agreement", []))
    import gate
    gate.build(a.out)
    spec = os.path.join(os.path.dirname(os.path.abspath(__file__)), "claims_spec.json")
    claim_fail = []
    if os.path.exists(spec):
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import claims
        claim_fail = claims.build(a.out, spec)
    import comparison
    comparison.build(a.out)
    import report
    if not claim_fail:
        report.build(a.out, os.path.dirname(os.path.abspath(__file__)))
    import croissant
    croissant.build(a.out)
    hits = ex.scrub_check()
    ex.checksums()
    print(json.dumps({k: (v if not isinstance(v, list) or len(v) < 12 else v[:12] + [f"... {len(v)} total"]) for k, v in cov.items()}, indent=1))
    if hits:
        print(f"PRIVATE PATTERN HITS: {len(hits)}", *hits[:20], sep="\n")
        sys.exit(2)
    print("scrub check: clean")
    if claim_fail:
        print(f"CLAIMS FAILING: {len(claim_fail)}", *claim_fail, sep="\n")
        sys.exit(3)
    print("claims: all hold")


if __name__ == "__main__":
    main()
