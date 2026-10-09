title: Observability runbooks
summary: Step-by-step fixes for the known traps in the observability stack: missing backfill in Loki, empty stat panels, Claude Code counter resets and sharing a dashboard.
order: 60
labels: runbook, operations
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: reference
---
These runbooks cover the traps found while running the stack. Each one gives the symptom, the cause, a check and the fix. Commands run on the home server from the repository directory unless a step says otherwise.

| Runbook | Symptom |
|---|---|
| [Backfilled runs missing in Loki](doc:obs/runbook-loki-backfill-missing) | The Website deploys dashboard shows no history after the deploy-exporter starts with an empty state |
| [Stat panel shows No data](doc:obs/runbook-stat-panel-no-data) | A stat panel is empty over a long range while the metric exists |
| [Counter resets from parallel sessions](doc:obs/runbook-counter-resets-parallel-sessions) | Claude Code spend computed from Prometheus counters reads in the millions of USD |
| [Share a dashboard publicly](doc:obs/runbook-share-a-dashboard) | Task: publish a dashboard at grafana.scoetzee.de |

## First checks

These commands show whether each service runs and whether the exporters serve metrics:

```bash
docker compose ps
docker compose logs --tail 50 deploy-exporter
curl -s http://localhost:9201/metrics | grep site_deploy_exporter
curl -s http://localhost:11435/metrics | grep ollama_up
```

## Health signals

| Signal | Query | Healthy value |
|---|---|---|
| Deploy-exporter poll age | `time() - site_deploy_exporter_last_poll_timestamp_seconds` | Close to the 60 s poll interval |
| Deploy-exporter poll errors | `site_deploy_exporter_errors_total` | Flat; it counts failed repository polls since the exporter started |
| Ollama reachable | `ollama_up` | 1; the `OllamaDown` alert fires after 2 minutes at 0 |
| Proxy scraped | `up{job="ollama-exporter"}` | 1; the `OllamaExporterDown` alert fires after 2 minutes at 0 |
| Claude Code spend | `sum(model:claude_code_cost_usd:sum1h)` | Under USD 40 per hour, the `ClaudeCodeSpendSpike` threshold |

The deploy-exporter writes one log line per run it reads, with site, run number, outcome, duration and gate result. Failure lines carry `poll failed`, `log fetch failed`, `loki flush failed`, `probe fetch failed` or `state save failed`, followed by the site where one applies and the error.

Alert rules and thresholds: [Alerts and SLOs](doc:obs/alerts-and-slos).
