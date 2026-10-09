title: ADR-0016: A public-demo banner and a stated access model
summary: Every Inside page except the map carries a banner saying the intranet is a public demo and that in production it sits behind single sign-on.
parent: decision-log
order: 16
adr: 16
status: accepted
created: 2026-10-09
labels: adr, decision
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

A visitor should know the intranet is public on purpose, and a founder reading it should see how access would work in a company.

## Decision

Every Inside page except the map carries a banner saying the intranet is a public demo and that in production it sits behind single sign-on. It links the [Access model](doc:eng/access-model): public, internal and restricted spaces, who grants each, and access per user and device without a network perimeter. The site has no login and no credential form.

## Consequences

The model is a description; the one part of it that runs is the Grafana front door, which passes only the public paths. Hosting stays on GitHub Pages.
