#!/usr/bin/env python3
"""Experiment 06: write croissant.json (MLCommons Croissant 1.0) describing the exported data folder.

File paths are relative to croissant.json, so the folder validates and loads where it lies. Called by export.py
after the data and claims are written and before SHA256SUMS; each distribution carries the file's sha256.
"""
import hashlib, json, os

CONTEXT = {
    "@language": "en", "@vocab": "https://schema.org/", "sc": "https://schema.org/",
    "cr": "http://mlcommons.org/croissant/", "rai": "http://mlcommons.org/croissant/RAI/", "dct": "http://purl.org/dc/terms/",
    "citeAs": "cr:citeAs", "column": "cr:column", "conformsTo": "dct:conformsTo",
    "data": {"@id": "cr:data", "@type": "@json"}, "dataType": {"@id": "cr:dataType", "@type": "@vocab"},
    "examples": {"@id": "cr:examples", "@type": "@json"}, "extract": "cr:extract", "field": "cr:field",
    "fileProperty": "cr:fileProperty", "fileObject": "cr:fileObject", "fileSet": "cr:fileSet", "format": "cr:format",
    "includes": "cr:includes", "isLiveDataset": "cr:isLiveDataset", "jsonPath": "cr:jsonPath", "key": "cr:key",
    "md5": "cr:md5", "parentField": "cr:parentField", "path": "cr:path", "recordSet": "cr:recordSet",
    "references": "cr:references", "regex": "cr:regex", "repeated": "cr:repeated", "replace": "cr:replace",
    "samplingRate": "cr:samplingRate", "equivalentProperty": "cr:equivalentProperty", "separator": "cr:separator", "source": "cr:source", "subField": "cr:subField", "transform": "cr:transform",
}

PAGE = "https://machinebehavior.io/research/experiments/06-stance-instructions-uncensored/"

FILES = [
    ("records.jsonl", "application/jsonlines", "One line per model conversation: probe, model, condition, the assistant turns."),
    ("labels.jsonl", "application/jsonlines", "One blind hand label per record: fold, hedge, hold or cut_off (benign refusal checks: comply, partial, refuse or cut_off), and the turn of the first fold."),
    ("results.csv", "text/csv", "Label counts per probe set, model, condition, thinking mode, temperature and language."),
    ("comparison.csv", "text/csv", "The comparison table: label counts per run, model, condition and thinking mode (battery rows: pressure probes B1, B6, B8)."),
    ("probes.json", "application/json", "Probe definitions: the user turns and the true answer each probe pressures against."),
    ("models.json", "application/json", "Each model build: repository, commit, file sha256 and quantiser, or the hosting provider."),
    ("agreement.json", "application/json", "Every label-agreement check, recomputed from the label files: agreement count, n and Cohen's kappa."),
    ("gate.json", "application/json", "The G2 fact gate (written before any label was read) run over every battery pressure answer: flagged or not, and why."),
    ("claims.json", "application/json", "Every number the published story states, recomputed from records and labels, with the record ids behind it."),
    ("conditions/index.json", "application/json", "The instruction texts used as system prompts and per-message reminders, with sha256."),
    ("coverage.json", "application/json", "Counts per run and any known gaps in the export."),
]


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def field(rs, name, dtype, desc, fid, path=None, col=None, repeated=False, references=None):
    f = {"@type": "cr:Field", "@id": f"{rs}/{name}", "name": name, "description": desc, "dataType": dtype,
         "source": {"fileObject": {"@id": fid}, "extract": ({"jsonPath": path} if path else {"column": col or name})}}
    if repeated:
        f["repeated"] = True
    if references:
        f["references"] = {"field": {"@id": references}}
    return f


def build(out):
    dist = []
    for rel, fmt, desc in FILES:
        p = os.path.join(out, rel)
        if os.path.exists(p):
            dist.append({"@type": "cr:FileObject", "@id": rel, "name": rel, "description": desc,
                         "contentUrl": rel, "encodingFormat": fmt, "sha256": sha(p)})
    T, I, F, B = "sc:Text", "sc:Integer", "sc:Float", "sc:Boolean"
    records = {"@type": "cr:RecordSet", "@id": "records", "name": "records", "key": {"@id": "records/id"},
               "description": "Model conversations under pressure to accept a false claim.",
               "field": [
                   field("records", "id", T, "Record id: run id and a sequence number.", "records.jsonl"),
                   field("records", "run", T, "Run id (date and arm).", "records.jsonl"),
                   field("records", "probe_set", T, "battery-B, heldout-v1 or heldout-v2.", "records.jsonl"),
                   field("records", "probe", T, "Probe id; see probes.json.", "records.jsonl"),
                   field("records", "model", T, "Model build name; see models.json.", "records.jsonl"),
                   field("records", "condition", T, "Instruction condition; see conditions/index.json.", "records.jsonl"),
                   field("records", "think", T, "Reasoning mode: off, on, or forced on.", "records.jsonl"),
                   field("records", "temperature", F, "Sampling temperature.", "records.jsonl"),
                   field("records", "language", T, "Language of the probe text.", "records.jsonl"),
                   field("records", "steering", T, "Control-vector setting, for the steering sweep only (chapter 9).", "records.jsonl"),
                   field("records", "assistant_turns", T, "The model's reply to each user turn, in order, as recorded.",
                         "records.jsonl", repeated=True),
               ]}
    labels = {"@type": "cr:RecordSet", "@id": "labels", "name": "labels",
              "description": "Blind hand labels, one per record.",
              "field": [
                  field("labels", "record", T, "The labelled record.", "labels.jsonl", references="records/id"),
                  field("labels", "label", T, "fold, hedge, hold or cut_off; on the benign refusal checks comply, partial, refuse or cut_off.", "labels.jsonl"),
                  field("labels", "labeller", T, "Who labelled, and how the blind check came out.", "labels.jsonl"),
                  field("labels", "blind", B, "Whether the labeller saw model and condition.", "labels.jsonl"),
                  field("labels", "fold_turn", T, "Multi-turn probes: the turn of the first fold, if any.", "labels.jsonl"),
              ]}
    cols = [("probe_set", T), ("model", T), ("condition", T), ("think", T), ("temperature", F), ("language", T),
            ("label_source", T), ("n", I), ("fold", I), ("hedge", I), ("hold", I), ("cut_off", I), ("comply", I), ("partial", I), ("refuse", I)]
    results = {"@type": "cr:RecordSet", "@id": "results", "name": "results", "description": "Label counts per cell.",
               "field": [field("results", c, t, f"Column {c}.", "results.csv", col=c) for c, t in cols]}
    doc = {
        "@context": CONTEXT, "@type": "sc:Dataset", "conformsTo": "http://mlcommons.org/croissant/1.0",
        "name": "machinebehavior-experiment-06-stance-instructions-uncensored",
        "description": ("Conversations in which local and hosted language models, stock and with refusals removed "
                        "(abliterated or Heretic builds), are pressured by authority, mood, premise or persistence to "
                        "accept a false claim, under no instruction, short stance instructions, and a long harness. "
                        "Every record carries a blind hand label; every published number is recomputed in claims.json."),
        "url": PAGE, "license": "https://creativecommons.org/licenses/by/4.0/",
        "creator": {"@type": "sc:Organization", "name": "machinebehavior.io", "url": "https://machinebehavior.io/"},
        "citeAs": ("@misc{machinebehavior_exp06_2026, title={Stance instructions on uncensored language models (experiment 06)}, "
                   "author={{machinebehavior.io}}, year={2026}, url={" + PAGE + "}}"),
        "datePublished": "2026-11-24", "version": "0.1.0", "inLanguage": ["en"],
        "keywords": ["sycophancy", "abliteration", "refusal removal", "Heretic", "stance", "LLM evaluation"],
        "rai:dataCollection": "Model answers generated by the authors with pinned scripts and pinned model files (see models.json); hosted arms are named by provider and model id.",
        "rai:dataAnnotationProtocol": "Blind hand labels by two readers per set, a third blind check on a random 40 records, and a reconciliation pass on any probe where the readers split along a rule line, until Cohen's kappa reaches about 0.85.",
        "rai:dataLimitations": "Three to five repetitions per cell; small and mid-size models; one labelling protocol; hosted arms are not file-pinned.",
        "distribution": dist, "recordSet": [records, labels, results],
    }
    json.dump(doc, open(os.path.join(out, "croissant.json"), "w"), indent=1)
    return len(dist)
