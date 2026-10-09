title: Monitor symptoms, page on user pain
summary: Monitoring should say what is broken for users before it says why, and a page should reach a person only when they must act. Here burn-rate and degraded-search alerts read what users get, five dashboards are public, and no alert is delivered.
parent: principles-in-practice
order: 70
labels: principle, sre, monitoring, alerting, observability
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
state: partial
source: [Pillar 3, symptoms over causes](doc:sre/symptoms-over-causes-for-alerting); [Google SRE book ch. 6](https://sre.google/sre-book/monitoring-distributed-systems/)
---
## The principle

Watch the four golden signals of each user-facing service: latency, traffic, errors and saturation. Alert on symptoms, what users get, and keep causes for dashboards and tickets, because one cause can show as many symptoms and many causes never reach a user. Every page must be urgent, actionable and new to the person who gets it. Black-box checks from outside show what users see now; white-box metrics from inside show what is about to break.

Source: [Symptoms over Causes for Alerting](doc:sre/symptoms-over-causes-for-alerting) under [Observability](doc:sre/observability); Google's [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) and [Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/).

## On this platform

- **Symptom alerts where an SLI exists.** The three Local LLM burn-rate alerts read the error ratio and the slow-first-token ratio that callers get. `SearXNGDegradedSearches` fires when the search script returned a degraded result 3 or more times in 15 minutes, and `SearXNGSlowSearches` when search latency p95 stays above 8 s ([Alerts and SLOs](doc:obs/alerts-and-slos)).
- **Most cause alerts are tickets.** Tunnel, proxy, engine and cost-exporter failures are tickets. Three cause alerts carry severity page: `OllamaDown`, `OllamaExporterDown` and `SearXNGDown`. The proposed routing would silence the SLO burns behind a down Ollama, so one cause raises one alert ([On-call and escalation](doc:obs/on-call)).
- **White-box telemetry.** The [observability stack](/inside/services/observability-stack/) runs Prometheus, Loki, Tempo and Grafana, fed by exporters for the model server and the deploy pipeline ([Architecture](doc:obs/architecture)), the search instance ([Alerts and SLOs](doc:obs/alerts-and-slos)) and AWS cost ([Budgets and alerts](doc:fin/budgets-and-alerts)). Five dashboards are public ([Public dashboards](doc:obs/public-dashboards)), among them [Website deploys](https://grafana.scoetzee.de/public-dashboards/e0f6a0c8f3a64884a67faac5cf4c3ad4).
- **Absence is not zero.** The SearXNG exporter pushes from a laptop, so a sleeping laptop leaves a gap in the series. The SearXNG rules read pushed values or failure ratios with a minimum number of calls, and none reads `up` or `absent()`.
- **A meter that was wrong.** Claude Code's cost counters reset each time a parallel session exported a lower total, and Prometheus summed the resets into USD 1.97M for a week of USD 1,003. The spend alert was in firing state 73% of the time on a false signal. Spend is now summed from per-request events ([incident record](/inside/status/#2026-10-09-phantom-spend-counters), [Counter resets from parallel sessions](doc:obs/runbook-counter-resets-parallel-sessions)).
- **The reader's view.** The [status page](/inside/status/) shows each service from the published records, with open and past incidents.

## State

**Partial.** Two services have symptom alerts and the telemetry is wide. Three parts are missing. No alert is delivered to anyone ([#36](https://github.com/uncovertechtalent/machinebehavior.io/issues/36)). No black-box probe checks the three sites from outside, so the most visible services have no symptom signal of their own ([#37](https://github.com/uncovertechtalent/machinebehavior.io/issues/37)). And the incident records do not say how each incident was detected; apart from the deploy the gate blocked, all were found by someone working at the time ([#41](https://github.com/uncovertechtalent/machinebehavior.io/issues/41)).

## Services that name it

<!-- principle-services -->

## In a company of 10 to 200 people

- Give each user-facing service the four golden signals on one dashboard, and one black-box probe from outside your own network.
- Page on symptoms tied to an SLO; send causes to tickets and dashboards.
- Review every page after the fact: was it urgent, was it actionable, was it new? Delete or demote the rules that fail.
- Test the alert rules like code, and alert on the alerting path itself.

## Open work

- [#36 Alert routing](https://github.com/uncovertechtalent/machinebehavior.io/issues/36)
- [#37 SLOs for the tier-1 services and the agent sessions](https://github.com/uncovertechtalent/machinebehavior.io/issues/37)
- [#41 Incident records: when and how each incident was detected](https://github.com/uncovertechtalent/machinebehavior.io/issues/41)
- [#29 Cost counters: drop them or alert on their resets](https://github.com/uncovertechtalent/machinebehavior.io/issues/29)
