title: Predictions and hashes
summary: How predictions and preregistrations are frozen and hashed before a run, and how the conformity run checks every hash on every push; 8 files, all matching.
order: 60
labels: prereg, predictions, sha256, integrity
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: reference
---
Predictions and preregistrations are written before a run, hashed with sha256 and listed in predictions/HASHES.txt; the conformity run on every push compares each file with its listed hash, and the run of 2026-10-09T07:54:32Z shows all 8 files matching.

| field | value |
|---|---|
| status | 8 prediction files, 0 problems (check predictions.hashes, requirement CC-6.3) |
| dates | first prediction written 2026-09-21; latest files hashed 2026-10-07 |
| ledgers | predictions/HASHES.txt; bench/HASHES.txt for the fawn-opener benchmark |
| published page | [/predictions/HASHES.txt](/predictions/HASHES.txt), [/conformity/](/conformity/) |

## The files

| file | what it holds | sha256 starts | hashed |
|---|---|---|---|
| the-cheating-moved-2026-09-21.txt | the prediction block as first written, from local vault commit f3f39ae | 955e60c9 | 2026-09-29 |
| the-cheating-moved-2026-09-29.txt | the block as published, with three amendments | 66ed5f04 | 2026-09-29 |
| continuous-conformity-self-assessment-2026-10-03.txt | predicted results for run 1 | 8ed4f766 | 2026-10-03, before scoring |
| sandbox-eval-04-prereg-v1.txt | experiment 04 prereg | ed5171af | 2026-10-07, before any scenario reached any model |
| sandbox-eval-04-prereg-v2.txt | amendment: output cap, ABSTAIN and TRUNCATED, qwen3-coder-30b | b07fb926 | 2026-10-07 |
| sandbox-eval-04-prereg-v3.txt | short-stance arm | 309a16c9 | 2026-10-07 |
| sandbox-eval-04-prereg-v4.txt | GPT line through the Codex CLI | 47108e39 | 2026-10-07 |
| sandbox-eval-04-prereg-v5.txt | three models via Bedrock | ddf2cfd1 | 2026-10-07 |

Run 1 of the conformity assessment is a self-assessment, not a certification; its prediction is the third row.

## What a hash proves

A published hash proves the text has not changed since the hash was published. The 2026-09-21 chess block is taken verbatim from local vault commit f3f39ae (2026-09-21 18:38 +0200), and that history is not public; the diff between the two files shows every amendment. The experiment 04 files were kept in a local repository until publication and are byte-identical to the files hashed then. The chess protocol has not been run; see [/the-cheating-moved/](/the-cheating-moved/).

## How the gate checks them

`check_predictions()` in run.py reads every line of the form `<name>.txt  sha256 <64 hex>` from predictions/HASHES.txt. A listed file that is missing or has a different sha256 fails the check, and so does any `.txt` in predictions/ that is not listed. A failing check blocks the deploy. The check reads predictions/HASHES.txt only; the benchmark hashes in bench/HASHES.txt (prompts b790afb3, v1 rules 02f49ee5, v2 rules d1c5885a) are outside it. Gate details: [Conformity gate](doc:eng/conformity-gate).

## Files and rerun

- [predictions/](https://github.com/uncovertechtalent/machinebehavior.io/tree/main/predictions) and [predictions/HASHES.txt](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/predictions/HASHES.txt)
- [bench/HASHES.txt](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/bench/HASHES.txt)
- [.github/actions/conformity/run.py](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/.github/actions/conformity/run.py)

Local check, from conformity/README.md (Python 3 and Node, no network):

```bash
python3 .github/actions/conformity/run.py --root . --config conformity/site-tier.json --requirements conformity/requirements.json --out conformity --dry-run
```
