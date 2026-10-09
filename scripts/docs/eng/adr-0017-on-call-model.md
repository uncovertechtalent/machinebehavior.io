title: ADR-0017: State the on-call model and propose Alertmanager routing
summary: The [On-call and escalation](doc:obs/on-call) page states the model as it runs: one operator, agent sessions as responders, the deploy gate as the only control that acts on its own, and no Alertmanager.
parent: decision-log
order: 17
adr: 17
status: accepted
created: 2026-10-09
labels: adr, decision
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

A founder checking the setup asks who gets woken up. Prometheus evaluates 13 alert rules, and none reaches a person.

## Decision

The [On-call and escalation](doc:obs/on-call) page states the model as it runs: one operator, agent sessions as responders, the deploy gate as the only control that acts on its own, and no Alertmanager. It proposes a routing and leaves it unwired.

## Consequences

Alerts stay visible only to someone who looks; the four incidents of the week were all found that way. Wiring a page to a personal device waits for the operator's choice of receiver.
