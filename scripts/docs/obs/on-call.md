title: On-call and escalation
summary: The real on-call model: one operator, agent sessions as responders, the deploy gate as the one control that acts on its own, and 13 alert rules that page nobody because no Alertmanager runs. With a proposed routing.
order: 15
labels: on-call, alerts, alertmanager, escalation, incidents
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
Nothing pages anyone. Prometheus evaluates 13 alert rules, but the stack runs no Alertmanager and Prometheus has no `alerting` target, so a firing alert stays in Prometheus and Grafana until someone looks. One person answers for every service, and the agent sessions that build the platform are the responders. The one control that acts without a person is the [deploy gate](doc:eng/conformity-gate): a failed check stops the deploy and the previous build stays live.

## Roles

| Role | Who | What they do |
|---|---|---|
| Operator | Stefan Coetzee | Owns every service in the [catalog](/inside/services/), decides, starts and stops agent sessions, holds the credentials |
| Responders | Claude Code sessions, one per track of work | Read the records and dashboards, follow the runbooks, fix within their track, push through the gate, write the incident record |
| Gate owner | The legislation-track session | Owns the conformity checks; tier changes are the operator's decision |
| Control | The conformity gate | Runs before every deploy of the three sites; blocks on a failed check without anyone on call |

A responder session works only while the operator has it running. There is no rotation, no second person and no response time agreed with anyone.

## How a problem is noticed today

1. **The gate fails.** The deploy does not run, the run is red on GitHub Actions, the [status page](/inside/status/) shows the site as degraded and the [Website deploys](https://grafana.scoetzee.de/public-dashboards/e0f6a0c8f3a64884a67faac5cf4c3ad4) dashboard shows the failing check. Readers keep the previous build.
2. **An alert fires.** It shows in Prometheus and on the internal Grafana dashboards. Nobody is told.
3. **A session or the operator sees it** while working: a dashboard, a failed search, a wrong number.
4. **A reader reports it** as a [GitHub issue](https://github.com/uncovertechtalent/machinebehavior.io/issues); it reaches the [board](/inside/board/) after triage.

The four incidents on the status page were all found by the third route.

## The alert rules

| Group | Rules | Severity |
|---|---|---|
| Local LLM SLOs | LocalLLMAvailabilityBudgetBurnFast, LocalLLMLatencyBudgetBurnFast, LocalLLMAvailabilityBudgetBurnSlow | page, page, ticket |
| Local LLM symptoms | OllamaDown, OllamaExporterDown, ModelSpilledToCPU | page, page, info |
| Claude Code spend | ClaudeCodeSpendSpike | ticket |
| SearXNG | SearXNGDown, SearXNGProxyEgressDown, SearXNGTunnelDown, SearXNGEngineFailing, SearXNGDegradedSearches, SearXNGSlowSearches | page, then five ticket |

Five rules carry `severity: page`, seven `ticket` and one `info`. Conditions and tests: [Alerts and SLOs](doc:obs/alerts-and-slos).

## Response

1. Open a record in `incidents/` with an `investigating` update and push; the status page shows it after the deploy. See [Status page](doc:eng/status-page).
2. Find the service in the [catalog](/inside/services/) and follow its runbook.
3. Fix through the gate. A fix that cannot pass the gate does not go out.
4. Move the record through identified, monitoring and resolved.
5. For anything readers saw, write the cause and the fix into the docs and link it from the record.

Order of work follows the service tier: tier 1 first, tier 2 the same day, tier 3 in the next working session.

## Escalation

| From | To | When |
|---|---|---|
| Responder session | The operator, in the session | Anything outside the session's track, anything that needs a credential, a cost, a change to the gate or a public statement |
| Operator | The gate owner | A false positive or a rule change in the gate |
| Operator | The provider | GitHub for Pages and Actions, Anthropic for the API, the upstream search engines for blocks |

## Proposed routing

This is a proposal and is not wired. Sending a page to a phone or an address needs the operator's go and a receiver the operator chooses.

```yaml
# alertmanager.yml (proposal)
route:
  receiver: board            # default: a ticket on the board
  group_by: [alertname]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 24h
  routes:
    - matchers: [severity="page"]
      receiver: operator-push
      repeat_interval: 1h
      active_time_intervals: [waking-hours]
    - matchers: [severity="page"]   # outside waking hours a page becomes a ticket
      receiver: board
    - matchers: [severity="info"]
      receiver: blackhole
    - matchers: [alertname="Watchdog"]
      receiver: heartbeat
      repeat_interval: 5m
inhibit_rules:
  - source_matchers: [alertname="OllamaDown"]
    target_matchers: [alertname=~"LocalLLM.+|ModelSpilledToCPU|OllamaExporterDown"]
  - source_matchers: [alertname="SearXNGDown"]
    target_matchers: [alertname=~"SearXNG.+"]
time_intervals:
  - name: waking-hours
    time_intervals:
      - times: [{start_time: "08:00", end_time: "22:00"}]
        location: Europe/Berlin
receivers:
  - name: operator-push      # a push service on the operator's phone; not chosen
  - name: board              # a webhook that opens or updates a GitHub issue with type and area labels
  - name: heartbeat          # an external check that alarms when the Watchdog stops arriving
  - name: blackhole
```

What it would change:

- The five page rules reach a person during waking hours; at night they wait as tickets, which matches one operator.
- Tickets land on the board as issues, so an alert has an owner and a history next to the other work.
- An always-firing `Watchdog` rule and an outside heartbeat check would show when the alerting path itself is down. Without it, a dead Prometheus and a quiet night look the same.
- Inhibition keeps one cause from raising five alerts: a down Ollama silences the SLO burns behind it.

Wiring it needs an Alertmanager service in the compose file, an `alerting` block in `prometheus.yml`, a `Watchdog` rule, promtool tests for the routes, and the operator's choice of receivers.

## Related

- [Alerts and SLOs](doc:obs/alerts-and-slos): every rule and its condition.
- [Runbooks](doc:obs/runbooks) and the [Engineering runbooks](doc:eng/runbooks).
- [Access model](doc:eng/access-model): who can reach what.
