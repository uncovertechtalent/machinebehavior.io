title: Budgets and alerts
summary: The cost controls that exist (the Claude Code spend alert, the AWS monthly budget with its internal dashboard and four alert rules, the eval harness caps), why only the AWS Budgets e-mail reaches a person, and what a budget alert for Claude Code would look like.
order: 50
labels: finops, budgets, alerts, prometheus, loki
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: reference
---
Two kinds of cost control exist. For Claude Code, `ClaudeCodeSpendSpike` fires when the list-price value of calls in the trailing hour stays above USD 40 for 10 minutes; until 2026-10-09 the threshold was USD 20. For the AWS account, a monthly cost budget in AWS Budgets e-mails at 80% of actual spend, and since 2026-10-09 an internal dashboard and four Prometheus rules compare spend and forecast with that budget. The stack runs no Alertmanager, so the Prometheus alerts are visible in Prometheus and Grafana and reach nobody; the AWS Budgets e-mail is the one cost notification that reaches a person. Claude Code has no budget, and the eval harness caps each run.

## What exists

| Control | Where | What it does | State on 2026-10-09 |
|---|---|---|---|
| `ClaudeCodeSpendSpike` | [prometheus/rules/alerts.yml](https://github.com/uncovertechtalent/agent-observability/blob/main/prometheus/rules/alerts.yml) | `sum(model:claude_code_cost_usd:sum1h) > 40` for 10 minutes, severity ticket | Evaluated; no notification route |
| `model:claude_code_cost_usd:sum1h` | [loki/rules/fake/claude-code.yml](https://github.com/uncovertechtalent/agent-observability/blob/main/loki/rules/fake/claude-code.yml) | Trailing-hour sum of `cost_usd` by model, every minute, written to Prometheus by the Loki ruler | Recording |
| Alert tests | [prometheus/tests/alerts_test.yml](https://github.com/uncovertechtalent/agent-observability/blob/main/prometheus/tests/alerts_test.yml) | The spend alert fires at USD 45 per hour, holds at USD 35 and holds on 8 minutes above the threshold; each AWS rule has a case above and a case below its threshold | In the repository; pass with promtool on 2026-10-09 |
| Eval run cap | Experiment 04 harness, `--budget-usd` | Starts no new conversation once the projected spend would cross the cap | v5 cap USD 20, spent USD 12.87 |
| Probe cap | [Weekly decision-layer probe](doc:res/decision-layer-probe) | Same guard, cap USD 1.0 | First run USD 0.269 |
| AWS monthly budget | AWS Budgets, in the account | Monthly cost budget on unblended cost, tax, credits and refunds included; e-mail when actual spend passes 80% | Active; the amount is not published |
| AWS spend dashboard | Grafana, uid `aws-spend`, internal | Month to date and forecast against the budget, daily cost by service, top services, the last three months, the budget table and the exporter's own API cost | Live since 2026-10-09; never shared |
| `AWSCostForecastOverBudget` | [alerts.yml](https://github.com/uncovertechtalent/agent-observability/blob/main/prometheus/rules/alerts.yml), group `aws_cost` | `max(aws_cost_month_forecast_usd) > max(aws_budget_limit_usd{period="MONTHLY"})` for 1 hour, severity ticket | Evaluated; no notification route |
| `AWSCostMonthToDateOver80` | same | `max(aws_cost_mtd_usd) > 0.8 * max(aws_budget_limit_usd{period="MONTHLY"})` for 1 hour, severity ticket | Evaluated; no notification route |
| `AWSCostDailySpike` | same | The latest day before today above twice the median of the 28 days before it and above USD 1, domain renewals and tax left out of both, for 1 hour | Evaluated; no notification route |
| `AWSCostExporterStale` | same | No error-free poll for 13 hours, or a running exporter that has never fetched | Evaluated; no notification route |

`alerts.yml` holds 17 alert rules: the Claude Code spend alert, the four AWS rules and 12 for the local LLM, Ollama and SearXNG ([Alerts and SLOs](doc:obs/alerts-and-slos)).

## AWS spend, internal

`aws-cost-exporter` in the [agent-observability](https://github.com/uncovertechtalent/agent-observability) stack reads the AWS account's daily `UnblendedCost` by service from Cost Explorer (this month and the three before), Cost Explorer's forecast to the end of the month and every budget in AWS Budgets. The budget rules take the amount from AWS Budgets, so a change to the budget there moves the thresholds without a rule change.

- Cost of the meter. Cost Explorer bills USD 0.01 per request. The exporter caches every answer and asks for this month every 12 hours, the forecast daily and older months weekly, about USD 1 a month. The dashboard shows the exporter's own requests and their cost.
- Lag. Cost Explorer data trails by up to a day and marks the current month as estimated, so the daily spike rule reads the latest day before today, which can still be partial.
- One-day charges. Domain renewals and the monthly tax post as single-day spikes. The spike rule leaves both out of the latest day and of the median; the budget rules include them, as AWS Budgets does.
- Two forecasts. The dashboard shows Cost Explorer's forecast and AWS Budgets' own forecast side by side; the two models can differ by a wide margin early in a month.
- Credentials. The exporter reads the AWS shared config on the home server through a read-only mount and publishes no port; only Prometheus scrapes it.

Amounts on the dashboard stay unpublished unless the owner releases them.

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
