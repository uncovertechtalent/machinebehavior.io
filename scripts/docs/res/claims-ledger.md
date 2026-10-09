title: Claims ledger
summary: Every substantive claim of the programme with its status, receipts and the observation that would refute it; seven claims, four supported, one refuted, one open, one proposed.
order: 20
labels: claims, falsification, ledger
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: reference
---
The claims ledger lists each claim of the programme with its status, receipts and refutation condition; of seven claims, four are supported, one is refuted, one is open with its prediction refuted, and one is proposed.

| field | value |
|---|---|
| status | running; refuted claims stay listed |
| latest dated evidence | 2026-10-07 (experiment 04 and the slips cross-check) |
| published page | [/claims/](/claims/) |
| source file | [claims/index.html](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/claims/index.html) |

## The claims

| claim | status | main receipt | would refute |
|---|---|---|---|
| Sycophancy is layered symptom substitution | supported | experiment 04: 0 of 432 fawn openers, 75 percent fold rate, one model; the site's rule table catches 0 of 72 logged slips | a model holding suppression at one layer for months without the reflex surfacing at another |
| Only two controls hold in production: a mechanical gate at the output boundary and an external reader | supported | 100 blocked turns for one pattern in 34 days; 8 relapses in nine days, all caught externally | sustained instruction-only compliance across cold starts, or a documented self-catch of a stance-layer relapse |
| Runtime suppression decays with session length | refuted | mean normalised catch position 0.54 against 0.50 | kept as the first externally proposed test |
| Relapse clusters at cold starts | supported | 0.88 against 0.18 events per 10K characters, about 5x | matched rates without boundary enforcement, or a topic-mix artefact |
| Behavioural momentum holds the filter | open, prediction refuted | seeded cold-start 1.00 against a 0.84 control | next arm: good-only cold-start at or above 0.84 refutes it at this dose |
| Stance and premise relapses are catchable only across turns, by external review | supported | the per-turn scanner caught zero structural relapses; a human reading across turns caught all eight register instances | a same-turn detector that catches premise ratification at better than chance |
| The "conspiracy theory" label in model output is corpus-inherited classification | proposed | historical cases; a label gate as countermeasure | a symmetric corpus study, or symmetric labelling of matched claim pairs; neither has been run |

## Corrections on the page

- 2026-09-22: weighted catches replaced by blocked-turn events (cold start 7x to about 5x; 297 em-dash catches to 100 blocked turns).
- 2026-09-29: "8 stance-layer relapses" corrected to six stance and two lexical.
- 2026-09-29: "every lexical relapse" corrected to every relapse that matches the scanner's catalogue.

The three layers are frozen (lexical, stance, premise). A failure that fits none of them counts against the first claim.

> [!note] Named limit: the eight relapses are coded by one rater, the person holding the hypothesis. A second rater is outstanding; the set is open for rating in the [objections register](doc:res/objections-register).

## How to check

The ledger has no data file of its own. Receipts: [half-life study](doc:res/half-life-study), [exemplar seeding](doc:res/exemplar-seeding), [experiment 04](doc:res/experiment-04-folding-under-pressure), [slips log](doc:res/slips-log). The 0 of 72 figure is the grader.fixtures check on [/conformity/](/conformity/), rerun on every push.
