title: Cost model
summary: Every cost component of the platform with its billing model, its meter and the amount where a source exists; components without a meter say so.
order: 10
labels: finops, cost-model, allocation
---
Nine components make up the cost of the platform. Four have a meter in the observability stack or in a provider API: Claude Code, the Bedrock evals, GitHub Actions and the GPU's energy. The others are billed by invoice or through the household electricity meter, and their amounts are not published.

## Components

| Component | Billing model | Meter here | Amount, range and source |
|---|---|---|---|
| Claude Code | Subscription plan: a flat fee with usage limits. Claude Code also prices each API call at list price per token. | One `api_request` event per API call in Loki with the model, `cost_usd`, four token counts and `query_source` ([Loki streams](doc:obs/loki-streams)) | List-price value USD 1,021.01 for 5,505 calls, 2026-10-01 15:21 to 2026-10-09 00:00 UTC (Loki). The billed amount: [Showback](doc:fin/showback) |
| Amazon Bedrock (evals) | On-demand price per input token and per output token, by model and region | The eval harness multiplies the token counts of each reply by the prices it declares (AWS Pricing API, 2026-10-07) | USD 14.94 for 14,040 calls in ten runs on 2026-10-07, from USD 0.21 to USD 5.13 per run (eval records; [Unit economics](doc:fin/unit-economics)). The AWS invoice is not published |
| GitHub Pages and Actions | Free on standard runners for public repositories. Private repositories get 2,000 minutes a month on GitHub Free and 3,000 on GitHub Team, then USD 0.006 a minute on a Linux 2-core runner ([GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)) | Actions API: job durations, and the run timing endpoint, which reports 0 billable ms for these repositories; the [deploy exporter](doc:obs/deploy-exporter) | USD 0 billed; 47.0 runner minutes over 63 runs of machinebehavior.io and tychat.io, 2026-10-01 to 2026-10-08 (Actions API) |
| Domains and DNS | Yearly registration per domain; hosted DNS zones billed by the month | None in the stack; registrar and DNS invoices | Not published |
| Cloud reverse proxy | A small virtual machine billed by the hour, plus disk and outbound traffic | None in the stack; the cloud provider's invoice | Not published |
| Home server power | Household electricity tariff per kWh | GPU board power only (`nvidia_smi_power_draw_watts`, one sample a minute); no meter for the whole host | GPU 2.22 kWh, 2026-10-01 to 2026-10-09 00:00 UTC, mean 11.6 W (Prometheus). The tariff is not published |
| Observability stack | Open-source images, no licence fee; it uses disk and a share of the host's power | Docker volume sizes; `prometheus_tsdb_storage_blocks_bytes` | 794 MB of volumes on 2026-10-09: Prometheus 713.5 MB, Grafana 53.0 MB, Tempo 22.1 MB, Loki 5.9 MB (`docker system df`) |
| Local LLM (Ollama on a GTX 1650) | No fee per token; the GPU's power and the hardware | ollama-exporter request and token counters ([Architecture](doc:obs/architecture)) | 1,716 requests, 1.30 million input and 66,883 output tokens, 2026-10-01 to 2026-10-09 00:00 UTC (Prometheus) |
| Second-vendor model access | Codex CLI on a ChatGPT plan, used for cross-model checks: a flat subscription with usage limits | None | Not published |

Outside the model: the workstation that runs Claude Code, the home internet line and the purchase of the home server. No depreciation schedule exists for the hardware.

## Allocation of Claude Code spend

Each event carries `query_source`, the subsystem that sent the call. Grouped as on the [Claude Code dashboard](doc:obs/public-dashboards), 2026-10-01 15:21 to 2026-10-09 00:00 UTC:

| Group | `query_source` values | USD | Share |
|---|---|---|---|
| Main loop | `sdk` (the desktop app's main conversation) | 762.14 | 74.6% |
| Subagents | `agent:builtin:workflow-subagent` 155.17, `agent:builtin:general-purpose` 51.09, `agent:builtin:Explore` 1.33, `agent:builtin:claude-code-guide` 0.13 | 207.71 | 20.3% |
| Side calls | `prompt_suggestion` 46.08, `insights` 3.36, `web_fetch_apply` 1.34, `compact` 0.38 | 51.16 | 5.0% |

Allocation stops there. The events carry no session ID (`OTEL_METRICS_INCLUDE_SESSION_ID=false`) and no working directory, so spend per project or per repository cannot be read from them. The cost of building and publishing an experiment, for example, is inside the Claude Code total and cannot be split out. The model calls under test can: they run on Bedrock and the harness records them per run.

## Metering choices

- Claude Code spend comes from per-request events, never from the cumulative counters. The reason is in [The phantom two million](doc:fin/anomaly-the-phantom-two-million).
- The Bedrock figures are the harness's own sums at declared prices. They are estimates of the invoice, close to it when no discount or credit applies.
- GPU power covers the graphics card only. The rest of the host draws power that no sensor in the stack reports.

Sources: Loki and Prometheus on the home server, queried 2026-10-09; the GitHub Actions API, queried 2026-10-09; eval run records of experiment 04 ([Experiment 04](doc:res/experiment-04-folding-under-pressure), [Weekly decision-layer probe](doc:res/decision-layer-probe)).
