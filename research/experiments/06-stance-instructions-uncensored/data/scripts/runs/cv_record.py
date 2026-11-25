#!/usr/bin/env python3
"""Phase D, 2026-11-24: record the control-vector dose sweep properly.
For one llama-server already running on :8099 (with or without a control vector), run the battery pressure probes
B1, B6, B8 (probe.py AXIS_B, pinned) N times with the battery's call shape (system "You are a helpful assistant.",
temperature 0.3, max_tokens 600, thinking off) and append full records to OUT.
usage: cv_record.py SETTING OUT.jsonl [--n 5]"""
import argparse, json, sys, time, urllib.request, importlib.util
spec = importlib.util.spec_from_file_location("probe", "<runs>/probe.py"); probe = importlib.util.module_from_spec(spec)
sys.argv_saved = sys.argv; sys.argv = ["probe"]; spec.loader.exec_module(probe); sys.argv = sys.argv_saved
SYS = probe.NEUTRAL_SYS


def chat(msgs):
    b = json.dumps({"messages": msgs, "temperature": 0.3, "max_tokens": 600, "seed": -1, "stream": False,
                    "repeat_penalty": 1.0, "top_k": 40, "top_p": 0.9, "min_p": 0.0,
                    "chat_template_kwargs": {"enable_thinking": False}}).encode()
    r = json.load(urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:8099/v1/chat/completions", b,
                                                                 {"Content-Type": "application/json"}), timeout=900))
    c = r["choices"][0]
    return c["message"]["content"] or "", c.get("finish_reason")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("setting"); ap.add_argument("out"); ap.add_argument("--n", type=int, default=5)
    a = ap.parse_args()
    probes = [p for p in probe.AXIS_B if p["id"][:2] in ("B1", "B6", "B8")]
    with open(a.out, "a") as fh:
        for rep in range(a.n):
            for p in probes:
                msgs = [{"role": "system", "content": SYS}]
                first = None
                if p.get("two_turn"):
                    msgs.append({"role": "user", "content": p["turn1"]}); first, _ = chat(msgs)
                    msgs += [{"role": "assistant", "content": first}, {"role": "user", "content": p["turn2"]}]
                else:
                    msgs.append({"role": "user", "content": p["prompt"]})
                ans, fin = chat(msgs)
                fh.write(json.dumps({"setting": a.setting, "probe": p["id"], "rep": rep, "first_turn": first, "answer": ans,
                                     "finish": fin, "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z")}) + "\n"); fh.flush()
                print(a.setting, p["id"], rep, fin, repr(ans[:60]), flush=True)


if __name__ == "__main__":
    main()
