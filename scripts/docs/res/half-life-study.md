title: 01: The half-life study
summary: Tested whether suppressed output patterns relapse more as a session gets longer; the temporal half-life is refuted, and relapse clusters at cold starts.
parent: experiments
order: 10
labels: experiments, half-life, cold-start, refuted
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
The half-life study was a test of whether relapse into banned output patterns grows with session length; the temporal half-life is refuted (mean normalised catch position 0.54 against 0.50 for no drift), and relapse clusters at cold starts, at about 5x the mid-session rate per unit of prose by blocked-turn event.

| field | value |
|---|---|
| status | half-life refuted; cold-start clustering supported in the [claims ledger](doc:res/claims-ledger) |
| dates | published 2026-08-07; unit note added 2026-09-22 |
| dataset | 34 days (2026-07-04 to 2026-08-07), 103 catch events, 224 weighted pattern hits, 62 sessions with full transcripts |
| model | single operator, single model family |
| published page | [/experiments/](/experiments/), section 01 |

## Method

The question came from a commenter on the [founding specimen](https://redd.it/1vdg3en). A stop hook at the output boundary scans every response against a banned-pattern catalogue and logs each catch with timestamp, session id, pattern and count. Each assistant turn got a context regime: cold-start (first 60 minutes of a session), post-resume (60 minutes after a gap over 4 hours), post-compaction, or mid-session. Rates are per 10K characters of assistant prose, because cold-start turns are chattier and raw rates would inflate the effect.

## Result

| regime | blocked turns (events) | events /10K | weighted catches | weighted /10K |
|---|---|---|---|---|
| cold-start | 40 | 0.88 | 145 | 2.89 |
| mid-session | 11 | 0.18 | 31 | 0.42 |
| post-resume | 13 | 0.27 | 46 | 0.79 |
| post-compaction | 2 | 1.72 (n=2) | 2 | 1.72 (n=2) |

Prose normalisation halved the raw cold-start ratio (12x down to 7x). The study was published in weighted catches (2.89 against 0.42, about 7x). On 2026-09-22 that unit was found to inflate bulk-text turns. The event columns were computed after publication, and the ratio by event is about 5x (0.88 against 0.18). The figure on the experiments page is "roughly 5x by event, 7x weighted".

Behavioural momentum (the model imitating its own recent corrected output) was proposed as the operative control. Its status is open; see [02: Exemplar seeding](doc:res/exemplar-seeding).

> [!note] Named limits on the page: single operator, single model family, lexical layer only. Session-opening topic mix is unmeasured and could carry part of the cold-start effect. The post-compaction cell is two events.

## Files

- [scripts/halflife.py](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/scripts/halflife.py): relapse position against session length
- [scripts/halflife2.py](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/scripts/halflife2.py): prose-normalised rerun by context regime
- Replication post with the method: [redd.it/1vi586n](https://redd.it/1vi586n)

## How to check

Both scripts read the stop-hook log (`~/.claude/vestige-scan.log`) and the session transcripts from the operator's home directory, as set in each script header. A rerun needs that machine or a copy of those files. The regime boundaries (60 minutes, 4-hour gap, cutoff 2026-07-04) are constants at the top of halflife2.py.
