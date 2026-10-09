title: The phantom two million
summary: A FinOps anomaly case from 2026-10-09: parallel Claude Code sessions wrote into one counter series, and Prometheus reported USD 1.97M for a week that cost USD 1,003 at list price.
order: 40
labels: finops, anomaly, data-quality, case, claude-code
---
For the week to 2026-10-09 00:00 UTC, `increase()` over Claude Code's cost counter in Prometheus reported USD 1,970,946.62. The per-request events in Loki for the same seven days (2026-10-02 to 2026-10-08) sum to USD 1,003.45 at list price. The counter overstated spend by a factor of about 1,960. No money moved; the defect was in the meter.

## The case in FinOps terms

| Field | Value |
|---|---|
| Capability | Anomaly Management, domain Understand Usage & Cost |
| Principle at stake | FinOps data should be accessible, timely, and accurate |
| Kind | Data-quality anomaly in the meter |
| Found | 2026-10-09, during work on the Claude Code cost panels |
| Downstream effect | The cost panels and the spend alert read the faulty series |
| Resolution | Spend and tokens summed from per-request events in Loki |

## Timeline (UTC)

- 2026-10-01 15:21: first Claude Code event in Loki. From then on Claude Code wrote both the counters and the events.
- 2026-10-02 07:54: `ClaudeCodeSpendSpike` starts firing on the counter-based expression. Up to the fix it is in firing state for 7,691 of 10,533 minutes, 73% of the time (Prometheus `ALERTS` series).
- 2026-10-09 07:23: end of the verification window. In the 24 hours before it, `increase()` reports USD 2,096.72 and the Loki events sum to USD 74.45.
- 2026-10-09 07:29: the dashboards and the alert move to sums over the events ([agent-observability c163b42](https://github.com/uncovertechtalent/agent-observability/commit/c163b429a63c69cff49dcde533da45f4a2c2f206)).
- 2026-10-09 07:43 to 10:18: the fixed alert fires on real spend, with a peak of USD 56.7 in the trailing hour at 08:30 ([Budgets and alerts](doc:fin/budgets-and-alerts)).

## Cause

Claude Code exports cumulative cost counters with no attribute that tells one process from another. The desktop app ran up to about 12 Claude Code processes at once, and all of them wrote one Prometheus series. Every export from a process with a lower running total looks like a counter reset, and `increase()` adds the full value after each reset. `resets()` counted 230,328 resets in the week. The mechanics and the check queries are in the runbook [Counter resets from parallel sessions](doc:obs/runbook-counter-resets-parallel-sessions).

## Fix

Claude Code also writes one `api_request` event per API call, with its `cost_usd` and four token counts. A sum over those events is exact, and over a week it matched the local session transcripts within 0.1% for the main model ([README, cost and tokens from per-request events](https://github.com/uncovertechtalent/agent-observability#design-decisions)). `request_sum()` in [grafana/build.py](https://github.com/uncovertechtalent/agent-observability/blob/main/grafana/build.py) builds every spend and token query from the events. For the alert, the Loki ruler records the trailing-hour sum by model and writes it to Prometheus. The counters still arrive; no panel or rule sums them.

## Lessons for cost data

1. Reconcile a cost meter against a second record before it feeds a decision. The events were checked against the session transcripts; the counters never were.
2. Watch the meter as well as the spend. A rule on `resets()` of a cost counter separates a broken meter from a spending spike. On 2026-10-09 the reset count, 230,328 in a week, is the figure that shows the cause.
3. Prefer per-event sums when many unlabelled writers report one quantity. A counter needs one writer per series; parallel agent sessions break that rule by default.
4. An alert that fires 73% of the time carries no signal, and a reader learns to ignore the spend line.

## Figures and sources

| Figure | Value | Source |
|---|---|---|
| `increase()` over 7 days to 2026-10-09 00:00 UTC | USD 1,970,946.62 | Prometheus, `claude_code_cost_usage_USD_total` |
| `resets()` over the same 7 days | 230,328 | Prometheus |
| Events, 2026-10-02 to 2026-10-08 | USD 1,003.45 | Loki, `api_request` events |
| `increase()`, 24 hours to 2026-10-09 07:23 UTC | USD 2,096.72 | Prometheus |
| Events, same 24 hours | USD 74.45 | Loki |
| Alert in firing state before the fix | 7,691 of 10,533 minutes | Prometheus `ALERTS` |

All queried on 2026-10-09.
