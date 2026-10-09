title: Weekly decision-layer probe
summary: A weekly rerun of a frozen experiment 04 subset on a reference model, recorded for requirement CC-6.6; first record 2026-10-07, record-only until 2026-11-04.
parent: experiments
order: 50
labels: probe, conformity, stance, record-only
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
The decision-layer probe reruns a frozen subset of experiment 04 on a reference model and records the fold rate for requirement CC-6.6; the first record (2026-10-07) shows a fold rate of 0.727 for the bare arm and 0.4 for the arm with the short stance instruction.

| field | value |
|---|---|
| status | record-only until 2026-11-04 (four weeks from the first run); no threshold; fold rates never block |
| first record | 2026-10-07T18:38:47Z |
| model | qwen.qwen3-coder-30b-a3b-v1:0 on Bedrock, eu-central-1 |
| n | 12 scenarios x 6 characters = 72 runs per arm; 144 runs, 720 calls, USD 0.269 (cap USD 1.0) |
| published page | [/conformity/](/conformity/) (check decision.probe), [/inside/](/inside/) |

## What runs

Twelve odd-numbered scenarios (s001 to s023) from the experiment 04 set, all six pressure characters, five turns. Subset file `probe/subset-v1.json`, sha256 1eadb377fdf9b5ba…; frozen sha256 e751c7edef03f2b9…. Two arms:

| arm | object of test | correct before pressure | correct after | fold rate [95% CI] |
|---|---|---|---|---|
| reference (baseline) | the model with the task prompt only | 0.764 | 0.306 | 0.727 [0.598, 0.827] (40/55) |
| assembly (stance-short) | the same model plus the short stance instruction (prereg v3, 2,846 characters) | 0.764 | 0.472 | 0.4 [0.281, 0.532] (22/55) |

Fold rate by character, reference against assembly: alpha-wolf 0.778 and 0.444, arrested-twelve 0.889 and 0.8, darvo 0.667 and 0.0, denial-cascader 1.0 and 0.333, fawn-mirror 0.0 and 0.0, pack-wolf 1.0 and 0.778.

> [!info] Scope, from the record and /conformity/: the object of test is a reference model in two arms, not the Claude Code assembly that writes the pages. Under the same design three larger models folded on 0 of 72 runs each ([experiment 04, v5](doc:res/experiment-04-folding-under-pressure)), so the fold rate is a property of the probed model.

## How the gate reads it

The probe record is written weekly from the probe host, per the `check_probe()` docstring in run.py. Every conformity run reads `conformity/probes/latest.json`: missing fields give a fail, a record older than twice the 7-day schedule interval gives a fail as stale, and otherwise the result is partial with the fold rates printed. See [Conformity gate](doc:eng/conformity-gate).

## Files

- [conformity/probes/latest.json](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/conformity/probes/latest.json): current record
- [conformity/probes/probe-2026-10-07.json](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/conformity/probes/probe-2026-10-07.json): first record, byte-identical to latest.json on 2026-10-09
- [.github/actions/conformity/run.py](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/.github/actions/conformity/run.py): the check

## Rerun

The record lists these steps. `probe/probe.py` is not in this repository.

1. rsync the repo to a host with Bedrock credentials
2. `.venv/bin/python probe/probe.py`
3. compare `arms.*.fold_rate` with this record
