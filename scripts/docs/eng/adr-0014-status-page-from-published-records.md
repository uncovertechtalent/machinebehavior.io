title: ADR-0014: A status page from records the site already publishes
summary: `/inside/status/` reads each site's gate record, `/inside/deploys.json` and the map snapshot time in the browser, and shows the incident history from `incidents/*.yml` with the stages Investigating, Identified, Monitoring and Resolved.
parent: decision-log
order: 14
adr: 14
status: accepted
created: 2026-10-09
labels: adr, decision
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

A visitor could see metrics on the dashboards but not, at a glance, whether a service was healthy or what went wrong last week.

## Decision

`/inside/status/` reads each site's gate record, `/inside/deploys.json` and the map snapshot time in the browser, and shows the incident history from `incidents/*.yml` with the stages Investigating, Identified, Monitoring and Resolved. Services without a record on the site say "No live check".

## Consequences

Six of twelve services have a live check on the page. Times without a record behind them are shown as "time not recorded". See [Status page](doc:eng/status-page).
