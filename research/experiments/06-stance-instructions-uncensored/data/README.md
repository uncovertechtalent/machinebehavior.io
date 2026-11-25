# Experiment 06 data: stance under pressure on uncensored models

This folder holds every recorded answer behind experiment 06 on machinebehavior.io, its labels, the checks on those labels, and every number the write-up states, recomputed from the records. The write-up is at https://machinebehavior.io/research/experiments/06-stance-instructions-uncensored/ and the report page at https://machinebehavior.io/research/experiments/06-stance-instructions-uncensored/report/.

Author: Stefan Coetzee, machinebehavior.io, 2026.

## Files

| File | What it holds |
|---|---|
| `records.jsonl` | One line per conversation: the probe, the user turns, the model's answers, the model and build, the condition, temperature, thinking mode, repetition, finish reason, and token counts. |
| `labels.jsonl` | One label per record: `fold`, `hedge`, `hold`, or `cut_off` on the pressure probes, and `comply`, `partial`, or `refuse` on the two benign requests. The pages say caved, wobbled, and held for fold, hedge, and hold. |
| `agreement.json` | Every blind agreement check on the labels: sample size, agreement, Cohen's kappa, and the records the readers disagreed on. |
| `claims.json` | Every number in the write-up: the sentence, the record filter, the metric, the value, the records behind it, and whether it holds. The pages link each number to its row. |
| `gate.json` | The result of the after-the-answer fact checks for each record they ran on: flagged or not, and why. |
| `probes.json` | The questions: id, kind, the true fact, and the user turns. |
| `conditions/` | The exact instruction texts each condition used, with `index.json` giving the sha256 of each file and its word count. |
| `models.json` | Each build: repository, pinned commit, file sha256, quantisation, method as its uploader states it, and its licence and output terms. |
| `results.csv`, `comparison.csv` | The counts per run, model, condition, and question set. |
| `coverage.json` | What the export holds, by run and by labelling pass. |
| `croissant.json` | MLCommons Croissant 1.0 metadata, so dataset tools can load the folder. |
| `RULE.txt` | The labelling rule for the steel-and-feathers question (B4), written before the consistency pass that used it. Claims C06-54 to C06-56 rest on it. |
| `RULE-benign.txt` | The labelling rule for the two benign requests. |
| `scripts/` | The runners (`scripts/runs/`), the blinding and unblinding scripts (`scripts/labelling/`), and the exporter that writes this folder and checks every claim (`scripts/export/`). |
| `SHA256SUMS` | The sha256 of every other file in the folder. |

## Check it

```
sha256sum -c SHA256SUMS                       # or: shasum -a 256 -c SHA256SUMS
python3 scripts/export/claims.py . scripts/export/claims_spec.json   # recomputes every claim; exit 0 when all hold
python3 scripts/export/report.py . --write report.html               # rebuilds the report page from this folder alone
```

`claims.py` writes a fresh `claims.json`, so run it on a copy if you want to keep the published one for comparison.

## What is not here

- The raw run folders and the hand-label source files. The exporter read them and wrote this folder.
- The shell wrappers that only set hosts and paths. In the published scripts, private host names and paths are replaced by `<runs>` and `<export>`, and the exporter's private-pattern list holds one pattern that never matches. The runners need a model server of your own to run again.

## Licences

- **Data:** every file outside `scripts/` is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0), https://creativecommons.org/licenses/by/4.0/. Credit "Stefan Coetzee, machinebehavior.io, experiment 06".
- **Scripts:** every file in `scripts/` is licensed under the MIT licence. Copyright (c) 2026 Stefan Coetzee. Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Model output

- Every answer in `records.jsonl` is output of a language model, published as recorded and not edited. None of it is written by a person.
- The licence and output terms of each build are in `models.json`, as read on 2026-11-25. For 16 of the 18 builds the entry says the licence does not restrict publishing the outputs. Two are marked unclear: the Gemma 4 E4B Heretic build (its licence tag is unresolved; its base model is Apache 2.0) and the Qwen3.8-27B Swift 1.5 Heretic build (its licence sets conditions on the weights and has no clause on outputs).
- **GLM-5.3 rows:** the 46 GLM-5.3 records were made through Z.AI's hosted API. Z.AI's terms, as summarised in `models.json`, bar using its outputs to train models that compete with Z.AI. CC BY 4.0 cannot remove that limit, so it still applies to anyone who uses those rows.
- Z.AI's and Featherless's terms ask that outputs be shown as AI-generated. This section does that for the whole folder.
