#!/usr/bin/env python3
"""heldout2.py against a llama.cpp server on 127.0.0.1:8099, for models that do not run under Ollama on this box.
Same probes, turns, system and suffix handling, and record shape as heldout2.py; only the transport differs. The body
mirrors the battery driver's llama.cpp backend: temperature 0.3, max_tokens as num_predict, seed -1, repeat_penalty 1.0,
top_k 40, top_p 0.9, min_p 0.0, enable_thinking per --think.
usage: as heldout2.py (the MODEL argument is only a label here)."""
import json, os, sys, time, urllib.request
sys.path.insert(0, os.path.expanduser("~/battery/runs/2026-11-24-v2"))
import heldout2


def chat(model, messages, think, num_predict):
    body = json.dumps({"messages": messages, "temperature": 0.3, "max_tokens": num_predict, "seed": -1, "stream": False,
                       "repeat_penalty": 1.0, "top_k": 40, "top_p": 0.9, "min_p": 0.0,
                       "chat_template_kwargs": {"enable_thinking": bool(think)}}).encode()
    for attempt in range(4):
        try:
            req = urllib.request.Request("http://127.0.0.1:8099/v1/chat/completions", body, {"Content-Type": "application/json"})
            r = json.load(urllib.request.urlopen(req, timeout=1800))
            c = r["choices"][0]
            return (c["message"].get("content") or "", c["message"].get("reasoning_content") or "",
                    c.get("finish_reason"), r.get("usage", {}).get("completion_tokens"))
        except Exception:
            if attempt == 3:
                raise
            time.sleep(10)


heldout2.chat = chat
if __name__ == "__main__":
    heldout2.main()
