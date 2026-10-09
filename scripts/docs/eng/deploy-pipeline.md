title: Deploy pipeline
summary: One GitHub Actions workflow runs the conformity checks, commits the record, and deploys to Pages only when the checks pass.
order: 20
labels: deploy, github-actions, pipeline
---
Every push to `main` of machinebehavior.io starts the workflow `.github/workflows/conformity.yml`. The workflow also runs every Monday at 06:17 UTC and by hand. It has two jobs, and the second runs only if the first passes.

## Job 1: conformity checks

1. Check out `main` with full history.
2. Run the conformity action against every published page (see [Conformity gate](doc:eng/conformity-gate)).
3. Commit `conformity/latest.json` and `conformity/index.html` as `conformity-bot`, with `[skip ci]` in the message, and push.
4. Gate step: read the overall result; anything other than `pass` fails the job with "deploy blocked, previous build stays live".

## Job 2: deploy to Pages

1. Check out `main` again, after the bot commit.
2. Refresh the map: run `scripts/crawl_map.py` against the live sites. The new `map/graph.json` replaces the committed one only if it has at least as many nodes and links. A partial crawl (for example Substack answering 403 to the runner) keeps the committed snapshot. This step may fail without failing the job, and its result is never committed.
3. Rebuild the search index: `scripts/build_search.py` merges the refreshed map with the docs and services into `inside/search.json`, so search matches the deployed map. It may fail without failing the job (the committed index is deployed) and is never committed. See [Top bar and search](doc:eng/top-bar-and-search).
4. Snapshot the deploy feed: read the last 15 Actions runs of machinebehavior.io and tychat.io and write `inside/deploys.json` for [Inside](/inside/). Like the map refresh, it may fail without failing the job and is never committed.
5. Snapshot the issues: `scripts/board_snapshot.py` reads the open and recently closed GitHub Issues and writes `inside/board/issues.json` for the [board](/inside/board/). It may fail without failing the job and is never committed. See [Ticket board](doc:eng/board).
6. Upload the repository as the Pages artifact and deploy it.

> [!warning] The bot commit moves `main` after every run. Always `git pull --rebase` before pushing; a push without it is rejected. See [Push rejected after a deploy](doc:eng/runbook-push-rejected).

## What happens around a deploy

- The [deploy exporter](doc:obs/deploy-exporter) polls the GitHub Actions API and writes each run, step and gate check to Loki and Prometheus. The [Website deploys dashboard](https://grafana.scoetzee.de/public-dashboards/e0f6a0c8f3a64884a67faac5cf4c3ad4) shows them.
- [Inside](/inside/) reads its deploy feed from the snapshot written in step 4; the visitor's browser sends no request to GitHub.

## Check before you push

```bash
git pull --rebase
python3 .github/actions/conformity/run.py --root . --config conformity/site-tier.json \
  --requirements conformity/requirements.json --out conformity --dry-run
```

Push only when the dry run prints `overall=pass`. In scripts, compare the value; a `grep` for `overall=` succeeds on a failing run too.
