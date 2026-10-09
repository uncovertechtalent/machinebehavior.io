title: Observability
summary: Metrics, logs and traces for Claude Code, a self-hosted Ollama server, its host and three website deploys, collected by one Docker Compose stack on a home server.
labels: observability, prometheus, loki, tempo, grafana
---
The Observability space documents agent-observability: a Docker Compose stack that collects metrics, logs and traces from Claude Code, a self-hosted Ollama server, the host that runs Ollama, and the GitHub Actions deploys of three websites. Stefan Coetzee runs it on a home server. Four of its Grafana dashboards are public and framed on the [Inside](/inside/#dashboards) page.

Source: [uncovertechtalent/agent-observability](https://github.com/uncovertechtalent/agent-observability) on GitHub, MIT licence.

## Components

| Component | Image or source | Role |
|---|---|---|
| Grafana Alloy | grafana/alloy:v1.10.0 | Receives OTLP from Claude Code, deletes identity attributes, sends each signal to its store |
| Prometheus | prom/prometheus:v3.5.0 | Metrics store, recording rules and alerts |
| Loki | grafana/loki:3.5.0 | Claude Code events and website deploy records |
| Tempo | grafana/tempo:2.8.1 | Claude Code traces, span metrics for Prometheus |
| Grafana | grafana/grafana:12.1.0 | Dashboards, provisioned read-only from the repository |
| ollama-exporter | repository, Python | Metering proxy in front of Ollama |
| deploy-exporter | repository, Python | GitHub Actions deploy runs of the three sites |
| cAdvisor | gcr.io/cadvisor/cadvisor:v0.49.1 | Per-container CPU, memory, network and disk |

`node_exporter` and `nvidia_gpu_exporter` run on the Docker host, outside the compose file.

## How data flows

1. Claude Code exports metrics, events and traces over OTLP gRPC to Alloy on port 4317.
2. Alloy deletes the account email, account IDs and organisation ID, batches the signals, and sends metrics to Prometheus, events to Loki and traces to Tempo.
3. Tempo writes span metrics to Prometheus. The Loki ruler writes the hourly Claude Code cost to Prometheus.
4. LLM clients call the ollama-exporter on port 11435. It passes each request to Ollama unchanged and records metrics, which Prometheus scrapes.
5. The deploy-exporter polls the GitHub Actions API, pushes one Loki line per run, step and gate check, and serves the latest state on port 9201.
6. Grafana reads Prometheus, Loki and Tempo. A cloud reverse proxy publishes only the public dashboard paths at https://grafana.scoetzee.de.

## Start here

- [Architecture](doc:obs/architecture): collectors, stores, Grafana, the front door and the deployment.
- [Public dashboards](doc:obs/public-dashboards): the four shared dashboards and their links.
- [Metrics reference](doc:obs/metrics-reference) and [Loki streams](doc:obs/loki-streams): names, labels and fields.
- [Runbooks](doc:obs/runbooks): fixes for the known traps.

The website deploy gate itself is documented in the Engineering space: [Deploy pipeline](doc:eng/deploy-pipeline).
