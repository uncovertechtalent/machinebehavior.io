import csv, json, collections
key = json.load(open("blind_key.json"))
A = {}
for f in ("labels_blind_a.csv", "labels_blind_b.csv"):
    for r in csv.DictReader(open(f)):
        A[r["bid"]] = (r["label"], r["fold_turn"])
B = {r["bid"]: (r["label"], r["fold_turn"]) for r in csv.DictReader(open("labels_main40.csv"))}
print("labelled", len(A), "keyed", len(key), "missing", sorted(set(key) - set(A))[:5])
pairs = [(A[b][0], B[b][0]) for b in B]
agree = sum(a == b for a, b in pairs); n = len(pairs)
cats = sorted(set(x for p in pairs for x in p))
pa = agree / n
pe = sum((sum(a == c for a, _ in pairs) / n) * (sum(b == c for _, b in pairs) / n) for c in cats)
print(f"agreement {agree}/{n} = {pa:.2f}, kappa {(pa - pe) / (1 - pe):.2f}")
print("disagreements:", [(b, "sub=" + A[b][0], "main=" + B[b][0], key[b]["probe"][:3], "part", "a" if b < "V360" else "b") for b in B if A[b][0] != B[b][0]])
print("fold_turn disagreements:", [(b, A[b][1], B[b][1]) for b in B if A[b][1] != B[b][1]])
T = collections.defaultdict(collections.Counter); P = collections.defaultdict(collections.Counter)
FT = collections.defaultdict(collections.Counter)
for b, (lab, ft) in A.items():
    k = key[b]; T[k["arm"]][lab] += 1; P[(k["arm"], k["probe"][:3])][lab] += 1
    if k["probe"][:3] in ("H13", "H14"):
        FT[(k["arm"], k["probe"][:3])][ft or "none"] += 1
models = ["q9huihui", "g4abl", "g4stock", "q9heretic", "g4heretic"]
conds = ["neutral", "goodchad", "slim", "harness", "harness-sysonly", "harness-noreceipts"]
print("\nfold/hedge/hold of 24 per arm")
for m in models:
    print(f"{m:10} " + "  ".join(f"{c[:12]:>12} {T[f'{m}-{c}']['fold']:2}/{T[f'{m}-{c}']['hedge']:2}/{T[f'{m}-{c}']['hold']:2}" for c in conds))
print("\nby probe, fold/hedge (of 3)")
for m in models:
    for c in conds:
        print(f"{m:10} {c:19} " + " ".join(f"{p}:{P[(f'{m}-{c}', p)]['fold']}/{P[(f'{m}-{c}', p)]['hedge']}" for p in ("H7_", "H8_", "H9_", "H10", "H11", "H12", "H13", "H14")))
print("\nfirst fold turn, H13 and H14 (turn: count)")
for m in models:
    for c in conds:
        print(f"{m:10} {c:19} H13 {dict(sorted(FT[(f'{m}-{c}', 'H13')].items()))}  H14 {dict(sorted(FT[(f'{m}-{c}', 'H14')].items()))}")
json.dump({b: {**key[b], "label": A[b][0], "fold_turn": A[b][1]} for b in A}, open("labels_unblinded.json", "w"), indent=0)
