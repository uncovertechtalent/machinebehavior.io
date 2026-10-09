title: Slips log
summary: Running log of register and stance slips caught while drafting the published pieces, with who caught each one; 72 slips from 2026-09-29 to 2026-10-06.
order: 40
labels: slips, register, self-audit, log
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: reference
---
The slips log records the register and stance slips caught while drafting the site's pieces, and who caught each one; it holds 72 slips across 8 published pieces and 1 unpublished draft set, 57 of them caught by the same model session that wrote the text.

| field | value |
|---|---|
| status | running; the log starts on 2026-09-29 |
| rows | 72, dated 2026-09-29 to 2026-10-06 |
| drafting model (author column) | Claude (Fable 5.1) 48, Claude (Opus 5.5) 16, Claude with model not recorded (author, Language and coordinator sessions) 8 |
| published page | [/slips/](/slips/) |

## What counts

A slip is a device or a claim that did not belong in the text: a speech device in silent-read writing, an overclaim, a staged contrast, an undisclosed change. Factual corrections after publication go in each piece's changelog and errata. Drafts that are not published carry the label "(vault, unpublished)".

## By who caught it

| relation | meaning | slips |
|---|---|---|
| self | the same model session that wrote the text | 57 |
| other session | a separate model session reviewing it | 10 |
| hook | a mechanical rule at the output boundary blocked the text before anyone read it | 3 |
| human | Stefan | 1 |
| reader | someone who read the published piece | 1 |

The most frequent devices: personification 13, overclaim 9, thing as subject 7, announced count 6, one-line punch 6.

> [!note] Limits on the page: the log holds only slips someone caught. The "self" count includes checks the model ran under a written procedure (the mode-leak pass), so the self count measures a procedure followed, with unprompted self-correction not counted apart.

## Cross-check with the deploy gate

The grader.fixtures check on [/conformity/](/conformity/) runs the site's rule table over the "before" text of all 72 slips and catches 0 of them; the 72 are stance and mode-leak devices outside the lexical grader's reach.

> [!warning] Page disagreement: in the claims ledger entry of 2026-10-07, all 72 are counted as caught by a reader (model or human). The log itself has 3 rows with relation "hook", all from a personification rule in the drafting harness (write-scan hook, Stop hook, vestige scanner). The counts here come from the log's relation column.

## Files

- [slips/log.csv](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/slips/log.csv): the data; columns `date`, `piece`, `author`, `device`, `before`, `after`, `caught_by`, `relation`, `reader_catch`
- [scripts/slips_page.py](https://github.com/uncovertechtalent/machinebehavior.io/blob/main/scripts/slips_page.py): builds slips/index.html from the CSV, with the counts by relation, device and piece

## Rebuild

From the script docstring, run from the repo root:

```bash
python3 scripts/slips_page.py
```

A new slip is a new CSV row; the page and its counts come from the rebuild.
