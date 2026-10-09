title: Share a dashboard publicly
summary: How to build a variable-free public cut of a dashboard, provision it, and turn on Grafana public sharing so it loads at grafana.scoetzee.de.
parent: runbooks
order: 40
labels: runbook, grafana, public-dashboards
---
A dashboard goes public in two parts: a public cut in build.py, and a public-dashboard record created through the Grafana API on the home server.

## Before you start

- Grafana public dashboards do not resolve template variables. A dashboard with variables gets a cut without them.
- Panels that show log lines, traces, names of private work or private repository details stay out of the cut. `claude_code_public` and `host_public` in [grafana/build.py](https://github.com/uncovertechtalent/agent-observability/blob/main/grafana/build.py) show both techniques: dropping panels and aggregating labels away.
- The front door at https://grafana.scoetzee.de passes only `/public-dashboards/*`, `/api/public/*` and `/public/*`, so the API call below runs on the home server.

## Steps

1. In `grafana/build.py`, add a function that returns a copy of the dashboard with an empty variable list, every variable filter replaced (for example `$model` with `.*`) and identifying labels aggregated away. Give it a uid that ends in `-public`.
2. Add the function to the list at the bottom of build.py, run `python3 grafana/build.py` and commit the JSON.
3. Copy the repository to the home server and run `docker compose up -d --build`. Grafana provisions the new dashboard in the folder "Agent Observability".
4. On the home server, create the public record with the command below. curl prompts for the admin password, which is `GRAFANA_ADMIN_PASSWORD` in `.env`.
5. Read `accessToken` in the JSON response. The public URL is https://grafana.scoetzee.de/public-dashboards/ followed by that token.
6. From outside the home network, open the URL and confirm the panels load.
7. Add the dashboard to [Public dashboards](doc:obs/public-dashboards). To frame it on Inside, see [Inside portal](doc:eng/inside-portal).

```bash
DASH=local-llm-public   # uid of the dashboard to share
curl -u admin -X POST -H 'Content-Type: application/json' \
  -d '{"isEnabled": true, "share": "public"}' \
  "http://localhost:3000/api/dashboards/uid/$DASH/public-dashboards"
```

## Check the result

| Check | Expected |
|---|---|
| Public URL from outside | Dashboard loads, no login |
| https://grafana.scoetzee.de/login from outside | 404 |
| Any panel with a template variable | None; the cut has an empty variable list |
| Panel queries | Hidden: on 2026-10-09 the public API served panel targets without query expressions; the annotation query of Website deploys was served |

Which dashboards are public today, and what each one shows: [Public dashboards](doc:obs/public-dashboards).
