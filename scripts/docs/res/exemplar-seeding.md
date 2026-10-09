title: 02: Exemplar seeding
summary: Tested whether two corrected-output exemplars injected at session start lower cold-start relapse; result, no change at this dose, with three earlier attributions withdrawn.
parent: experiments
order: 20
labels: experiments, momentum, cold-start, null-result
---
Exemplar seeding was a test of whether two corrected-output exemplar pairs injected at every session start pull cold-start relapse toward the mid-session rate; scored by blocked-turn event, the result is no change at this dose (1.00 per 10K characters against a 0.84 control).

| field | value |
|---|---|
| status | no change at this dose; behavioural momentum open |
| prediction | committed 2026-08-07 in [the replication post](https://redd.it/1vi586n) |
| arm installed | 2026-08-07T18:28+02:00, SessionStart hook |
| evaluated | 2026-09-22 |
| n | cold-start: 36 events pre-install, 17 post-install |
| published page | [/experiments/](/experiments/), section 02; [/claims/](/claims/) |

## Prediction and outcomes

The prediction: seeding pulls cold-start relapse from 2.89 toward 0.42 per 10K characters (weighted unit, as published then). Three outcomes were pre-registered: a drop supports the momentum mechanism, no change weakens it at this dose, a rise is read as bad-example leakage. Each assistant turn is assigned to an arm by its own timestamp against the install boundary.

## Result

| regime | arm | events | prose kchars | events /10K | weighted /10K (superseded) |
|---|---|---|---|---|---|
| cold-start | pre-install | 36 | 427 | 0.84 | 3.02 |
| cold-start | post-install | 17 | 171 | 1.00 | 6.86 |
| mid-session | pre-install | 10 | 573 | 0.17 | 0.35 |
| mid-session | post-install | 16 | 815 | 0.20 | 0.87 |

The stop-hook log records a weight per blocked turn: em-dash x25 counts as 25. Across the log, 13 turns with weight of ten or more carry 40% of all weight, and two sessions carried the whole post-install "rise". Three attributions were published and withdrawn on the same day, 2026-09-22, in order: priming from the BAD exemplar halves, a period confound, and model version (a 30x spread resting on one catch in a 63K-char cell).

> [!warning] Disclosed on the page: the scoring unit was changed after the result, and the unit was not fixed in the prereg. Under the weighted unit the arm scores as "refuted in direction"; under the event unit, as "no change". Both units are in the table.

## Next arm, pre-registered before install

Good-only exemplars (BAD halves removed), a dated install boundary, model recorded per turn, SessionStart stack hashed. Primary metric: blocked-turn events per 10K prose characters. Good-only cold-start below 0.84 supports momentum; at or above refutes it at this dose. Evaluation one month after install.

Named limits: single operator, not blinded; 17 events in 171K prose characters is thin; the seed was never isolated from the rest of the SessionStart stack.

## Files and rerun

- [scripts/exemplar.py](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/scripts/exemplar.py): v4, event-scored; the header lists v1 to v4 and what changed in each
- [scripts/model_rate.py](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/scripts/model_rate.py): superseded 2026-09-22, kept as a receipt of the withdrawn 30x reading

From the script header, with the stop-hook log and transcripts on the operator's machine:

```bash
python3 scripts/exemplar.py
```
