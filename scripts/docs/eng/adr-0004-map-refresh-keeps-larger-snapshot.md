title: ADR-0004: The map refresh keeps the larger snapshot
summary: The deploy job replaces `map/graph.json` only when the new crawl has at least as many nodes and links as the committed snapshot.
parent: decision-log
order: 4
adr: 4
status: accepted
created: 2026-10-08
labels: adr, decision
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

The deploy job crawls the live sites before each deploy. Substack answers some GitHub runners with 403, and a partial crawl would shrink the map.

## Decision

The deploy job replaces `map/graph.json` only when the new crawl has at least as many nodes and links as the committed snapshot.

## Consequences

A real removal shows on the map only after a local crawl is committed. See [Map crawler](doc:eng/map-crawler).
