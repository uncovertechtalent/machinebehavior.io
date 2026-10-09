title: Public dashboards
summary: The four Grafana dashboards shared at grafana.scoetzee.de, what their panels show, and how each public cut differs from the internal dashboard.
order: 40
labels: grafana, dashboards, public
---
Four dashboards are public at https://grafana.scoetzee.de and framed on [Inside](/inside/#dashboards). Grafana public dashboards do not resolve template variables, so every public dashboard is built without them in [grafana/build.py](https://github.com/uncovertechtalent/agent-observability/blob/main/grafana/build.py).

| Dashboard | Grafana uid | Link |
|---|---|---|
| Website deploys | site-deploys | [open](https://grafana.scoetzee.de/public-dashboards/e0f6a0c8f3a64884a67faac5cf4c3ad4) |
| Claude Code agents, public | claude-code-public | [open](https://grafana.scoetzee.de/public-dashboards/3a4ba6b21e6f4924ab2845b47a300af0) |
| Host (Ollama box), public | host-public | [open](https://grafana.scoetzee.de/public-dashboards/81c9dfd269cc430abaf6a6ce7b64c4d6) |
| Local LLM (Ollama), public | local-llm-public | [open](https://grafana.scoetzee.de/public-dashboards/e6a9dd2153004ad0a868ce6f0e19071f) |

On 2026-10-09 each link returned the dashboard named in the table, with the same panels as the JSON in the repository.

## Website deploys

Default range 7 days, refresh every minute.

- Right now: whether each site's latest run deployed, time since each site's latest deploy, open gate findings and runs seen.
- History: deploy runs per hour by outcome, run duration from push to live with deploy markers, average time per workflow step and the result of every gate check on every run (the last two for machinebehavior.io).
- What the deploy shipped: map nodes, map links, links carried forward, pages dropped, and the decision probe fold rate by arm. The probe is record-only until 2026-11-04 and never blocks a deploy.
- Run log: one line per run, with titles for the public repositories only.

This dashboard has no template variables, and the exporter keeps private repository details out of Loki, so it is shared as built.

## Claude Code agents

Default range 24 hours. Cost, tokens, cache read share, API requests, prompts and tool calls over the range; cost per hour by model; tokens per second by type; cost by source (main loop, subagent, auxiliary). The values are sums over Claude Code events in Loki. The public cut drops the tools and API row, the traces row and the cost by skill and agent panel, because log lines show commands and file paths and skill names describe private work. Every query is wrapped in `sum without (...)` over identifying labels.

## Host

Default range 6 hours. Overview stats (uptime, CPU, load, memory, root filesystem, GPU temperature and power, failed systemd units), then rows for CPU, memory with ZFS ARC, disk, network, and GPU and sensors. The public cut sums or maxes per-device series into one line each, removes unit, container, mount, disk, network interface, sensor and job names, and drops the containers row: 30 panels against 34, rows not counted.

## Local LLM

Default range 6 hours. Service level stats (requests per minute, error ratio, slow first token, time to first token p95, decode tokens per second, Ollama up), a time-to-first-token heatmap, p50 and p95 by model, decode speed, model load time, token and request throughput, resident models with their GPU and CPU split, GPU utilisation and host CPU. The public cut replaces the model variable filter with `.*`.

To add a dashboard to this list: [Share a dashboard publicly](doc:obs/runbook-share-a-dashboard).
