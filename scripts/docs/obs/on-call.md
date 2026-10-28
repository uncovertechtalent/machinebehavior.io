title: On-call and escalation
summary: The on-call model as it runs: a PagerDuty-style pager on a private Discord server with a rotation, an escalation policy and a read-only responder agent; one Alertmanager for both Prometheus servers; every page and ticket as an issue on the board; an outside heartbeat on the alerting path; and the rotation, last pages and pager load from a public snapshot.
order: 15
created: 2026-10-09
updated: 2026-10-28
labels: on-call, alerts, alertmanager, pager, rotation, escalation, incidents, discord, heartbeat
owner: Stefan Coetzee
reviewed: 2026-10-17
review_by: 2027-01-15
type: explanation
---
A page reaches the person on call through a pager. One Alertmanager serves both Prometheus servers in the house, the agent-observability stack's and the NAS monitoring stack's. A `page` becomes an incident on a private Discord server, run the way PagerDuty runs one: a message with Acknowledge, Resolve and Escalate buttons, a thread for its timeline, a rotation that says who is on call, and an escalation policy for when nobody acknowledges. Every page and every `ticket` also opens an issue on the [board](/inside/board/); `info` goes nowhere. Each Prometheus carries an always-firing `Watchdog` that pings a heartbeat check outside the house, so a dead Prometheus no longer looks like a quiet night. The [deploy gate](doc:eng/conformity-gate) stays the one control that acts without a person.

## Rotation and the last pages

The tables below are a snapshot, as of the time in its last line: the rotation from [pager/rotation.yml](https://github.com/uncovertechtalent/agent-observability/blob/main/pager/rotation.yml), and the pages from the records the pager keeps on their board issues. The deploy job refreshes it; the page sends no request to GitHub. It shows names, alert names and times, never a Discord account or channel.

<!-- oncall-snapshot -->

## Roles

| Role | Who | What they do |
|---|---|---|
| Primary | The operator, 08:00 to 22:00 Berlin time | Acknowledges a page, owns the incident, decides, holds the credentials |
| Responder agent | The pager's responder layer, at all hours | Posts the alert's runbook link and a read-only diagnosis in the incident thread. Changes nothing and never acknowledges |
| Responder sessions | Claude Code sessions, one per track of work | Pick up an acknowledged incident from its board issue, follow the runbooks, fix through the gate, write the incident record |
| Gate owner | The legislation-track session | Owns the conformity checks; tier changes are the operator's decision |
| Control | The conformity gate | Blocks a failing deploy of the three sites without anyone on call |

There is one person, so there is one human layer. Nobody is woken at night: out of hours the responder agent takes the page at once, and the primary hears at 08:00 if the page is still open and unacknowledged.

## How a page runs

1. **It fires.** Alertmanager sends it to the pager, grouped by alert name and Prometheus. The pager opens an incident keyed by the alert's fingerprint: a message in the pages channel and a thread under it.
2. **The person on call is notified.** The thread mentions the primary. Without an acknowledgement, the mention repeats every 5 minutes, 3 times.
3. **It escalates.** At 15 minutes the responder layer runs: the runbook link and a diagnosis from read-only Prometheus queries (the alert's expression now, minutes firing in the last 24 hours, `up` of its job, the other alerts firing). The Escalate button reaches the next layer at once.
4. **Someone acknowledges.** Acknowledge stops the escalation; the message shows who and after how long.
5. **It resolves.** Alertmanager's resolve closes the incident. Resolve in the pager closes it too, and the rest of that firing episode stays quiet; a new episode pages again. An incident that hears nothing from Alertmanager for 2.5 hours closes as stale, since an alert that clears while inhibited or silenced sends no resolve.
6. **The record stays public.** The pager sends a redacted record of the page (times, names from the rotation) to the alert's board issue, which comments on acknowledge, responder and a person's resolve. The snapshot above reads these records.

Tickets do not page: each opens a board issue and a message in the tickets channel that links it.

## Routing

The configuration is [alertmanager.yml](https://github.com/uncovertechtalent/agent-observability/blob/main/alertmanager/alertmanager.yml). Each Prometheus names itself on every alert with an external label, `prometheus="agent-observability"` or `prometheus="nas"`, and signs in with its own user: every Alertmanager endpoint needs basic auth, because an alert posted to it can end up as a public issue.

| Alert | Receiver | Repeats |
|---|---|---|
| `Watchdog` | the outside heartbeat check of the Prometheus that sent it | every 5 minutes |
| `PagerDown`, `PagerDisconnected`, `PagerFailing`, `AlertmanagerNotificationsFailing` | the alerting-path channel by webhook, and the board: never through the pager | hourly |
| `AWSCostForecastOverBudget`, `AWSCostMonthToDateOver80`, `AWSCostDailySpike` | nowhere: the AWS spend rules stay a dashboard showcase | |
| `severity="info"` | nowhere | |
| `severity="page"` | the pager, and the board | hourly; the pager only refreshes the open incident |
| `severity="ticket"` | the board, and the tickets channel | daily; the issue body refreshes, no comment |

Inhibition keeps one cause to one alert, within the same Prometheus: `OllamaDown` silences `LocalLLM.+`, `ModelSpilledToCPU` and `OllamaExporterDown`; `SearXNGDown` silences the other SearXNG alerts; `PagerDown` silences `PagerDisconnected`.

**What a board issue shows.** This repository is public, so the ticket receiver `alert-issues` writes the alert name, the summary annotation, the start and end time, an allowlist of labels and the pager record. The description, the instance address and the link back to Prometheus stay out; every shown value loses URLs and IP addresses, and cannot mention a person or link an issue. One issue belongs to one alert fingerprint: a repeat refreshes the body, a resolve comments and closes, a new firing episode reopens it, and an issue that hears nothing for 25 hours closes with a comment. An issue the operator closed stays closed until the alert fires again.

## Rotation and policy

[pager/rotation.yml](https://github.com/uncovertechtalent/agent-observability/blob/main/pager/rotation.yml) uses PagerDuty's model:

- **Schedules with layers.** A layer has members, a turn length and a handoff time, and may be restricted to days and hours; a shift past midnight belongs to the day it starts. A later layer wins over an earlier one.
- **Overrides** win over every layer, from the file or from `/pager override` on the server.
- **An escalation policy** walks its rules in order of delay. A level with nobody on call passes the page on at once.

`/oncall` on the server shows the same as the snapshot. The Discord accounts behind the names are linked on the server with `/pager iam`, so no ID is written down anywhere.

## Watching the alerting path

Nothing inside the house can report that the house is down, so the last check sits outside. Tested on 2026-10-17: with the agent-observability Watchdog silenced at 17:55, its outside check went down at 18:02:08 and the alarm e-mail arrived the same minute. Each Prometheus's `Watchdog` pings its own check every 5 minutes; a check that gets no ping for 5 minutes past its period alarms by e-mail and in the alerting-path channel, from outside. A stopped Prometheus, Alertmanager, home server or uplink all stop the pings. Inside, the pager cannot report its own outage either, so `PagerDown`, `PagerDisconnected` and `PagerFailing` (a Discord call that failed for an incident) go past it by webhook, and so does a notification Alertmanager gave up on.

`scripts/check-alerting.sh` in the stack's repository checks it all without sending anything: promtool on the Prometheus config and every rule test, amtool on the Alertmanager config and its routing tree, every alert rule's severity against the receivers it promises, and the unit tests of the ticket receiver and the pager.

## The alert rules

| Group | Rules | Severity |
|---|---|---|
| Local LLM SLOs | LocalLLMAvailabilityBudgetBurnFast, LocalLLMLatencyBudgetBurnFast, LocalLLMAvailabilityBudgetBurnSlow | page, page, ticket |
| Local LLM symptoms | OllamaDown, OllamaExporterDown, ModelSpilledToCPU | page, page, info |
| Claude Code spend | ClaudeCodeSpendSpike | ticket |
| SearXNG | SearXNGDown, SearXNGProxyEgressDown, SearXNGTunnelDown, SearXNGEngineFailing, SearXNGDegradedSearches, SearXNGSlowSearches | page, then five ticket |
| AWS cost | AWSCostForecastOverBudget, AWSCostMonthToDateOver80, AWSCostDailySpike, AWSCostExporterStale | ticket; the three spend rules not delivered |
| Alerting path | Watchdog, PagerDown, PagerDisconnected, PagerFailing, AlertmanagerNotificationsFailing | heartbeat, page, page, page, ticket |
| UniFi gateway (NAS Prometheus) | UCGMaxLowAvailableMemory, UCGMaxMetricsMissing, UCGMaxPollerScrapeFailing, and its own Watchdog | ticket, heartbeat |

Across both servers: 8 page rules, 15 ticket rules (3 of them the AWS spend showcase), 1 info rule and 2 Watchdogs. Outside the stack, the AWS monthly budget in AWS Budgets sends an e-mail at 80% of actual spend ([Budgets and alerts](doc:fin/budgets-and-alerts)). Conditions and tests: [Alerts and SLOs](doc:obs/alerts-and-slos).

## Response

1. Acknowledge in the pager, then start from the incident thread and its board issue. For anything readers saw, open a record in `incidents/` with an `investigating` update and push; the status page shows it after the deploy. See [Status page](doc:eng/status-page).
2. Find the service in the [catalog](/inside/services/) and follow its runbook; the responder's link points there.
3. Fix through the gate. A fix that cannot pass the gate does not go out.
4. Move the record through identified, monitoring and resolved. The incident and its board issue close when the alert resolves.
5. For anything readers saw, write the cause and the fix into the docs and link it from the record.

Order of work follows the service tier: tier 1 first, tier 2 the same day, tier 3 in the next working session.

## Escalation outside the pager

| From | To | When |
|---|---|---|
| Responder session | The operator, in the session | Anything outside the session's track, anything that needs a credential, a cost, a change to the gate or a public statement |
| Operator | The gate owner | A false positive or a rule change in the gate |
| Operator | The provider | GitHub for Pages, Actions and the board, Discord for the pager, the heartbeat service, Anthropic for the API, the upstream search engines for blocks |

## What changed from the proposal

The routing proposed here on 2026-10-09 ([ADR-0017](doc:eng/adr-0017-on-call-model)) was wired on 2026-10-17 ([#36](https://github.com/uncovertechtalent/machinebehavior.io/issues/36), [ADR-0037](doc:eng/adr-0037-alert-routing-discord-board-heartbeat)). Five points differ:

- **A pager instead of a push.** Pages go to a pager service with a rotation, an escalation policy, buttons and a timeline, in place of a plain push in waking hours.
- **An agent layer.** The responder agent is the second level of the policy, and the first out of hours.
- **Every page is also a ticket**, day and night, so each page leaves an issue with its history and its public record.
- **The three AWS spend rules are not delivered.** `AWSCostExporterStale`, which reports a broken exporter, is a ticket.
- **Both Prometheus servers use the one Alertmanager**, each with its own Watchdog and heartbeat check, behind basic auth.

## Related

- [Alerts and SLOs](doc:obs/alerts-and-slos): every rule and its condition.
- [Runbooks](doc:obs/runbooks) and the [Engineering runbooks](doc:eng/runbooks).
- [Access model](doc:eng/access-model): who can reach what.
- [Someone carries the pager](doc:sre/principle-standby): the SRE principle this page answers.
