title: Public dashboards
summary: The six Grafana dashboards shared at grafana.scoetzee.de, what their panels show, and how each public cut differs from the internal dashboard.
order: 40
labels: grafana, dashboards, public
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: reference
---
Six dashboards are public at https://grafana.scoetzee.de and framed on [Inside](/inside/#dashboards). Grafana public dashboards do not resolve template variables, so every public dashboard is built without them in [grafana/build.py](https://github.com/uncovertechtalent/agent-observability/blob/main/grafana/build.py).

| Dashboard | Grafana uid | Link |
|---|---|---|
| Website deploys | site-deploys | [open](https://grafana.scoetzee.de/public-dashboards/e0f6a0c8f3a64884a67faac5cf4c3ad4) |
| Claude Code agents, public | claude-code-public | [open](https://grafana.scoetzee.de/public-dashboards/3a4ba6b21e6f4924ab2845b47a300af0) |
| FinOps: the bill, public | finops-public | [open](https://grafana.scoetzee.de/public-dashboards/9a0e4c394fc14f9880e766524aa637e8) |
| Host (Ollama box), public | host-public | [open](https://grafana.scoetzee.de/public-dashboards/81c9dfd269cc430abaf6a6ce7b64c4d6) |
| Local LLM (Ollama), public | local-llm-public | [open](https://grafana.scoetzee.de/public-dashboards/e6a9dd2153004ad0a868ce6f0e19071f) |
| SearXNG search engines | searxng-public | [open](https://grafana.scoetzee.de/public-dashboards/8bfa9ce4bdb946de8c37c738c9e61346) |

On 2026-10-09 each link returned the dashboard named in the table, with the same panels as the JSON in the repository. The FinOps link was checked on 2026-10-31 the same way: it returned the dashboard named in the table, with the 44 panels of the JSON (rows counted), and the login page of the host still answered 404.

## Website deploys

Default range 7 days, refresh every minute.

- Right now: whether each site's latest run deployed, time since each site's latest deploy, open gate findings and runs seen.
- History: deploy runs per hour by outcome, run duration from push to live with deploy markers, average time per workflow step and the result of every gate check on every run (the last two for machinebehavior.io).
- What the deploy shipped: map nodes, map links, links carried forward, pages dropped, and the decision probe fold rate by arm. The probe is record-only until 2026-11-04 and never blocks a deploy.
- Run log: one line per run, with titles for the public repositories only.

This dashboard has no template variables, and the exporter keeps private repository details out of Loki, so it is shared as built.

## Claude Code agents

Default range 24 hours. Cost, tokens, cache read share, API requests, prompts and tool calls over the range; the spend alert `ClaudeCodeSpendSpike` on a timeline (below USD 40, pending, firing); cost per hour by model, with the USD 40 threshold as a dashed line; tokens per second by type; cost by source (main loop, subagent, auxiliary). Cost, token and count values are sums over Claude Code events in Loki. The public cut drops the tools and API row, the traces row and the cost by skill and agent panel, because log lines show commands and file paths and skill names describe private work. Every query is wrapped in `sum without (...)` over identifying labels. Public dashboards drop annotations that query a data source, so the alert is a panel. The timeline reads the alert's own `ALERTS` series from 2026-10-09 11:00 UTC, when the USD 40 rule went live; earlier samples came from older rules, so before that point it replays the USD 40 rule on the recorded hourly cost, which starts at 07:29 UTC that day.

## FinOps

Default range this month, refresh every 15 minutes. The AWS bill in the shape of a FinOps tool, read from the cost and usage report, with the Claude plan beside it. The bill this month: One bill (AWS month to date plus the Claude plan price), AWS month to date, the Claude Code API calls at list price, AWS against the same days of last month, and the forecast against the budget. The Claude plan against list price: the plan price, the list price of the calls so far this month, a month-end projection, the projected savings, the multiple of the plan that the list price reaches, and a chart of the list price added up through the month against the plan. Cache efficiency: the prompt-cache hit ratio for the month so far and per day, cache reads over all input tokens. Cost centers by rule (virtual tags): daily spend, this month against last, and the services that rose and fell most. Where the money goes: usage types, months by cost center, months by record type. Anomalies: the latest day against the 28-day median per service and per cost center, and the daily total with its estimated days. Unit costs: AWS per 1,000 searches over 7 days, Claude Code per API call and per 1M output tokens, and the searches behind the first. A data row: the allocated share, the days compared, the latest complete day, the age of the data, whether the latest day is estimated, what measuring costs, the source, the forecast method, and the report line items.

The public cut is a separate dashboard (`finops-public`) built as an allow-list by panel title: 36 panels against 44, rows not counted. It drops the Resources row (its labels are instance ids, bucket names, and ARNs), the Commitments note, the fixed costs entered by hand with their unpriced items, and the two resource counts in the data row. The only fixed cost a kept panel reads is the Claude plan, so One bill adds AWS and the plan price; the list price of the calls stands in while the plan has no price. The panels that pass a metric's labels straight through name the labels they may show, and the build stops when a panel that shows labels is not on that list. A public dashboard runs each saved query on the server, which does not interpolate Grafana time variables, so the plan line of the chart reads the plan with a query function and starts on the day the plan was priced. The AWS figures are the UTC calendar month to date, so the dashboard does not offer a time range. The internal dashboard is not shared.

## Host

Default range 6 hours. Overview stats (uptime, CPU, load, memory, root filesystem, GPU temperature and power, failed systemd units), then rows for CPU, memory with ZFS ARC, disk, network, and GPU and sensors. The public cut sums or maxes per-device series into one line each, removes unit, container, mount, disk, network interface, sensor and job names, and drops the containers row: 30 panels against 34, rows not counted.

## Local LLM

Default range 6 hours. Service level stats (requests per minute, error ratio, slow first token, time to first token p95, decode tokens per second, Ollama up), a time-to-first-token heatmap, p50 and p95 by model, decode speed, model load time, token and request throughput, resident models with their GPU and CPU split, GPU utilisation and host CPU. The public cut replaces the model variable filter with `.*`.

## SearXNG search engines

The self-hosted SearXNG instance that research agents search through. Stats: instance up, searches per hour, share of searches with results over 24 hours, results per search, median search time, engines answering now. A table of the engines in use with their current state (ok, no results, rate-limited, blocked), answered share and median time over 24 hours, plus an engine status timeline and searches per hour by outcome. The public cut is a separate dashboard (`searxng-public`); the internal one is not shared. It shows engine names and outcomes only, nothing about how requests leave the network.

To add a dashboard to this list: [Share a dashboard publicly](doc:obs/runbook-share-a-dashboard).
