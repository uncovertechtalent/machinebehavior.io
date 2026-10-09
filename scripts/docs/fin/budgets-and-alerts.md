title: Budgets and alerts
summary: The one cost alert that exists, why nothing pages, how it behaved on real spend on 2026-10-09, the budget caps in the eval harness, and what a budget alert for Claude Code would look like.
order: 50
labels: finops, budgets, alerts, prometheus, loki
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: reference
---
One alert watches cost: `ClaudeCodeSpendSpike`. It fires when the list-price value of Claude Code calls in the trailing hour stays above USD 40 for 10 minutes; until 2026-10-09 the threshold was USD 20. The stack runs no Alertmanager, so a firing alert is visible in Prometheus and Grafana and reaches nobody. No budget is set for any component; the eval harness caps each run.

## What exists

| Control | Where | What it does | State on 2026-10-09 |
|---|---|---|---|
| `ClaudeCodeSpendSpike` | [prometheus/rules/alerts.yml](https://github.com/uncovertechtalent/agent-observability/blob/main/prometheus/rules/alerts.yml) | `sum(model:claude_code_cost_usd:sum1h) > 40` for 10 minutes, severity ticket | Evaluated; no notification route |
| `model:claude_code_cost_usd:sum1h` | [loki/rules/fake/claude-code.yml](https://github.com/uncovertechtalent/agent-observability/blob/main/loki/rules/fake/claude-code.yml) | Trailing-hour sum of `cost_usd` by model, every minute, written to Prometheus by the Loki ruler | Recording |
| Alert tests | [prometheus/tests/alerts_test.yml](https://github.com/uncovertechtalent/agent-observability/blob/main/prometheus/tests/alerts_test.yml) | The spend alert fires at USD 45 per hour, holds at USD 35 and holds on 8 minutes above the threshold | In the repository; run with promtool |
| Eval run cap | Experiment 04 harness, `--budget-usd` | Starts no new conversation once the projected spend would cross the cap | v5 cap USD 20, spent USD 12.87 |
| Probe cap | [Weekly decision-layer probe](doc:res/decision-layer-probe) | Same guard, cap USD 1.0 | First run USD 0.269 |

`alerts.yml` holds 13 alert rules; the other 12 watch the local LLM, Ollama and SearXNG ([Alerts and SLOs](doc:obs/alerts-and-slos)). Account-level budgets at the cloud provider are outside this documentation.

## The spend alert on real spend

After the switch to per-request events ([The phantom two million](doc:fin/anomaly-the-phantom-two-million)), the alert, then at USD 20, fired on 2026-10-09 from 07:43 to 10:18 UTC. The trailing-hour value, in 15-minute samples:

| UTC | 07:30 | 08:00 | 08:30 | 09:00 | 09:30 | 10:00 | 10:30 |
|---|---|---|---|---|---|---|---|
| USD in the trailing hour | 18.2 | 33.1 | 56.7 | 52.7 | 44.2 | 34.3 | 18.5 |

Several Claude Code sessions ran in parallel that morning. In the week before (clock hours from 2026-10-02 to 2026-10-08, Loki), 69 of 168 hours had any spend, the median of those hours was USD 10.59, 16 hours were above USD 20 and the busiest hour reached USD 87.41. A USD 20 threshold sits below 16 of that week's clock hours.

The threshold moved to USD 40 the same day. Replayed on the trailing-hour series from 2026-10-02 to 2026-10-09 11:00 UTC in 5-minute steps, USD 20 fires 21 times and USD 40 fires four times:

| Firing (UTC) | Peak USD in the trailing hour |
|---|---|
| 2026-10-07 12:20 to 12:30 | 40.9 |
| 2026-10-07 18:15 to 18:40 | 44.6 |
| 2026-10-07 20:20 to 22:10 | 87.4 |
| 2026-10-09 08:20 to 09:45 | 56.8 |

Each is a busy hour with several sessions in parallel. USD 40 marks those hours and stays quiet through ordinary ones. A rule relative to recent hours, 1.5 times the 7-day 99th percentile of the trailing hour with a USD 30 floor, fires once in the same replay; it needs seven days of the Prometheus series, which starts on 2026-10-09.

## What a budget means on a subscription

On a flat plan a dollar budget limits nothing that is billed. It is a usage budget written in list-price dollars, a proxy for the share of the plan's limits that is used ([Showback](doc:fin/showback)). On API billing the same rules would track the bill directly.

## A budget alert for Claude Code (proposal, not deployed)

1. Delivery first. Add Alertmanager with one receiver that reaches a person, such as mail or a push service. Without it, none of the rules below reaches anyone.
2. Record a daily and a weekly sum with the Loki ruler, next to the hourly rule:

```yaml
# loki/rules/fake/claude-code.yml, proposal
- record: claude_code_cost_usd:sum24h
  expr: sum(sum_over_time({service_name=~"claude-code.*"} | event_name="api_request" | keep cost_usd | unwrap cost_usd [24h]))
- record: claude_code_cost_usd:sum7d   # in a group with interval: 1h; a 7-day range every minute is wasteful
  expr: sum(sum_over_time({service_name=~"claude-code.*"} | event_name="api_request" | keep cost_usd | unwrap cost_usd [7d]))
```

3. Keep the budget as a series, so the threshold lives in one place, and alert on the day and on a 30-day forecast from the last seven days:

```yaml
# prometheus/rules/alerts.yml, proposal
- record: budget:claude_code_cost_usd:per_day
  expr: vector(150)   # example: the mean day of 2026-10-02 to 2026-10-08 was USD 143.35
- alert: ClaudeCodeDailyBudget
  expr: claude_code_cost_usd:sum24h > on() 0.8 * budget:claude_code_cost_usd:per_day
  for: 15m
  labels: {severity: ticket}
- alert: ClaudeCodeMonthlyForecast
  expr: claude_code_cost_usd:sum7d / 7 * 30 > on() 30 * budget:claude_code_cost_usd:per_day
  for: 1h
  labels: {severity: ticket}
```

4. Watch the meter. A rule on `resets()` of a cost counter flags a broken meter. On this stack it would fire until the unused Claude Code counters are dropped in Alloy, because they still arrive and still reset.
5. Test each new rule with promtool, as the existing spend alert is tested: one case above the threshold, one below.

The owner sets the budget figure. The value 150 in the example stands in for that decision: it is the mean of the measured week, rounded up.
