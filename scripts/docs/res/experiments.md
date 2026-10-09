title: Experiments
summary: Overview of the four published experiments and the weekly decision-layer probe, with status, dates and headline numbers for each.
order: 10
labels: experiments, overview, eval
---
Four studies are published on [/experiments/](/experiments/): the temporal half-life is refuted, exemplar seeding showed no change at its dose, the fawn-opener benchmark has a pilot only, and experiment 04 found folding under pressure in one of four open-weight models.

| field | value |
|---|---|
| status | 01 refuted, 02 no change, 03 pilot only, 04 run; probe record-only |
| dates | 2026-08-07 (01) to 2026-10-07 (04 and the first probe record) |
| models | Claude models in the author's harness (01, 02); Haiku 4.5, GPT-5.6 (terra), llama3.1:8b (03 pilot); qwen3-coder-30b, gpt-oss-120b, DeepSeek V3.2, Kimi K2.5 (04) |
| published page | [/experiments/](/experiments/), probe on [/conformity/](/conformity/) |
| source file | [experiments/index.html](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/experiments/index.html) |

## The studies

| study | date | result |
|---|---|---|
| [01: The half-life study](doc:res/half-life-study) | 2026-08-07 | half-life refuted; cold-start relapse about 5x mid-session by event (7x weighted) |
| [02: Exemplar seeding](doc:res/exemplar-seeding) | evaluated 2026-09-22 | no change at this dose: 1.00 against 0.84 events per 10K characters |
| [03: Fawn-opener benchmark](doc:res/fawn-opener-benchmark) | prereg and pilot 2026-09-23 | pilot only; no reading scored |
| [Experiment 04: folding under pressure](doc:res/experiment-04-folding-under-pressure) | 2026-10-07 | 75 percent fold rate on qwen3-coder-30b; 0 of 72 baseline runs on three larger models |
| [Weekly decision-layer probe](doc:res/decision-layer-probe) | first record 2026-10-07 | fold rate 0.727 bare, 0.4 with the short stance instruction |

## Units

Since 2026-09-22 the primary unit for the log-based studies is the blocked-turn event: one per blocked turn. Weighted catches (one per pattern instance in the turn) are reported as a secondary column and are not used to score an outcome. The change followed the finding that the weighted unit inflates bulk-text turns. For experiments 03 and 04 the unit was fixed in the prereg before the first call.

## Data and files

Experiments 01 and 02 ran on production logs from a daily-driver agent harness: the stop-hook log and the session transcripts on the operator's machine. The paths are in the script headers (`~/.claude/vestige-scan.log`, `~/.claude/projects/*/`); those logs are not in the repo. The scripts are:

- [scripts/halflife.py](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/scripts/halflife.py) and [scripts/halflife2.py](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/scripts/halflife2.py) for 01
- [scripts/exemplar.py](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/scripts/exemplar.py) for 02, and [scripts/model_rate.py](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/scripts/model_rate.py), superseded on 2026-09-22 and kept as a receipt
- [bench/](https://github.com/uncovertechtalent/machinebehavior.io/tree/main/bench) for 03: frozen prompts, rule files, scorer and pilot outputs
- [predictions/](https://github.com/uncovertechtalent/machinebehavior.io/tree/main/predictions) for the 04 prereg and its addenda v2 to v5

The 04 harness, generator and run logs are not yet in a public repository; the prereg files record the sha256 of the scenario set, generator, character scripts and task prompt.

## Checking

Each child page lists its files and any commands the repo shows. Prereg hashes are checked on every push; see [Predictions and hashes](doc:res/predictions-and-hashes).
