title: Status page
summary: How /inside/status/ decides the state of each service from records the site already publishes, and how to open, update and close an incident in incidents/*.yml.
order: 67
labels: inside, status, incidents, how-to
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: how-to
---
The [status page](/inside/status/) shows the current state of every service in the [catalog](/inside/services/) and the incident history. It is built by `scripts/build_inside.py` from `services/*.yml` and `incidents/*.yml`; the service states are read in the visitor's browser.

## Where the state comes from

The page reads only records the site already publishes, so a visit sends no request to a third party.

| Record | Used for | Written by |
|---|---|---|
| `https://<site>/conformity/latest.json` of each site | Gate pass or fail, time of the last run | The conformity job of each site |
| `/inside/deploys.json` | Result and push-to-live time of the last workflow run per public repository | The deploy job of this site |
| `map_generated` in `/inside/search.json` | Age of the map snapshot | The deploy job, after the map refresh |
| An open incident with reader impact | Marks the services it names as degraded | `incidents/*.yml` |

The `status` block of a service file names its records (`gate`, `deploys`). A service without one shows "No live check" and links its dashboard. The observability stack, SearXNG, the local LLM and the agent sessions have no record on this site; Grafana and the alert rules watch them. See [Alerts and SLOs](doc:obs/alerts-and-slos).

| State | Rule |
|---|---|
| Operational | The gate record passes and the last run on the deploy feed succeeded |
| Degraded | The gate fails (new deploys blocked, the previous build stays live), the last run failed, the map snapshot is older than eight days, or an open incident with reader impact names the service |
| Outage | A site does not answer with its gate record |
| No live check | No record for the service on this site |

## Incidents

One YAML file per incident in [incidents/](https://github.com/uncovertechtalent/machinebehavior.io/tree/main/incidents), named `YYYY-MM-DD-short-name.yml`.

| Field | Required | Values |
|---|---|---|
| `id` | yes | Same as the file name |
| `title`, `summary` | yes | Plain text, blameless: what happened to the system, never who |
| `services` | yes | Service ids from the catalog |
| `impact` | yes | `none`, `minor`, `major`, `critical`; `none` does not mark services as degraded |
| `started` | yes | `YYYY-MM-DD` or `YYYY-MM-DDTHH:MMZ` (UTC) |
| `resolved` | when resolved | Same format; set exactly when the last update is `resolved` |
| `updates` | yes | A list of `stage`, `at`, `text`; stages only go forward: investigating, identified, monitoring, resolved |
| `follow_up` | no | What changed so it does not happen again |
| `postmortem` | no | `doc:space/slug` links to the write-up and runbooks |

A time that was not recorded is written as a date alone and shown as "time not recorded". Only times with a record behind them (a commit, a run, a log line) carry a clock time.

## Open, update, close

1. Open: add the file with one `investigating` update, run `python3 scripts/build_inside.py`, run the gate dry run and push.
2. Update: append an update with the next stage, or another update in the same stage, and push.
3. Close: append a `resolved` update, set `resolved`, link the write-up in `postmortem`, and push.

The status page is as fresh as the last deploy. The incident text is in the page source, so the gate scans it like any other page.

## Rules for the text

- No private addresses, host names, personal details or employer names.
- Name the mechanism and the fix; no person is the cause.
- Numbers come from a record: a run, a commit, a query result.
