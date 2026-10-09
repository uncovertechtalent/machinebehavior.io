title: Stat panel shows No data
summary: Why Grafana stat panels on young series show No data over long time ranges, and how build.py switches them to instant queries.
parent: runbooks
order: 20
labels: runbook, grafana, prometheus, loki
---
A stat panel shows "No data" when the dashboard range is long, for example 7 days, while the metric has a current value. This applies to the Website deploys dashboard: its default range is 7 days, and the deploy-exporter's series start when the exporter starts.

## Cause

By default a stat panel runs a range query over the dashboard range and reduces the result to one value. Over long ranges, stat panels on young series show "No data". An instant query evaluates at one point in time, so it returns the current value at any dashboard range.

## Check

1. Open the panel in Explore with the same query.
2. Set the query type to Instant and run it.
3. A value in Explore and "No data" in the panel confirm this cause.

## Fix

Make the panel run an instant query. In [grafana/build.py](https://github.com/uncovertechtalent/agent-observability/blob/main/grafana/build.py), the `now()` helper inside `site_deploys()` does this for a Prometheus stat panel:

- It sets `instant: true` on every target of the panel.
- It sets `graphMode` to none, since an instant query returns no history to draw.
- It sets explicit threshold colours, and optionally a value size.

A stat on Loki gets the same treatment from the `stat()` helper: with `ds=LOKI` it sets `queryType: instant`. With a `[$__range]` window, the instant query returns one total over the selected range. The Claude Code cost, token and count stats work this way.

Example from the Website deploys dashboard, description argument left out:

```python
p.append(L.place(now(stat("Runs seen", "sum(site_deploy_runs_total)")), 3, 5))
```

Then rebuild and deploy:

1. Run `python3 grafana/build.py` and commit the JSON.
2. Copy the repository to the home server and run `docker compose up -d --build`.
3. Reload the dashboard over a 7-day and a 30-day range and confirm the value shows in both.

## Where it applies

- Website deploys, row "Right now": latest run deployed, time since the latest deploy, open gate findings, runs seen.
- Website deploys, row "What the deploy shipped": map nodes, map links, links carried forward, pages dropped, decision probe fold rate.
- Claude Code agents: every stat in the "Spend and volume" row.

The workflow is described in [Dashboards as code](doc:obs/dashboards-as-code).
