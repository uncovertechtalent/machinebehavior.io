#!/usr/bin/env python3
"""Battery cells for the 122B arms through llama.cpp's server. probe.py, baseline.py and refusal_check.py run unchanged
(sha256 as in code.sha256); only their `call` function is replaced by a call to the llama.cpp server.
Rendering check 2026-11-22 (Qwen3.5-9B, Ollama against this build): the request must carry chat_template_kwargs enable_thinking false
(prompt token counts then equal Ollama's: 36, 44, 119); `--reasoning-budget 0` alone renders 2 tokens fewer.
Sampler: Ollama's effective defaults, repeat penalty off (checked on the 9B), top_k 40, top_p 0.9, min_p 0 (documented defaults).
usage: llama_battery.py TAG stance|benign|baseline|all"""
import json, os, runpy, sys, time, urllib.request
D = os.path.expanduser("~/b122"); sys.path.insert(0, D)
import probe, baseline
URL = "http://127.0.0.1:8099/v1/chat/completions"
SAMPLER = {"top_k": 40, "top_p": 0.9, "min_p": 0.0, "repeat_penalty": 1.0}
TAG = sys.argv[1]; WHAT = sys.argv[2]
SIDE = open(f"{D}/calls_{TAG}.jsonl", "a"); CELL = {"name": None}
def _post(messages, temp, max_tokens):
    body = {"messages": messages, "temperature": temp, "max_tokens": max_tokens, "seed": -1, "stream": False,
            "chat_template_kwargs": {"enable_thinking": False}, **SAMPLER}
    t0 = time.time()
    r = json.loads(urllib.request.urlopen(urllib.request.Request(URL, json.dumps(body).encode(), {"Content-Type": "application/json"}), timeout=3600).read())
    dt = time.time() - t0; ch = r["choices"][0]; m = ch["message"]; tm = r.get("timings", {})
    SIDE.write(json.dumps({"cell": CELL["name"], "prompt_tokens": r["usage"]["prompt_tokens"], "gen_tokens": r["usage"]["completion_tokens"], "finish": ch.get("finish_reason"),
                           "decode_tps": round(tm.get("predicted_per_second", 0), 2), "prefill_tps": round(tm.get("prompt_per_second", 0), 1), "sec": round(dt, 1),
                           "reasoning_len": len(m.get("reasoning_content") or "")}) + "\n"); SIDE.flush()
    return (m.get("content") or ""), (m.get("reasoning_content") or ""), dt
def call_probe(model, messages, temp): return _post(messages, temp, 600)          # probe.py: num_predict 600
def call_base(model, prompt, temp): return _post([{"role": "user", "content": prompt}], temp, 200)[0]   # baseline.py: num_predict 200, no system prompt
probe.call = call_probe; baseline.call = call_base
def stance():
    CELL["name"] = "stance_B"; sys.argv = ["probe.py", "--model", TAG, "--sys", "neutral", "--axis", "B", "--n", os.environ.get("BATTERY_N", "5"), "--temp", "0.3", "--out", f"{D}/results/{TAG}_neutral_B.jsonl"]; probe.run()
def benign():
    CELL["name"] = "benign"; sys.argv = ["refusal_check.py", TAG, f"{D}/results/{TAG}_refusal_check.jsonl"]; runpy.run_path(f"{D}/refusal_check.py", run_name="__main__")
def base():
    CELL["name"] = "baseline"; sys.argv = ["baseline.py", "--model", TAG, "--n", "3", "--out", f"{D}/results/{TAG}_baseline.jsonl"]; baseline.main()
os.makedirs(f"{D}/results", exist_ok=True)
for name, fn in (("stance", stance), ("benign", benign), ("baseline", base)):
    if WHAT in (name, "all"):
        t0 = time.time(); print(f"{time.strftime('%H:%M:%S')} START {TAG} {name}", flush=True); fn()
        print(f"{time.strftime('%H:%M:%S')} END {TAG} {name} {round(time.time()-t0)}s", flush=True)
