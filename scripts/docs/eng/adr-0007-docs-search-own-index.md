title: ADR-0007: Docs search over its own index, Enter opens the first hit
summary: The docs top bar searched `inside/docs/search.json` only, and Enter opened the first hit.
parent: decision-log
order: 7
adr: 7
status: superseded
created: 2026-10-09
superseded_by: adr-0012-one-top-bar-and-search
labels: adr, decision
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
Recorded after the fact from commit [0e4fe0a](https://github.com/uncovertechtalent/machinebehavior.io/commit/0e4fe0a).

## Context

The first docs tree needed a search box before any other part of Inside had one.

## Decision

The docs top bar searched `inside/docs/search.json` only, and Enter opened the first hit.

## Consequences

Inside had a second search box over the map, so there were two boxes over two indexes, and Enter could open a page the reader had not chosen. Replaced by [ADR-0012](doc:eng/adr-0012-one-top-bar-and-search).
