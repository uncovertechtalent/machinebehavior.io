title: Deploy exporter
summary: A standard-library Python service that reads the GitHub Actions deploy runs of three websites, writes them to Loki and serves the latest state as Prometheus metrics on port 9201.
parent: architecture
order: 10
labels: loki, prometheus, github-actions, deploys
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: reference
---
The deploy-exporter reads the GitHub Actions deploy runs of machinebehavior.io, tychat.io and uncovertechtalent.com and turns them into Loki lines and Prometheus metrics. It reads the GitHub API from outside the repositories, so the site workflows stayed unchanged, and a run that fails before any step finishes is still recorded. Source: [deploy-exporter/exporter.py](https://github.com/uncovertechtalent/agent-observability/blob/main/deploy-exporter/exporter.py), Python standard library only, running as user nobody.

## What it reads

| Site | Repository | Workflow |
|---|---|---|
| machinebehavior.io | uncovertechtalent/machinebehavior.io | Conformity |
| tychat.io | uncovertechtalent/tychat.io | Conformity |
| uncovertechtalent.com | the uncovertechtalent.com repository (private) | its Pages deploy workflow |

For the private repository the exporter stores no run titles, commit SHAs or URLs. It also reads the public probe record at `/conformity/probes/latest.json` on machinebehavior.io.

## Poll cycle

Every 60 seconds the exporter runs these steps:

1. List the newest 100 workflow runs per repository and keep the completed runs of the deploy workflow that are not yet in state.
2. Read each run's jobs and steps. Steps named "Set up job" or "Complete job", and steps whose name starts with "Post", are left out.
3. Download the log of each job that succeeded or failed. Parse the gate line (overall result, open findings, warnings, result per check) and the map refresh line. GitHub redirects job logs to signed blob storage; the exporter follows the redirect without the token.
4. Set the outcome: deployed (run succeeded), blocked (the step named Gate failed), cancelled, or failed.
5. Push one line for the run and one per step to Loki, each stamped with the time it finished, and one line per gate check stamped with the run's finish time. See [Loki streams](doc:obs/loki-streams).
6. Fetch the probe record and write state.

The metrics are listed in [Metrics reference](doc:obs/metrics-reference).

## State and backfill

State is `/data/state.json` on the Docker volume `deploy_exporter_data`: the last 500 run IDs per site, run counts by outcome, the latest run per site and the latest probe values. Without a state file, the first poll backfills from the GitHub API.

Loki takes samples up to one week old, so the exporter counts runs older than one week minus one hour and does not push them. After a poll that pushed runs that finished more than three hours ago, the exporter POSTs `/flush` to Loki, which makes the backfilled lines queryable at once. Replayed lines are exact duplicates, and Loki drops them. GitHub expires job logs after a while: older runs keep their timings and lose the per-check result. Runbook: [Backfilled runs missing in Loki](doc:obs/runbook-loki-backfill-missing).

## Configuration

| Variable | Default | Use |
|---|---|---|
| `GITHUB_TOKEN` | empty | Read access to the repositories and their Actions; private repositories and job logs fail without it |
| `LOKI_URL` | the Loki service, port 3100 | Push and flush target |
| `STATE_FILE` | `/data/state.json` | State location |
| `POLL_SECONDS` | 60 | Poll interval |
| `PORT` | 9201 | Metrics port |
| `SITES_JSON` | the three sites above | Replaces the site list |
| `PROBE_URL` | the machinebehavior.io probe record | Probe source |

The gate that produces the parsed lines is described in [Deploy pipeline](doc:eng/deploy-pipeline).
