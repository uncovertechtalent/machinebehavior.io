title: ADR-0008: Docs pages are map nodes
summary: Docs pages carry their front matter as meta tags, and the crawler adds them to the graph with parent links as `tree` edges.
parent: decision-log
order: 8
adr: 8
status: accepted
created: 2026-10-09
labels: adr, decision
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

The map showed the published pages and posts, but none of the reference notes behind them.

## Decision

Docs pages carry their front matter as meta tags, and the crawler adds them to the graph with parent links as `tree` edges.

## Consequences

One graph holds everything published, so a reader or a model can walk from a claim to the note it rests on. The graph grew from about 120 to over 400 nodes, and the map gained a filter for docs.
