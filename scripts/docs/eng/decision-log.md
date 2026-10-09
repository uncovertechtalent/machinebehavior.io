title: Decision records
summary: Numbered architecture decision records for the platform, each with a status, the context, the decision and its consequences; superseded records stay and link their successor.
order: 80
labels: adr, decisions, governance
aliases: Decision log
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: reference
---
Each record states one decision: its number, date and status, the context that forced it, the decision, and what it costs. Decisions are made by Stefan Coetzee unless the record says otherwise. A record is never deleted: when a later decision replaces it, its status becomes superseded and it links the record that replaced it.

| Status | Meaning |
|---|---|
| proposed | Written down, not yet in force |
| accepted | In force |
| superseded | Replaced by a later record, kept for the history |

<!-- adr-index -->

## Add a record

1. Copy the newest record in `scripts/docs/eng/` to `adr-NNNN-short-name.md` with the next number.
2. Fill in context, decision and consequences; set `status`.
3. If it replaces an earlier record, add `supersedes:` here and `superseded_by:` there, and set the old one to `superseded`. The build stops when the two sides disagree.
4. Run the docs build, the gate dry run, and push. The change also appears in the [changelog](doc:eng/changelog).
