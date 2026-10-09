title: Conformity self-assessment, run 1
summary: One working AI setup scored by the model inside it against 35 draft requirements and a hashed prediction, with pass 4, partial 16, gap 13 and n/a 2 (self-assessment, not a certification).
order: 70
labels: conformity, self-assessment, prereg, second-rater
---
In run 1 the model inside Stefan Coetzee's working AI setup scored the setup against the 35 requirements of the working draft "Continuous Conformity for Deployed AI Systems" (draft 0.2): pass 4, partial 16, gap 13, n/a 2, against a prediction hashed before scoring that matched 29 of 35. Self-assessment, not a certification.

| field | value |
|---|---|
| status | scored 2026-10-03; model second rating 2026-10-07; human second rater wanted |
| grader | Claude (Opus 5.5), inside the setup under test |
| system under test | Claude Code plus instruction files, hooks, memory and a knowledge vault |
| n | 35 requirements, CC-4.1 to CC-12.5 |
| published page | [/continuous-conformity-self-assessment/](/continuous-conformity-self-assessment/) |

## Result

| result | predicted | scored |
|---|---|---|
| pass | 7 | 4 |
| partial | 16 | 16 |
| gap | 11 | 13 |
| n/a | 1 | 2 |

Five of the six misses were too generous: applying the evidence rule (no evidence, no credit) lowered the scores. Passes: CC-6.3 (hashed prediction records), CC-9.1 (independence: 11 incidents caught by Stefan, 0 by self-audit), CC-11.3 (method and raw records published), CC-11.4 (second-rater calls and a disagreement table). Common gaps: no test cycle, no knowledge freshness, no programme document, no outside tester.

## Addendum 2026-10-07

CC-6.6, decision-layer tests under scripted pressure, was added in working draft 0.3 after [experiment 04](doc:res/experiment-04-folding-under-pressure). Scored gap, listed outside the hashed prediction so the run 1 totals stay as predicted and scored.

## Second rating 1: gpt-oss-120b

A model rater on Amazon Bedrock, blind to the run 1 scores and the prediction record, public access only, temperature 0, input sha256 7d495201eea9ea49…. Agreement 19 of 35 rows (54 percent); Cohen's kappa 0.36 over all rows. It was stricter on 6 rows, looser on 5, and recorded "cannot verify" on 5. Run 1 scores do not change; a rerun with amended evidence is the way a score moves.

> [!note] Page disagreement: [conformity/README.md](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/conformity/README.md) names draft 0.2 with 35 requirements. The newer [conformity/requirements.json](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/conformity/requirements.json) and the 2026-10-09 run on [/conformity/](/conformity/) use working draft 0.3 with 36. Run 1 is given here under draft 0.2, and the live tier under 0.3.

## Files

- [predictions/continuous-conformity-self-assessment-2026-10-03.txt](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/predictions/continuous-conformity-self-assessment-2026-10-03.txt): the prediction, sha256 8ed4f766…adf4
- [continuous-conformity-self-assessment/second-rater/gpt-oss-120b-01/](https://github.com/uncovertechtalent/machinebehavior.io/tree/main/continuous-conformity-self-assessment/second-rater/gpt-oss-120b-01): rater input, request, raw output, scored form, and the blocked Codex attempt
- [conformity/requirements.json](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/conformity/requirements.json): run 1 result per row, read by the live site tier

## Rerun

1. Check the prediction's sha256 against predictions/HASHES.txt.
2. For each row, open the evidence named and decide pass, partial, gap or n/a with the definitions in the prediction file.
3. Send disagreements by row; they will be listed next to the original score.

Several run 1 probes cover only Stefan's machine; two of them:

```bash
git -C ~/dotfiles status -s
crontab -l
```
