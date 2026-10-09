title: ADR-0010: No third-party requests on page load
summary: Fonts and d3 are served from the site itself, and the Inside deploy feed is a JSON written by the deploy job.
parent: decision-log
order: 10
adr: 10
status: accepted
created: 2026-10-09
supersedes: adr-0003-map-loads-from-public-cdns, adr-0006-inside-reads-github-api-in-browser
labels: adr, decision
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

Fonts came from Google, d3 from a CDN and the Inside deploy feed from the GitHub API, so opening a page passed the visitor's address to three companies. The LG München I judgment of 2022-01-20 (3 O 17493/20) found this unlawful for Google Fonts loaded without consent.

## Decision

Fonts and d3 are served from the site itself, and the Inside deploy feed is a JSON written by the deploy job. Opening a page sends no request to a third party. Grafana frames load only when the reader scrolls to them.

## Consequences

The deploy feed on Inside is as fresh as the last deploy; the live view is the Website deploys dashboard. Font and d3 updates are manual. Later Inside data (board, search index) follows the same pattern.
