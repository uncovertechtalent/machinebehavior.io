title: Deploy pipeline
summary: One GitHub Actions workflow runs the conformity checks, commits the record, and deploys to Pages only when the checks pass.
order: 20
labels: deploy, github-actions, pipeline
owner: Stefan Coetzee
reviewed: 2026-10-12
review_by: 2027-01-10
type: explanation
---
Every push to `main` of machinebehavior.io starts the workflow `.github/workflows/conformity.yml`; since [ADR-0029](doc:eng/adr-0029-changes-through-pull-requests) that push is a merged pull request or a bot commit. The workflow also runs every Monday at 06:17 UTC, by hand, and on every pull request to `main`. It has three jobs. Job 2 runs only if job 1 passes; job 3 runs beside them and the deploy does not wait for it. A pull request run is the required check before the merge: it runs job 1 on the merge result of the pull request, commits nothing and skips job 2. The workflow grants no permissions itself; each job asks for its own, listed under its heading.

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

## Pull request review

A second workflow, `.github/workflows/change-review.yml`, reviews each pull request from a branch of this repository with `/sdlc:change-review` from the CTO powersuit and posts the review as one comment. It reads this repository's ADRs, these docs, `CLAUDE.md`, the gate's README and config, [/man/](/man/), [/llms.txt](/llms.txt) and the linked issue first, so a recorded choice is a note ("intentional per ADR-NNNN"), not a finding. It needs the repository secret `CLAUDE_CODE_OAUTH_TOKEN`, skips without it, and is not a required check.

> [!warning] The bot commit moves `main` after every run. Branch from `origin/main` and rebase the branch on it when it falls behind; a direct push to `main` is rejected. See [Push rejected](doc:eng/runbook-push-rejected).

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
