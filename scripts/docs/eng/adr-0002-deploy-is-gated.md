title: ADR-0002: The deploy is gated
summary: GitHub Pages deploys from GitHub Actions, and the deploy job depends on the conformity job.
parent: decision-log
order: 2
adr: 2
status: accepted
created: 2026-10-07
labels: adr, decision
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

The conformity checks ran after a page was live, so they could only detect a problem that readers already saw.

## Decision

GitHub Pages deploys from GitHub Actions, and the deploy job depends on the conformity job. A failed check stops the deploy and the previous build stays live.

## Consequences

A false positive blocks a deploy until the sentence is rewritten or the rule is demoted by the gate owner. The bot commit after each run moves `main`, so every push needs a rebase first. See [Conformity gate](doc:eng/conformity-gate).
