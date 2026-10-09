title: ADR-0003: The map loads d3 and its fonts from public CDNs
summary: The map page loaded d3 7.9.0 from cdnjs and Space Grotesk and JetBrains Mono from Google Fonts.
parent: decision-log
order: 3
adr: 3
status: superseded
created: 2026-10-08
superseded_by: adr-0010-no-third-party-requests
labels: adr, decision
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
Recorded after the fact from commit [604f178](https://github.com/uncovertechtalent/machinebehavior.io/commit/604f178).

## Context

The first version of the map needed a force-directed graph library and the two site fonts, and the fastest path was to link them.

## Decision

The map page loaded d3 7.9.0 from cdnjs and Space Grotesk and JetBrains Mono from Google Fonts.

## Consequences

Each visit sent the reader's address to two third parties. Replaced the next day by [ADR-0010](doc:eng/adr-0010-no-third-party-requests), which serves both from the site.
