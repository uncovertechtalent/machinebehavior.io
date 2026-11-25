import json, collections, random
lab = json.load(open("labels_unblinded.json"))
recs = [json.loads(l) for l in open("results.jsonl")]
turns = {}
import importlib.util
spec = importlib.util.spec_from_file_location("h", "heldout.py"); h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
for p in h.PROBES: turns[p["id"]] = p["turns"][-1]
by = collections.defaultdict(lambda: {"hold": [], "fold": []})
for bid, k in lab.items():
    if not k["arm"].startswith("q9huihui"): continue
    if k["label"] not in ("hold", "fold"): continue
    r = recs[k["line"]]
    by[r["probe"]][k["label"]].append(r["answer"])
random.seed(7)
pos, neg = [], []
def flat(t): return " ".join(t.split())[:600]
for probe, d in sorted(by.items()):
    n = min(len(d["hold"]), len(d["fold"]))
    random.shuffle(d["hold"]); random.shuffle(d["fold"])
    for i in range(n):
        u = flat(turns[probe])
        pos.append(f"User: {u} Assistant: {flat(d['hold'][i])}")
        neg.append(f"User: {u} Assistant: {flat(d['fold'][i])}")
    print(probe, "holds", len(d["hold"]), "folds", len(d["fold"]), "pairs", n)
open("cv_positive.txt", "w").write("\n".join(pos) + "\n")
open("cv_negative.txt", "w").write("\n".join(neg) + "\n")
print("pairs total", len(pos))
