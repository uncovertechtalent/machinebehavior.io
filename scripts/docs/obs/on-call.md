title: On-call and escalation
summary: The on-call model as it runs: one operator, agent sessions as responders, the deploy gate as the one control that acts on its own, and one Alertmanager for both Prometheus servers that sends a page to Discord in waking hours, opens an issue on the board for every page and ticket, and pings an outside heartbeat check so a dead alerting path shows.
order: 15
labels: on-call, alerts, alertmanager, escalation, incidents, discord, heartbeat
owner: Stefan Coetzee
reviewed: 2026-10-17
review_by: 2027-01-15
type: explanation
---
Alerts reach a person. One Alertmanager serves both Prometheus servers in the house: the agent-observability stack's and the NAS monitoring stack's. A `page` goes to Discord between 08:00 and 22:00 Berlin time and opens an issue on the [board](/inside/board/) at any hour; a `ticket` opens an issue; `info` goes nowhere. Each Prometheus also carries an always-firing `Watchdog` that pings a heartbeat check outside the house every 5 minutes, and the check alarms when the pings stop, so a dead Prometheus no longer looks like a quiet night. One person answers for every service, the agent sessions that build the platform are the responders, and the [deploy gate](doc:eng/conformity-gate) stays the one control that acts without a person: a failed check stops the deploy and the previous build stays live.

## Roles

| Role | Who | What they do |
|---|---|---|
| Operator | Stefan Coetzee | Owns every service in the [catalog](/inside/services/), receives the pages, decides, starts and stops agent sessions, holds the credentials |
| Responders | Claude Code sessions, one per track of work | Read the alert issue, the records and dashboards, follow the runbooks, fix within their track, push through the gate, write the incident record |
| Gate owner | The legislation-track session | Owns the conformity checks; tier changes are the operator's decision |
| Control | The conformity gate | Runs before every deploy of the three sites; blocks on a failed check without anyone on call |

A responder session works only while the operator has it running. There is no rotation, no second person and no response time agreed with anyone. At night a page waits on the board; nobody is woken.

## How a problem is noticed

1. **A page fires.** In waking hours a message arrives in the operator's Discord channel within about a minute, and an issue opens on the board. At night only the issue opens; if the alert still fires at 08:00, the Discord message follows then.
2. **A ticket fires.** An issue opens on the board, labelled `kind:finding` and an area. It closes itself when the alert resolves and reopens when the same alert fires again.
3. **The gate fails.** The deploy does not run, the run is red on GitHub Actions, the [status page](/inside/status/) shows the site as degraded and the [Website deploys](https://grafana.scoetzee.de/public-dashboards/e0f6a0c8f3a64884a67faac5cf4c3ad4) dashboard shows the failing check. Readers keep the previous build.
4. **The heartbeat stops.** The outside check alarms when no `Watchdog` ping has arrived for 10 minutes: Prometheus, Alertmanager, the home server or the uplink is down.
5. **A session or the operator sees it** while working: a dashboard, a failed search, a wrong number.
6. **A reader reports it** as a [GitHub issue](https://github.com/uncovertechtalent/machinebehavior.io/issues); it reaches the board after triage.

Before 2026-10-17 only routes 3, 5 and 6 existed. Of the four incidents then on the status page, the gate found one (the blocked deploy of 2026-10-08) and someone working at the time found the other three.

## Routing

The configuration is [alertmanager.yml](https://github.com/uncovertechtalent/agent-observability/blob/main/alertmanager/alertmanager.yml). Each Prometheus names itself on every alert with an external label, `prometheus="agent-observability"` or `prometheus="nas"`, and signs in with its own user: every Alertmanager endpoint needs basic auth, because an alert posted to it can end up as a public issue.

| Alert | Receiver | Repeats |
|---|---|---|
| `severity="page"` | Discord, 08:00 to 22:00 Europe/Berlin | every hour while it fires |
| `severity="page"` or `"ticket"` | `alert-issues`: one issue per alert on this repository | the issue body refreshes daily; no comment |
| `severity="info"` | nowhere | |
| `AWSCostForecastOverBudget`, `AWSCostMonthToDateOver80`, `AWSCostDailySpike` | nowhere: the AWS spend rules stay a dashboard showcase | |
| `Watchdog` | the outside heartbeat check of the Prometheus that sent it | every 5 minutes |
| anything else | `alert-issues` | daily |

Inhibition keeps one cause to one alert, within the same Prometheus: `OllamaDown` silences `LocalLLM.+`, `ModelSpilledToCPU` and `OllamaExporterDown`, and `SearXNGDown` silences the other SearXNG alerts.

**What an alert issue shows.** This repository is public, so `alert-issues` writes the alert name, the summary annotation, the start and end time and an allowlist of labels (severity, the Prometheus, job, component, and the name, engine, model or source a rule splits by). The description, the instance address and the link back to Prometheus stay out; every shown value loses URLs and IP addresses, and cannot mention a person or link an issue. One issue belongs to one alert fingerprint, the hash of the alert's labels: a repeat refreshes the body, a resolve comments and closes, and a new firing episode reopens the same issue with a comment. An issue the operator closed stays closed until the alert fires again.

## The alert rules

| Group | Rules | Severity |
|---|---|---|
| Local LLM SLOs | LocalLLMAvailabilityBudgetBurnFast, LocalLLMLatencyBudgetBurnFast, LocalLLMAvailabilityBudgetBurnSlow | page, page, ticket |
| Local LLM symptoms | OllamaDown, OllamaExporterDown, ModelSpilledToCPU | page, page, info |
| Claude Code spend | ClaudeCodeSpendSpike | ticket |
| SearXNG | SearXNGDown, SearXNGProxyEgressDown, SearXNGTunnelDown, SearXNGEngineFailing, SearXNGDegradedSearches, SearXNGSlowSearches | page, then five ticket |
| AWS cost | AWSCostForecastOverBudget, AWSCostMonthToDateOver80, AWSCostDailySpike, AWSCostExporterStale | ticket; the three spend rules not delivered |
| Alerting path | Watchdog, AlertmanagerNotificationsFailing | heartbeat, ticket |
| UniFi gateway (NAS Prometheus) | UCGMaxLowAvailableMemory, UCGMaxMetricsMissing, UCGMaxPollerScrapeFailing, and its own Watchdog | ticket, heartbeat |

Across both servers that is 5 page rules, 15 ticket rules (3 of them the AWS spend showcase), 1 info rule and 2 Watchdogs. Outside the stack, the AWS monthly budget in AWS Budgets still sends an e-mail at 80% of actual spend ([Budgets and alerts](doc:fin/budgets-and-alerts)). Conditions and tests: [Alerts and SLOs](doc:obs/alerts-and-slos).

## Watching the alerting path

Nothing inside the house can report that the house is down, so the check sits outside. Alertmanager sends each Prometheus's `Watchdog` to its own check every 5 minutes; a check that gets no ping for 5 minutes past its period alarms the operator from outside. A stopped Prometheus, a stopped Alertmanager, a dead home server and a dead uplink all stop the pings. `AlertmanagerNotificationsFailing` covers the other half: a notification Alertmanager gave up on after its retries, such as a broken Discord webhook, becomes a ticket.

`scripts/check-alerting.sh` in the stack's repository checks the setup without sending anything: promtool on the Prometheus config and every rule test, amtool on the Alertmanager config and its routing tree, every alert rule's severity against the receivers it promises, and the ticket receiver's unit tests.

## Response

1. Start from the alert issue. For anything readers saw, open a record in `incidents/` with an `investigating` update and push; the status page shows it after the deploy. See [Status page](doc:eng/status-page).
2. Find the service in the [catalog](/inside/services/) and follow its runbook.
3. Fix through the gate. A fix that cannot pass the gate does not go out.
4. Move the record through identified, monitoring and resolved. The alert issue closes on its own when the alert resolves.
5. For anything readers saw, write the cause and the fix into the docs and link it from the record.

Order of work follows the service tier: tier 1 first, tier 2 the same day, tier 3 in the next working session.

## Escalation

| From | To | When |
|---|---|---|
| Responder session | The operator, in the session | Anything outside the session's track, anything that needs a credential, a cost, a change to the gate or a public statement |
| Operator | The gate owner | A false positive or a rule change in the gate |
| Operator | The provider | GitHub for Pages, Actions and the board, Discord for the page channel, the heartbeat service, Anthropic for the API, the upstream search engines for blocks |

## What changed from the proposal

The routing proposed here on 2026-10-09 ([ADR-0017](doc:eng/adr-0017-on-call-model)) was wired on 2026-10-17 ([#36](https://github.com/uncovertechtalent/machinebehavior.io/issues/36), [ADR-0037](doc:eng/adr-0037-alert-routing-discord-board-heartbeat)), with four changes:

- **Discord is the push receiver**, through Alertmanager's own Discord integration and a channel webhook.
- **Every page is also a ticket**, day and night. The proposal turned a page into a ticket only outside waking hours. A ticket route muted by day would drop the resolved notice of a page that started at night and leave its issue open, and the proposal's night route came after a route that already matched, so it could never fire.
- **The three AWS spend rules are not delivered.** They show their state on the AWS spend dashboard, as before; `AWSCostExporterStale`, which reports a broken exporter, is a ticket.
- **Both Prometheus servers use the one Alertmanager**, each with its own Watchdog and heartbeat check.

## Related

- [Alerts and SLOs](doc:obs/alerts-and-slos): every rule and its condition.
- [Runbooks](doc:obs/runbooks) and the [Engineering runbooks](doc:eng/runbooks).
- [Access model](doc:eng/access-model): who can reach what.
- [Standby](doc:sre/principle-standby): the SRE principle this page answers.
