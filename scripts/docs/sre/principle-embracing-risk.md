title: Risk is a budget
summary: A target of 100% reliability costs more than users can notice; the gap between the target and 100% is an error budget for change. Here tiers set the order of response and the Local LLM has burn-rate alerts, but no policy says what happens when a budget is spent.
parent: principles-in-practice
order: 50
labels: principle, sre, risk, error-budget, tiers
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
state: partial
source: [Pillar 1, error budgets](doc:sre/error-budgets-as-reliability-currency); [Google SRE book ch. 3](https://sre.google/sre-book/embracing-risk/)
---
## The principle

Each extra nine of reliability costs more than the one before, and past a point users cannot tell the difference, because their own network and device fail more often. So the target is set below 100%, and the difference is an error budget: the failure a service may have in a window while releases and experiments go on. While budget remains, changes ship; when it is spent, the work moves to reliability. Product and operations then argue over one number.

Source: [Error Budgets as Reliability Currency](doc:sre/error-budgets-as-reliability-currency) under [Reliability](doc:sre/reliability); Google's [Embracing Risk](https://sre.google/sre-book/embracing-risk/) and the [example error budget policy](https://sre.google/workbook/error-budget-policy/) in the workbook.

## On this platform

- **Tiers set how much risk a service may carry.** The [catalog](/inside/services/) puts each service in one of three tiers. Tier 1 is what readers meet or what decides a deploy, and is first in line; tier 2 is fixed the same day; tier 3 waits for the next working session ([Service catalog](doc:eng/service-catalog)).
- **One service has a budget.** The [Local LLM](/inside/services/local-llm/) has two SLOs, 99% availability and 95% of streamed requests with a first token within 4 s. Multi-window burn-rate alerts fire when errors use the budget 14.4 times (page) or 6 times (ticket) faster than the 30-day window allows ([Alerts and SLOs](doc:obs/alerts-and-slos)).
- **A budget sized to the traffic.** The model server answers a few requests an hour, so one failed request in a quiet hour is a 100% error ratio. The availability alerts carry a traffic floor, so one failure does not page.
- **No budget for bad pages.** The gate blocks the deploy on any blocking finding. A blocked deploy costs minutes; a wrong page in front of readers costs their trust. The record of 2026-10-08 shows the trade: 81 seconds of delay and no reader impact ([incident record](/inside/status/#2026-10-08-gate-blocked-map-push)).

## State

**Partial.** Tiers and one error budget exist. Three parts are missing: a policy that says what happens when the Local LLM spends its budget ([#38](https://github.com/uncovertechtalent/machinebehavior.io/issues/38)); budgets for the tier-1 services, which have no SLOs ([Service level objectives](doc:sre/principle-service-level-objectives)); and a dashboard panel with the budget left, which `grafana/build.py` does not define today.

## Services that name it

<!-- principle-services -->

## In a company of 10 to 200 people

- Agree the target with the product owner, in writing, and set it from what customers notice, below what the system does today.
- Write the error budget policy before the first budget runs out: who decides, what stops, what restarts it, and who settles a disagreement.
- Show the budget left next to the release calendar, so the team sees the trade before it ships.
- Use tiers to say which services may fail cheaply. Most internal tools need a lower target than the product.

## Open work

- [#38 Error budget policy: what happens when a service spends its budget](https://github.com/uncovertechtalent/machinebehavior.io/issues/38)
- [#37 SLOs for the tier-1 services and the agent sessions](https://github.com/uncovertechtalent/machinebehavior.io/issues/37)
