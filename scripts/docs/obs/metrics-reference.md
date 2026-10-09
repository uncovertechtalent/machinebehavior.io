title: Metrics reference
summary: Every Prometheus metric the deploy-exporter and the ollama-exporter serve, with type, labels and meaning, taken from the exporter source.
order: 20
labels: prometheus, metrics, reference
---
This page lists every metric the two exporters in the repository serve on `/metrics`. Names, types and labels come from [deploy-exporter/exporter.py](https://github.com/uncovertechtalent/agent-observability/blob/main/deploy-exporter/exporter.py) and [ollama-exporter/exporter.py](https://github.com/uncovertechtalent/agent-observability/blob/main/ollama-exporter/exporter.py). Each histogram also serves `_bucket`, `_sum` and `_count` series.

## Deploy exporter, port 9201

Prometheus scrapes it every 60 seconds. Except for the two counters, each value describes the latest completed run per site.

| Metric | Type | Labels | Meaning |
|---|---|---|---|
| `site_deploy_runs_total` | counter | site, outcome | Completed deploy runs read: deployed, blocked, failed, cancelled |
| `site_deploy_last_finished_timestamp_seconds` | gauge | site | When the latest run finished |
| `site_deploy_last_duration_seconds` | gauge | site | Wall time of the latest run, start to finish |
| `site_deploy_last_deployed` | gauge | site | 1 if the latest run deployed, else 0 |
| `site_deploy_last_job_duration_seconds` | gauge | site, `gh_job` | Duration of each job in the latest run |
| `site_conformity_check_state` | gauge | site, check | 0 fail, 1 pending, 2 partial, 3 pass, -1 unknown |
| `site_conformity_findings_open` | gauge | site | Open findings after the latest gate run |
| `site_map_nodes` | gauge | site | Nodes in the map snapshot the latest deploy shipped |
| `site_map_links` | gauge | site | Links in that snapshot |
| `site_map_carried_links` | gauge | site | Links carried forward from the previous snapshot because their pages were unreachable from the runner |
| `site_map_dropped_pages` | gauge | site | Pages dropped because they did not return HTML |
| `site_probe_fold_ratio` | gauge | arm | Decision-layer probe: share of WAIT runs that folded under pushback; arm is stance or reference |
| `site_probe_last_timestamp_seconds` | gauge | none | When the latest probe ran |
| `site_deploy_exporter_last_poll_timestamp_seconds` | gauge | none | Last poll in which every repository poll succeeded |
| `site_deploy_exporter_errors_total` | counter | none | Failed repository polls since the exporter started |

The `site_map_*` series exist only for a site whose deploy log prints the map refresh line.

## Ollama exporter, port 11435

The request metrics carry three common labels: `gen_ai_operation_name` (chat, `text_completion` or embeddings), `gen_ai_request_model`, and `api` (ollama or openai).

| Metric | Type | Labels | Meaning |
|---|---|---|---|
| `gen_ai_client_operation_duration_seconds` | histogram | common, `error_type` | End-to-end duration at the proxy; `error_type` is the HTTP status (400 and up) or the connection error name, empty on success |
| `gen_ai_server_time_to_first_token_seconds` | histogram | common | Time to the first streamed chunk; streamed, successful, non-embedding requests only |
| `gen_ai_server_time_per_output_token_seconds` | histogram | common | `eval_duration / eval_count` from Ollama's final chunk |
| `gen_ai_client_token_usage` | histogram | common, `gen_ai_token_type` | Tokens per request, input or output |
| `ollama_tokens_total` | counter | common, `gen_ai_token_type` | Tokens processed, for `rate()` |
| `ollama_model_load_duration_seconds` | histogram | `gen_ai_request_model` | Model load time; near zero when the model is warm |
| `ollama_requests_in_flight` | gauge | `gen_ai_request_model` | Metered requests in progress |
| `ollama_loaded_model_info` | gauge | model, processor | 1 per resident model; processor is gpu, split or cpu |
| `ollama_loaded_model_bytes` | gauge | model, kind | Memory per resident model; kind is total or vram |
| `ollama_loaded_model_expiry_timestamp_seconds` | gauge | model | When Ollama unloads the model |
| `ollama_up` | gauge | none | 1 if the last `/api/ps` poll succeeded |

Time to first token is recorded for streamed requests only. For a non-streamed response the first byte arrives with the last, so the value would be end-to-end latency. The processor label is gpu when the whole model sits in VRAM, cpu when none of it does, and split otherwise.

Recording rules and alerts built on these metrics: [Alerts and SLOs](doc:obs/alerts-and-slos).
