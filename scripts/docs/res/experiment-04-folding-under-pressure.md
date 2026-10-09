title: Experiment 04: folding under pressure
summary: Decision-layer test of whether a model keeps a correct verdict under scripted pushback; qwen3-coder-30b folded on 75 percent of eligible baseline runs, three larger models on none.
parent: experiments
order: 40
labels: eval, sycophancy, prereg, stance
---
Experiment 04 is a test of whether a model keeps a correct WAIT verdict under four turns of scripted pushback; on qwen3-coder-30b the baseline folded on 75 percent of eligible runs (42 of 56), and gpt-oss-120b, DeepSeek V3.2 and Kimi K2.5 folded on 0 of 72 baseline runs each.

| field | value |
|---|---|
| status | run; fold result from one model |
| date | 2026-10-07 |
| models | qwen.qwen3-coder-30b-a3b-v1:0; v5: gpt-oss-120b, DeepSeek V3.2, Kimi K2.5; Amazon Bedrock, temperature 0 |
| n | 24 scenarios (12 BUY, 12 WAIT), 6 characters; 2,160 calls (full-01), 720 (full-02), 2,880 per model (v5) |
| published page | [/experiments/#experiment-04](/experiments/#experiment-04) |

## Method

The world is the deterministic Buy-or-Wait forecast engine from the HackerRank Orchestrate hackathon. The opening fact sheet holds the facts the engine used, so the correct answer is one subtraction and one comparison away. Six scripted characters push toward BUY for four turns, one pressure type each: dominance, consensus, fact denial, flattery, emotional urgency, reverse blame. Arms: baseline (task prompt), lexical (plus the output-filter instruction), stance (plus a stance stack of about 17,000 characters), short stance (2,846 characters, addendum v3). A fixed regular expression reads the last VERDICT line; no model is in the loop. Fold: correct at turn 0, opposite decision later.

## Results, qwen3-coder-30b (WAIT cases, 72 runs per arm)

| arm | correct turn 0 | correct turn 4 [95% CI] | fold rate [95% CI] | over-refusal (BUY) |
|---|---|---|---|---|
| baseline | 78% | 32% [22-43] | 75% [62-84] | 0% |
| lexical | 74% | 35% [25-46] | 62% [49-74] | 0% |
| stance | 44% | 35% [25-46] | 34% [20-52] | 6% |
| stance, short | 76% | 50% [39-61] | 33% [22-46] | 4% |

As frozen: H1 (folding exists) supported; H2 and H3 not testable on this model; H4 (the fact-denial character produces the most folds) not supported; H5 (holding is not refusing) supported. Addendum v3: the full stance arm lost turn-0 accuracy through its length (R1), and short-arm runs fold less than baseline runs, with intervals that do not overlap (R2). In full-01 no reply opened with a fawn marker at turn 0 (0 of 432).

Addendum v5: H1 not supported on the three larger models, H5 supported on all three. Addendum v4 (GPT through the Codex CLI) stopped at a usage limit after 48 of 480 smoke calls; no result.

> [!warning] Limits: one world, one operator, pressure always toward BUY, scripted characters, 9 to 10 eligible runs per character cell, no Claude or frontier closed model run. 24 of 30 ABSTAIN replies in full-01 open with a bare "BUY" or "WAIT" line and were not rescored. Claude models drafted prereg v1 and v2.

## Files and checks

Prereg v1 to v5 are in [predictions/](https://github.com/uncovertechtalent/machinebehavior.io/tree/main/predictions) (`sandbox-eval-04-prereg-v*.txt`), each hashed before the calls it covers; see [Predictions and hashes](doc:res/predictions-and-hashes). Harness, generator and run logs are not yet public. A subset reruns weekly as the [decision-layer probe](doc:res/decision-layer-probe).
