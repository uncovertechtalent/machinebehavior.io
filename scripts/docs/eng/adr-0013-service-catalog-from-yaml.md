title: ADR-0013: A service catalog from YAML in the repository
summary: Every service is one YAML file in `services/`, validated at build by a strict standard-library reader.
parent: decision-log
order: 13
adr: 13
status: accepted
created: 2026-10-09
labels: adr, decision
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

The systems were documented page by page, but nothing listed them in one place with who answers for each, how much each matters and where its runbooks are.

## Decision

Every service is one YAML file in `services/`, validated at build by a strict standard-library reader. The build writes `/inside/services/`, a page per service and `services.json`. Service pages are `service` nodes in the map, and the dashboards they link become `dashboard` nodes.

## Consequences

A service without docs or runbooks shows the gap on its page. All twelve services have one owner, so the owner field names who is accountable and no team structure sits behind it. See [Service catalog](doc:eng/service-catalog).
