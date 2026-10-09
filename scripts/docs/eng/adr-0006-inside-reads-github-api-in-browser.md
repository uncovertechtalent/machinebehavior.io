title: ADR-0006: Inside reads the deploy feed from the GitHub API in the browser
summary: The page called the GitHub Actions API from the visitor's browser for each repository on every load.
parent: decision-log
order: 6
adr: 6
status: superseded
created: 2026-10-09
superseded_by: adr-0010-no-third-party-requests
labels: adr, decision
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
Recorded after the fact from commit [cc9db2a](https://github.com/uncovertechtalent/machinebehavior.io/commit/cc9db2a).

## Context

The first Inside front page needed the latest workflow runs of the public site repositories.

## Decision

The page called the GitHub Actions API from the visitor's browser for each repository on every load.

## Consequences

Each visit sent a request to GitHub, and the anonymous API limit of 60 requests per hour applied per visitor. Replaced the same day by [ADR-0010](doc:eng/adr-0010-no-third-party-requests): the deploy job writes `/inside/deploys.json`.
