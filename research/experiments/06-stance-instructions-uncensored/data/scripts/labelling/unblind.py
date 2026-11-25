import csv, json, collections
key = json.load(open("blind_key.json"))
A = {r["bid"]: r["label"] for r in csv.DictReader(open("labels_blind.csv"))}
B = {r["bid"]: r["label"] for r in csv.DictReader(open("labels_main40.csv"))}
print("labelled", len(A), "keyed", len(key))
pairs = [(A[b], B[b]) for b in B]
agree = sum(a == b for a, b in pairs); n = len(pairs)
cats = sorted(set(A.values()) | set(B.values()))
pa = agree / n
pe = sum((sum(a == c for a, _ in pairs) / n) * (sum(b == c for _, b in pairs) / n) for c in cats)
print(f"agreement {agree}/{n} = {pa:.2f}, kappa {(pa - pe) / (1 - pe):.2f}")
print("disagreements:", [(b, "sub=" + A[b], "main=" + B[b], key[b]["probe"][:2]) for b in B if A[b] != B[b]])
T = collections.defaultdict(collections.Counter)
P = collections.defaultdict(collections.Counter)
for b, lab in A.items():
    k = key[b]; T[k["arm"]][lab] += 1; P[(k["arm"], k["probe"][:2])][lab] += 1
order = ["neutral", "goodchad", "harness-v0", "harness-fixed"]
for m in ("q9huihui", "g4abl", "g4stock"):
    for c in order:
        t = T[f"{m}-{c}"]
        print(f"{m:9} {c:14} fold {t['fold']:2} hedge {t['hedge']:2} hold {t['hold']:2}")
print()
for m in ("q9huihui", "g4abl", "g4stock"):
    for c in order:
        cells = []
        for p in ("H1", "H2", "H3", "H4", "H5", "H6"):
            x = P[(f"{m}-{c}", p)]
            cells.append(f"{p}:{x['fold']}/{x['hedge']}")
        print(f"{m:9} {c:14} " + " ".join(cells))
json.dump({b: {**key[b], "label": A[b]} for b in A}, open("labels_unblinded.json", "w"), indent=0)
