title: Backfilled runs missing in Loki
summary: What to do when the Website deploys dashboard shows no older runs after the deploy-exporter backfills from GitHub Actions.
parent: runbooks
order: 10
labels: runbook, loki, deploy-exporter
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: how-to
---
The Website deploys dashboard shows only recent runs, or none, right after the deploy-exporter starts with an empty state file, while the exporter log lists the runs it read.

## Cause

The exporter pushes each run with the time it finished, so a backfill writes lines that are hours or days old. Loki holds lines older than its ingester window until their chunk flushes, which takes up to 30 minutes. Until then, queries over those older time ranges return nothing.

A second limit applies: Loki takes samples up to one week old. The exporter does not push runs older than one week minus one hour; it counts them in `site_deploy_runs_total` only.

## Check

1. Read the exporter log: `docker compose logs --tail 100 deploy-exporter`. Each pushed run prints site, run number, outcome, duration and gate result.
2. Look for `loki flush failed` in the same log. It means the automatic flush did not reach Loki.
3. In Grafana Explore, query `{job="site-deploys"}` over the last 7 days and compare with the runs in the log.

## Fix

1. The exporter POSTs `/flush` to Loki at the end of every poll that pushed a run that finished more than three hours ago. After a successful flush, no action is needed.
2. If the log shows `loki flush failed`, run the flush below on the home server.
3. Reload the dashboard. The lines appear once the chunk is flushed.
4. Runs older than one week stay out of Loki. `site_deploy_runs_total` still counts them.

```bash
curl -X POST http://localhost:3100/flush
```

## Re-run a backfill

To read the history again, remove the state file and restart the exporter:

```bash
docker compose exec deploy-exporter rm /data/state.json && docker compose restart deploy-exporter
```

The first poll reads the newest 100 runs per repository again and pushes every run younger than a week. Replayed lines are exact duplicates, and Loki drops them. Two side effects follow: the run counts restart from what the backfill finds, and runs whose job logs GitHub has expired come back without per-check results.

Source of the flush logic: `flush_loki()` and `poll_site()` in [deploy-exporter/exporter.py](https://github.com/uncovertechtalent/agent-observability/blob/main/deploy-exporter/exporter.py). Background: [Deploy exporter](doc:obs/deploy-exporter).
