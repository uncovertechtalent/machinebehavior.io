import json, random, re, ast
src = open("heldout2.py").read()
probes = ast.literal_eval(re.search(r"^PROBES = (\[.*?^\])", src, re.S | re.M).group(1))
turns = {p["id"]: p["turns"] for p in probes}
recs = [json.loads(l) for l in open("results.jsonl")]
random.Random(20261124).shuffle(recs)
key = {}
with open("blind.jsonl", "w") as fh:
    for i, r in enumerate(recs):
        bid = f"V{i:03d}"
        key[bid] = {"arm": r["arm"], "model": r["model"], "rep": r["rep"], "probe": r["probe"]}
        ta = r.get("turn_answers") or [r["answer"]]
        fh.write(json.dumps({"bid": bid, "probe": r["probe"], "kind": r["kind"], "truth": r["truth"],
                             "user_turns": turns[r["probe"]], "assistant_turns": ta,
                             "finish": r["finish"]}) + "\n")
json.dump(key, open("blind_key.json", "w"), indent=0)
ids = sorted(key); half = len(ids) // 2
open("part_a.txt", "w").write("\n".join(ids[:half])); open("part_b.txt", "w").write("\n".join(ids[half:]))
s = random.Random(40).sample(ids, 40); open("sample40.txt", "w").write("\n".join(sorted(s)))
print(len(recs), "blinded;", sum(len(json.loads(l)["assistant_turns"]) for l in open("blind.jsonl")), "assistant turns")
