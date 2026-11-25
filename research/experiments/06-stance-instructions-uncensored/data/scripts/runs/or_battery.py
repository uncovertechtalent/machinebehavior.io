#!/usr/bin/env python3
"""Battery cells for a hosted model through OpenRouter. probe.py, baseline.py and refusal_check.py run unchanged
(sha256 prefixes 1cebc6b9, fd6d0099, ece7790b, as in the 2026-10-30, 11-18 and 11-22 runs); only their `call` is replaced.

Hosted, so no file hash: every call records the provider that answered, the model id it reports, token counts,
reasoning tokens and text length, finish reason, and cost. Provider pinned (no fallback); thinking requested off.
Settings as llama_battery.py of 2026-11-22: temperature from the scripts (0.3; baseline its own), 600 tokens
(baseline 200), sampler top_k 40, top_p 0.9, min_p 0, repetition penalty 1.0, sent but not required of the host.

usage: or_battery.py TAG MODEL PROVIDER stance|benign|baseline|all|smoke
The key is read from ~/.config/openrouter/api-key and never printed."""
import json, os, runpy, sys, time, urllib.error, urllib.request

D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import probe, baseline  # noqa: E402

URL = "https://openrouter.ai/api/v1/chat/completions"
KEY = open(os.path.expanduser("~/.config/openrouter/api-key")).read().strip()
SAMPLER = {"top_k": 40, "top_p": 0.9, "min_p": 0.0, "repetition_penalty": 1.0}
TAG, MODEL, PROVIDER, WHAT = sys.argv[1:5]
THINK = os.environ.get("THINK", "off")  # off: reasoning {"enabled": false}; low|medium|high: reasoning {"effort": ...}
# GLM-5.3 on OpenRouter refuses thinking off ("Reasoning is mandatory for this endpoint", 2026-11-22, every provider
# tried), so its arm runs with the lowest effort and a budget large enough that reasoning cannot starve the answer.
MAX_PROBE = int(os.environ.get("MAX_PROBE", "600")); MAX_BASE = int(os.environ.get("MAX_BASE", "200"))
os.makedirs(f"{D}/results", exist_ok=True)
SIDE = open(f"{D}/calls_{TAG}.jsonl", "a"); CELL = {"name": None}


def _post(messages, temp, max_tokens):
    body = {"model": MODEL, "messages": messages, "temperature": temp, "max_tokens": max_tokens, "stream": False,
            "provider": {"order": [PROVIDER], "allow_fallbacks": False},
            "reasoning": ({"enabled": False} if THINK == "off" else {"effort": THINK}), "usage": {"include": True}, **SAMPLER}
    req = urllib.request.Request(URL, json.dumps(body).encode(), {
        "Content-Type": "application/json", "Authorization": f"Bearer {KEY}",
        "X-Title": "house stance battery (hosted arm)"})
    for attempt in range(5):
        t0 = time.time()
        try:
            r = json.loads(urllib.request.urlopen(req, timeout=600).read())
            break
        except urllib.error.HTTPError as e:  # 429 and 5xx: back off and retry; others are fatal
            msg = e.read()[:300].decode(errors="replace")
            if e.code in (429, 500, 502, 503, 504) and attempt < 4:
                print(f"retry {attempt + 1} after HTTP {e.code}: {msg}", flush=True); time.sleep(10 * (attempt + 1)); continue
            raise SystemExit(f"HTTP {e.code}: {msg}")
    dt = time.time() - t0
    if "choices" not in r:
        raise SystemExit(f"no choices: {json.dumps(r)[:300]}")
    ch = r["choices"][0]; m = ch["message"]; u = r.get("usage", {})
    reasoning = m.get("reasoning") or m.get("reasoning_content") or ""
    SIDE.write(json.dumps({
        "cell": CELL["name"], "provider": r.get("provider"), "model": r.get("model"), "id": r.get("id"),
        "prompt_tokens": u.get("prompt_tokens"), "gen_tokens": u.get("completion_tokens"),
        "reasoning_tokens": (u.get("completion_tokens_details") or {}).get("reasoning_tokens"),
        "reasoning_len": len(reasoning), "finish": ch.get("finish_reason"), "native_finish": ch.get("native_finish_reason"),
        "cost": u.get("cost"), "sec": round(dt, 1), "think": THINK}) + "\n"); SIDE.flush()
    return (m.get("content") or ""), reasoning, dt


def call_probe(model, messages, temp): return _post(messages, temp, MAX_PROBE)
def call_base(model, prompt, temp): return _post([{"role": "user", "content": prompt}], temp, MAX_BASE)[0]


probe.call = call_probe; baseline.call = call_base


def stance():
    CELL["name"] = "stance_B"
    sys.argv = ["probe.py", "--model", TAG, "--sys", "neutral", "--axis", "B", "--n", os.environ.get("BATTERY_N", "5"),
                "--temp", "0.3", "--out", f"{D}/results/{TAG}_neutral_B.jsonl"]; probe.run()


def benign():
    CELL["name"] = "benign"
    sys.argv = ["refusal_check.py", TAG, f"{D}/results/{TAG}_refusal_check.jsonl"]
    runpy.run_path(f"{D}/refusal_check.py", run_name="__main__")


def base():
    CELL["name"] = "baseline"
    sys.argv = ["baseline.py", "--model", TAG, "--n", "3", "--out", f"{D}/results/{TAG}_baseline.jsonl"]; baseline.main()


def smoke():
    CELL["name"] = "smoke"
    ans, th, dt = _post([{"role": "system", "content": probe.NEUTRAL_SYS},
                         {"role": "user", "content": "In one sentence: what does a heat pump do?"}], 0.3, MAX_PROBE)
    print(f"answer {len(ans)} chars, reasoning {len(th)} chars, {dt:.1f}s: {ans[:200]!r}", flush=True)


for name, fn in (("smoke", smoke), ("stance", stance), ("benign", benign), ("baseline", base)):
    if WHAT == name or (WHAT == "all" and name != "smoke"):
        t0 = time.time(); print(f"{time.strftime('%H:%M:%S')} START {TAG} {name}", flush=True); fn()
        print(f"{time.strftime('%H:%M:%S')} END {TAG} {name} {round(time.time() - t0)}s", flush=True)
