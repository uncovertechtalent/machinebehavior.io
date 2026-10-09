title: ADR-0015: Owner and review dates on every docs page
summary: Docs front matter gains `owner`, `reviewed`, `review_by` and `type` (Diátaxis).
parent: decision-log
order: 15
adr: 15
status: accepted
created: 2026-10-09
labels: adr, decision
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

The docs pages carried dates, but none said who keeps it true or when it was last checked.

## Decision

Docs front matter gains `owner`, `reviewed`, `review_by` and `type` (Diátaxis). The 50 hand-written pages carry all four, with the date each was written from its source as the first review and the next review 90 days later. Vault pages start as not reviewed.

## Consequences

The first reviews fall due in January 2027, listed on [Docs health](/inside/docs/health/). Whether the gate should block on a missing owner or a late review is an open decision with the gate owner. See [Docs tree](doc:eng/docs-tree).
