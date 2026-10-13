title: Deploy pipeline
summary: One GitHub Actions workflow runs the conformity checks, commits the record, and deploys to Pages only when the checks pass.
order: 20
labels: deploy, github-actions, pipeline
owner: Stefan Coetzee
reviewed: 2026-10-13
review_by: 2027-01-11
type: explanation
---
Every push to `main` of machinebehavior.io starts the workflow `.github/workflows/conformity.yml`; since [ADR-0029](doc:eng/adr-0029-changes-through-pull-requests) that push is a merged pull request or a bot commit. The workflow also runs every Monday at 06:17 UTC, by hand, and on every pull request to `main`. It has four jobs. Job 2 runs only if job 1 passes; job 3 runs beside them and the deploy does not wait for it; job 4 runs after a successful deploy from a push to `main`. A pull request run is the required check before the merge: it runs job 1 on the merge result of the pull request, commits nothing and skips job 2. The workflow grants no permissions itself; each job asks for its own, listed under its heading.

## Job 1: conformity checks

Permissions: `contents: write`, for the bot commit when the deploy key is missing.

1. Check out `main` with full history (a pull request run checks out the merge result). On every run except a pull request run, checkout uses the deploy key in the secret `CONFORMITY_PUSH_KEY` when it exists, so the bot commit in step 3 passes the branch rules on `main`.
2. Run the conformity action against every published page (see [Conformity gate](doc:eng/conformity-gate)).
3. Commit `conformity/latest.json` and `conformity/index.html` as `conformity-bot`, with `[skip ci]` in the message, and push. Skipped on pull request runs.
4. Gate step: read the overall result; anything other than `pass` fails the job with "deploy blocked, previous build stays live".

## Job 2: deploy to Pages

Permissions: `contents: read`, `pages: write` and `id-token: write` for the deploy, and `actions: read` and `issues: read` for the two snapshots in steps 4 and 5.

1. Check out `main` again, after the bot commit, without persisting the credentials.
2. Refresh the map: run `scripts/crawl_map.py` against the live sites. The new `map/graph.json` replaces the committed one only if it has at least as many nodes and links. A partial crawl (for example Substack answering 403 to the runner) keeps the committed snapshot. This step may fail without failing the job, and its result is never committed.
3. Rebuild the search index: `scripts/build_search.py` merges the refreshed map with the docs and services into `inside/search.json`, so search matches the deployed map. It may fail without failing the job (the committed index is deployed) and is never committed. See [Top bar and search](doc:eng/top-bar-and-search).
4. Snapshot the deploy feed: read the last 15 Actions runs of machinebehavior.io and tychat.io and write `inside/deploys.json` for [Inside](/inside/). Like the map refresh, it may fail without failing the job and is never committed.
5. Snapshot the issues: `scripts/board_snapshot.py` reads the open and recently closed GitHub Issues and writes `inside/board/issues.json` for the [board](/inside/board/). It may fail without failing the job and is never committed. See [Ticket board](doc:eng/board).
6. Upload the repository as the Pages artifact and deploy it.

## Job 3: workflow security (zizmor)

Permissions: `contents: read`.

zizmor checks every workflow and the conformity action under `.github/` for template injection, broad permissions, persisted credentials, unpinned or impostor actions, and actions with known advisories. It runs on every trigger, pull requests included. A finding fails this job and never blocks the deploy; it is a required check only if the ruleset names it. Accepted findings have an inline `# zizmor: ignore[<rule>]` comment, and `.github/zizmor.yml` lists each one with its reason. Details in `conformity/README.md`.

## Job 4: submit changed URLs to IndexNow

Permissions: `contents: read`, to check out the deployed commit with its history.

Runs only after job 2 succeeds on a push to `main` ([#85](https://github.com/uncovertechtalent/machinebehavior.io/issues/85)). Scheduled and manual runs have no push range and submit nothing.

1. Check out the commit job 2 deployed, recorded by its step "Record the deployed commit", with full history.
2. `scripts/indexnow.py` lists the files that changed between the commit before the push (`github.event.before`) and the deployed commit. Each changed `index.html` of a page in `sitemap.xml` becomes its URL, a changed `llms.txt` is added, and the sitemap URL goes with every submission. Removed pages are left out. When nothing a search engine reads changed, the job stops here.
3. `curl` posts the host, the key, the key location and the URL list to `https://api.indexnow.org/indexnow` and logs the HTTP status: 200 means submitted, 202 received with the key check pending. Any other status, or no URL list, is a warning in the job log.

The key is public by design: the engines fetch `/a738b040f4845f81e1a541ccd2b9e05d.txt` from the site root to check that a submission comes from the site's owner. The job is `continue-on-error` and never fails the run; the deploy is already live, and a refused submission waits for the next crawl. To check a submission, read the job log of the run.

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
