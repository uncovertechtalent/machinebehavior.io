#!/usr/bin/env python3
"""Resumable .161 pilot runner: llama3.1:8b, raw /api/generate, one prompt per call, temperature 0.
Skips ids already present in the output file, so it can be relaunched under a 10-minute cap until complete."""
import json, urllib.request, time, os, sys
API="http://192.168.1.161:11434/api/generate"; MODEL="llama3.1:8b"
BUDGET=float(sys.argv[1]) if len(sys.argv)>1 else 540  # seconds, stop cleanly before the cap
skill=open("/Users/stefancoetzee/code/vestige-kit/skills/output-filter/SKILL.md").read()
prompts=[json.loads(l) for l in open("bench/prompts-v1.jsonl") if l.strip()]
t0=time.time()
for cond,system in (("bare",None),("instr",skill)):
    path=f"bench/pilot/out/l31-{cond}.jsonl"
    done=set()
    if os.path.exists(path):
        for l in open(path):
            try: done.add(json.loads(l)["id"])
            except Exception: pass
    with open(path,"a") as out:
        for p in prompts:
            if p["id"] in done: continue
            if time.time()-t0>BUDGET: print(f"budget reached; {cond} at {len(done)}/48", flush=True); sys.exit(0)
            body={"model":MODEL,"prompt":p["prompt"],"stream":False,"options":{"temperature":0,"num_predict":600}}
            if system: body["system"]=system
            try:
                r=urllib.request.urlopen(urllib.request.Request(API,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"}),timeout=240)
                resp=json.load(r)["response"]
            except Exception as e:
                resp=f"__ERROR__ {type(e).__name__}: {e}"
            out.write(json.dumps({"id":p["id"],"category":p["category"],"cond":cond,"model":MODEL,"temperature":0,"response":resp},ensure_ascii=False)+"\n"); out.flush(); done.add(p["id"])
    print(f"{cond}: complete {len(done)}/48", flush=True)
print("ALL DONE .161 pilot")
