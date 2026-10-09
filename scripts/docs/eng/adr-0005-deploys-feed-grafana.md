title: ADR-0005: Deploys feed Grafana without changing the workflows
summary: A separate exporter polls the GitHub Actions API and writes runs, steps and gate checks to Loki and Prometheus.
parent: decision-log
order: 5
adr: 5
status: accepted
created: 2026-10-08
labels: adr, decision
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

The deploy history of three sites lived only on the GitHub Actions pages, one repository at a time, and one repository is private.

## Decision

A separate exporter polls the GitHub Actions API and writes runs, steps and gate checks to Loki and Prometheus. The site workflows stay as they are.

## Consequences

Data arrives on the exporter's polling interval. The private repository's titles, SHAs and URLs are never stored. See [Deploy exporter](doc:obs/deploy-exporter).
