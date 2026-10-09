title: Counter resets from parallel sessions
summary: Why Claude Code's cost counters in Prometheus report spend in the millions of USD, and how the stack reads spend and tokens from per-request events in Loki.
parent: runbooks
order: 30
labels: runbook, prometheus, loki, claude-code
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: how-to
---
Claude Code spend computed with `increase()` over its Prometheus cost counter reports millions of USD. In the week to 2026-10-09, `increase()` reported USD 1.97M, while the API calls cost USD 76 in the last 24 hours of that week.

## Cause

Claude Code exports cumulative counters with no per-process attribute. It sets no `service.instance.id`, and `OTEL_METRICS_INCLUDE_SESSION_ID=false` in [client/claude-code.env](https://github.com/uncovertechtalent/agent-observability/blob/main/client/claude-code.env) removes the session ID. The desktop app runs several Claude Code processes at once (up to about 12 in that week), and all of them write the same Prometheus series. Each interleaved export reads as a counter reset: `resets()` counted 230,328 in the week. Prometheus also dropped 235 batches that carried two values for one timestamp.

## Check

Count the resets of the cost counter over a week:

```promql
sum(resets({__name__=~"claude_code_cost.*"}[7d]))
```

Then compare with the Loki sum of the same week, which matches the real spend:

```logql
sum(sum_over_time({service_name=~"claude-code.*"} | event_name="api_request" | keep cost_usd | unwrap cost_usd [7d]))
```

## Fix in place

Spend and tokens come from the `api_request` events in Loki. Claude Code writes one per API call with its cost and four token counts, so the sum is exact. Over a week the event sums matched the local session transcripts within 0.1% for the main model, and they include side calls the transcripts leave out: prompt suggestions, compaction and web fetch.

- `request_sum()` in [grafana/build.py](https://github.com/uncovertechtalent/agent-observability/blob/main/grafana/build.py) builds every spend and token query. A `keep` stage before `unwrap` drops `request_id` and `trace_id`, so the sum does not split into one series per request.
- The Loki ruler records `model:claude_code_cost_usd:sum1h` and remote-writes it to Prometheus for the `ClaudeCodeSpendSpike` alert.
- The counters still arrive in Prometheus. No dashboard or rule sums them.

## Why not a per-process label

A per-process label would stop the resets at a cost of about 600 extra series a day, some 54,000 at 90-day retention. The counters would still be inexact. Each process's series starts at its first non-zero value, and Prometheus 3.5 does not turn the OTLP start time into a zero sample (tested with `created-timestamp-zero-ingestion`). So `increase()` would lose each process's first export and count a process that exports once as zero.

## Apply the same fix elsewhere

For any counter that parallel processes write without a per-process label, sum a per-event log field in Loki for the dashboard. For an alert, record the sum with the Loki ruler and remote-write it to Prometheus. The events and their fields: [Loki streams](doc:obs/loki-streams). The alert: [Alerts and SLOs](doc:obs/alerts-and-slos).
