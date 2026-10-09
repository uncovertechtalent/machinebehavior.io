title: Alerts and SLOs
summary: The recording rules, service level objectives and 13 alerts that Prometheus and the Loki ruler evaluate, with thresholds from the rule files.
parent: metrics-reference
order: 10
labels: prometheus, alerts, slo, loki
---
Prometheus evaluates recording rules and 13 alerts from [recording.yml](https://github.com/uncovertechtalent/agent-observability/blob/main/prometheus/rules/recording.yml) and [alerts.yml](https://github.com/uncovertechtalent/agent-observability/blob/main/prometheus/rules/alerts.yml). The Loki ruler adds one recording rule for Claude Code spend. The compose file runs no Alertmanager.

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
| ClaudeCodeSpendSpike | `sum(model:claude_code_cost_usd:sum1h) > 40` for 10 minutes | ticket |
| SearXNGDown | `searxng_up == 0` for 3 minutes | page |
| SearXNGProxyEgressDown | `searxng_proxy_up == 0` for 5 minutes | ticket |
| SearXNGTunnelDown | The SSH tunnel behind the proxy egress not active on the home server for 2 minutes | ticket |
| SearXNGEngineFailing | One engine failed over 80% of its calls in 30 minutes (rate limit, block, timeout or error), with at least 5 calls, for 10 minutes | ticket |
| SearXNGDegradedSearches | `search.sh` returned `SEARXNG_DEGRADED` 3 or more times in 15 minutes | ticket |
| SearXNGSlowSearches | Search latency p95 above 8 s over 30 minutes, with more than one search per 5 minutes, for 10 minutes | ticket |

The burn-rate alerts follow the multi-window, multi-burn-rate pattern from chapter 5 of the Google SRE Workbook. A homelab LLM serves a handful of requests per hour, and one failed request in a quiet hour is a 100% error ratio. The traffic floor on the two availability alerts holds the page in that case.

The SearXNG exporter pushes from the laptop that runs the instance, so a sleeping laptop leaves a gap in the series, not a zero. The SearXNG rules read pushed values, or failure ratios with a minimum number of calls; none reads `up` or `absent()`.

The spend threshold comes from the week of 2026-10-02 to 2026-10-08 in Loki: the median hour with any spend was USD 10.59, the 99th percentile of the trailing hour USD 47.71 and the busiest hour USD 87.41. Replayed on the trailing-hour series from 2026-10-02 to 2026-10-09 11:00 UTC in 5-minute steps, USD 40 fires four times, each on a busy hour with several sessions in parallel; the earlier USD 20 threshold fires 21 times. Details: [Budgets and alerts](doc:fin/budgets-and-alerts).

## Spend rule from Loki

`model:claude_code_cost_usd:sum1h` comes from the Loki ruler, file [loki/rules/fake/claude-code.yml](https://github.com/uncovertechtalent/agent-observability/blob/main/loki/rules/fake/claude-code.yml). Every minute it sums `cost_usd` over the `api_request` events of the trailing hour, by model, and remote-writes the result to Prometheus. "fake" is the tenant name when Loki runs without auth. The reason the alert does not read Claude Code's counters is in [Counter resets from parallel sessions](doc:obs/runbook-counter-resets-parallel-sessions).

## Tests

[prometheus/tests/alerts_test.yml](https://github.com/uncovertechtalent/agent-observability/blob/main/prometheus/tests/alerts_test.yml) checks 11 cases with promtool. The fast availability alert fires at 20% errors and one request per second, and the traffic floor holds it at one request per hour. The spend alert fires at USD 45 per hour summed over two models, does not fire at USD 35, and does not fire on 8 minutes above the threshold, inside the 10-minute hold. The SearXNG cases cover a down instance, a sleeping laptop, a rate-limited engine above and below the call floor, and degraded searches above and below the count.

```bash
docker run --rm -v "$PWD/prometheus:/p:ro" -w /p/tests --entrypoint promtool \
  prom/prometheus:v3.5.0 test rules alerts_test.yml
```
