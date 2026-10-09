title: Architecture
summary: How the collectors, the three stores, Grafana and the public front door of the observability stack connect, and how the stack is deployed.
order: 10
labels: architecture, alloy, prometheus, loki, tempo, grafana
---
The stack is one Docker Compose project on a home server: collectors feed Prometheus, Loki and Tempo, and Grafana reads all three. Every service is defined in [docker-compose.yml](https://github.com/uncovertechtalent/agent-observability/blob/main/docker-compose.yml).

## Collectors

- **Alloy** receives OTLP on port 4317 (gRPC) and 4318 (HTTP); its pipeline UI is on 12345. An attributes processor deletes `user.email`, `user.account_uuid`, `user.account_id`, `user.id` and `organization.id` before any store receives a signal. Config: [alloy/config.alloy](https://github.com/uncovertechtalent/agent-observability/blob/main/alloy/config.alloy).
- **ollama-exporter** is a pass-through proxy on port 11435. Ollama has no metrics endpoint. Its final response chunk carries `prompt_eval_count`, `eval_count`, `eval_duration` and `load_duration`. The proxy reads those fields and polls `/api/ps` every 15 seconds for resident models.
- **deploy-exporter** polls the GitHub Actions API for the three website repositories. See [Deploy exporter](doc:obs/deploy-exporter).
- **cAdvisor** reports per-container resources. `node_exporter` (port 9100) and `nvidia_gpu_exporter` (port 9835) run on the host.

To meter clients that hardcode Ollama's port 11434, the README describes a transparent mode: Ollama moves to port 11436, `OLLAMA_PROXY_PORT=11434` puts the proxy on the usual port, and `OLLAMA_UPSTREAM` points the proxy at the new Ollama port.

## Stores

| Store | Input | Retention | Settings |
|---|---|---|---|
| Prometheus | OTLP receiver, remote-write receiver, scrapes every 15 s | 90 days | Only `service.name`, `service.version` and `host.name` become labels; 30-minute out-of-order window for late OTLP batches |
| Loki | OTLP from Alloy, push API from the deploy-exporter | 90 days | TSDB schema v13, structured metadata on; the ruler remote-writes to Prometheus |
| Tempo | OTLP from Alloy | 14 days | Metrics generator writes span metrics and service graphs to Prometheus |

Scrape jobs: prometheus, ollama-exporter, alloy, loki, tempo, node, nvidia-gpu, cadvisor and deploy-exporter (every 60 s). Rules and alerts: [Alerts and SLOs](doc:obs/alerts-and-slos).

## Grafana

Grafana provisions three data sources (Prometheus as default, Loki, Tempo) and the dashboard JSON files into the folder "Agent Observability", read-only. Prometheus exemplars link to Tempo traces, and Tempo traces link to Loki logs by trace ID. On the home network, anonymous visitors get the Viewer role. Embedding is on (`GF_SECURITY_ALLOW_EMBEDDING=true`), so [Inside](/inside/#dashboards) frames the public dashboards. How the JSON is built: [Dashboards as code](doc:obs/dashboards-as-code).

## Front door

https://grafana.scoetzee.de reaches Grafana through a cloud reverse proxy. Only `/public-dashboards/*`, `/api/public/*` and `/public/*` pass. The login page returns 404 from outside (checked 2026-10-09). The shared dashboards are listed in [Public dashboards](doc:obs/public-dashboards).

## Deployment

The repository is copied to the home server and started with `docker compose up -d --build`. Every service has `restart: unless-stopped`. Data lives in named volumes: `alloy_data`, `prometheus_data`, `loki_data`, `tempo_data`, `grafana_data` and `deploy_exporter_data`. The Grafana admin password comes from `GRAFANA_ADMIN_PASSWORD` in `.env`, and the deploy-exporter reads `GITHUB_TOKEN` from the same file.
