title: Service level objectives
summary: An SLO is a target for a measured indicator of what users get, and the basis for alerts and error budgets. Here one of twelve services has SLOs, the Local LLM; the five tier-1 services, which readers meet directly, have none.
parent: principles-in-practice
order: 60
labels: principle, sre, slo, sli, reliability
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
state: gap
source: [Pillar 1, reliability](doc:sre/reliability); [Google SRE book ch. 4](https://sre.google/sre-book/service-level-objectives/)
---
## The principle

Pick a few indicators that describe what users get from a service (the share of requests that succeed, the share answered fast enough), measure them as ratios of good events to all events, and set a target for each over a window. The target is the SLO; an SLA adds a consequence for missing it and is set looser than the SLO. Without SLOs there is no error budget, and alerts fall back on causes in place of user pain. Scalability and performance are the same discipline in the capacity and latency dimensions.

Source: [Reliability](doc:sre/reliability), the first of the [ten pillars](doc:sre/pillars); Google's [Service Level Objectives](https://sre.google/sre-book/service-level-objectives/) and [Implementing SLOs](https://sre.google/workbook/implementing-slos/).

## On this platform

- **The worked example.** The [Local LLM](/inside/services/local-llm/) has two SLOs with their good events written out: availability 99% (a request without an upstream error) and latency 95% (a streamed chat request with a first token within 4 s). Recording rules compute both ratios over 5 minutes, 30 minutes, 1 hour and 6 hours, and burn-rate alerts read them ([Alerts and SLOs](doc:obs/alerts-and-slos)). The [public dashboard](https://grafana.scoetzee.de/public-dashboards/e6a9dd2153004ad0a868ce6f0e19071f) shows the requests, errors and time to first token behind them.
- **The rest of the catalog.** The other eleven service pages say "None defined" under Service level objectives, and their health comes from the records on the [status page](/inside/status/): the gate record for the sites, the deploy feed for the deploy job, incident files for the rest.
- **Data that exists for SLIs.** The [deploy exporter](/inside/services/deploy-exporter/) records every Actions run with its steps and gate checks, enough for a deploy SLO. Per-request Claude Code events in Loki carry model, tokens and cost, enough for an agent spend SLO ([Cost model](doc:fin/cost-model)). The SearXNG exporter records search latency and degraded results ([incident record](/inside/status/#2026-10-09-searxng-engine-suspensions)).

## State

**Gap.** One of twelve services has SLOs, and it is a tier-3 research tool. The three sites, the gate and the deploy job have none, so nobody can say how reliable they were last month. The sites also lack the probe an availability SLI needs: the map crawl in the deploy job fetches every page on each deploy, but nothing requests them every minute and records the answers. The issue lists candidate indicators to check against the data before any target is set ([#37](https://github.com/uncovertechtalent/machinebehavior.io/issues/37)).

## Services that name it

<!-- principle-services -->

## In a company of 10 to 200 people

- Start with the one or two user journeys that pay the bills, one availability and one latency SLI each, measured as close to the user as you can.
- Set the first target from a month of data, a little below what the system already does, and tighten it only when users ask.
- Put the SLO in the service catalog next to the owner, so every service page answers "how reliable is it supposed to be?".
- Review the SLOs each quarter with the product owner; drop an SLO nobody acts on.

## Open work

- [#37 SLOs for the tier-1 services and the agent sessions](https://github.com/uncovertechtalent/machinebehavior.io/issues/37)
- [#38 Error budget policy](https://github.com/uncovertechtalent/machinebehavior.io/issues/38)
