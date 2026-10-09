title: Alerts and SLOs
summary: The recording rules, service level objectives and seven alerts that Prometheus and the Loki ruler evaluate, with thresholds from the rule files.
parent: metrics-reference
order: 10
labels: prometheus, alerts, slo, loki
---
Prometheus evaluates recording rules and seven alerts from [recording.yml](https://github.com/uncovertechtalent/agent-observability/blob/main/prometheus/rules/recording.yml) and [alerts.yml](https://github.com/uncovertechtalent/agent-observability/blob/main/prometheus/rules/alerts.yml). The Loki ruler adds one recording rule for Claude Code spend. The compose file runs no Alertmanager.

## Service level objectives

Both SLOs cover the local LLM behind the ollama-exporter.

| SLO | Target | Good event |
|---|---|---|
| Availability | 99% | A request without an upstream error (`error_type` empty) |
| Latency | 95% | A streamed chat request with a first token within 4 s |

SLI rules record the error ratio and the slow-first-token ratio over 5m, 30m, 1h and 6h windows (`sli:gen_ai_availability_errors:ratio_rate*` and `sli:gen_ai_ttft_slow:ratio_rate*`). Per-model rules record request rate, error rate, time to first token p50 and p95, decode tokens per second and token rate (`model:gen_ai_*`). Both groups run every 30 seconds.

## Alerts

| Alert | Condition | Severity |
|---|---|---|
| LocalLLMAvailabilityBudgetBurnFast | Error ratio above 14.4 times 1% over 1h and 5m, and over 1h more than one request per 10 minutes | page |
| LocalLLMAvailabilityBudgetBurnSlow | Error ratio above 6 times 1% over 6h and 30m, and over 6h more than one request per 30 minutes | ticket |
| LocalLLMLatencyBudgetBurnFast | Slow-first-token ratio above 14.4 times 5% over 1h and 5m | page |
| OllamaDown | `ollama_up == 0` for 2 minutes | page |
| OllamaExporterDown | `up{job="ollama-exporter"} == 0` for 2 minutes | page |
| ModelSpilledToCPU | A resident model on split or cpu while requests are in flight, for 5 minutes | info |
| ClaudeCodeSpendSpike | `sum(model:claude_code_cost_usd:sum1h) > 20` for 10 minutes | ticket |

The burn-rate alerts follow the multi-window, multi-burn-rate pattern from chapter 5 of the Google SRE Workbook. A homelab LLM serves a handful of requests per hour, and one failed request in a quiet hour is a 100% error ratio. The traffic floor on the two availability alerts holds the page in that case.

## Spend rule from Loki

`model:claude_code_cost_usd:sum1h` comes from the Loki ruler, file [loki/rules/fake/claude-code.yml](https://github.com/uncovertechtalent/agent-observability/blob/main/loki/rules/fake/claude-code.yml). Every minute it sums `cost_usd` over the `api_request` events of the trailing hour, by model, and remote-writes the result to Prometheus. "fake" is the tenant name when Loki runs without auth. The reason the alert does not read Claude Code's counters is in [Counter resets from parallel sessions](doc:obs/runbook-counter-resets-parallel-sessions).

## Tests

[prometheus/tests/alerts_test.yml](https://github.com/uncovertechtalent/agent-observability/blob/main/prometheus/tests/alerts_test.yml) checks four cases with promtool. The fast availability alert fires at 20% errors and one request per second, and the traffic floor holds it at one request per hour. The spend alert fires at USD 25 per hour and does not fire at USD 15.

```bash
docker run --rm -v "$PWD/prometheus:/p:ro" -w /p/tests --entrypoint promtool \
  prom/prometheus:v3.5.0 test rules alerts_test.yml
```
