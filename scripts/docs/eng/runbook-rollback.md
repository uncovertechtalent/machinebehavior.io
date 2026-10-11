title: Roll back a deploy
summary: A deploy passed the gate and the live site is wrong; revert the commits on main and push, so the workflow gates and deploys the earlier state. Re-running an older run does not roll back.
parent: runbooks
order: 40
labels: runbook, deploy, rollback
owner: Stefan Coetzee
reviewed: 2026-10-11
review_by: 2027-01-09
type: how-to
---
**Symptom.** The Conformity workflow is green and the Deploy to Pages job succeeded, but a page on the live site is wrong or broken.

**If the gate failed instead,** there is nothing to roll back: the deploy did not run and the previous build is still live. Follow [Gate blocked a deploy](doc:eng/runbook-gate-blocked).

## How a rollback works here

The only path to the live site is a push to `main` that passes the gate ([Deploy pipeline](doc:eng/deploy-pipeline)), and changes reach `main` through pull requests ([ADR-0029](doc:eng/adr-0029-changes-through-pull-requests)). A rollback is therefore a revert pull request that undoes the bad commit, and it goes through the same check, gate and deploy as any other change.

Re-running an earlier workflow run does not roll back. Both jobs in `.github/workflows/conformity.yml` check out `main` by name (`ref: main`), so a re-run, or a run started by hand, deploys the current `main`. There is no way in the workflow to redeploy an earlier build.

## Steps

1. **Record it, if readers saw it.** Open `incidents/YYYY-MM-DD-short-name.yml` with an `investigating` update, as in [Status page](doc:eng/status-page). It can go out in the same push as the revert.
2. **Find the commits to undo.** The run on GitHub Actions, the [Website deploys dashboard](https://grafana.scoetzee.de/public-dashboards/e0f6a0c8f3a64884a67faac5cf4c3ad4) and `git log` name the commit each deploy came from. Skip the `conformity-bot` commits marked `[skip ci]`: they only touch `conformity/latest.json` and `conformity/index.html`, which every run rewrites.
3. **Revert on a branch from the current main**, newest commit first:

   ```bash
   git fetch origin && git switch -c revert-<sha> origin/main
   git revert --no-edit <sha>
   ```

   If the revert conflicts with later commits, fix forward instead: change the page and send the fix through the same steps.
4. **Leave hashed predictions alone.** If a bad commit added or changed a file in `predictions/` or `predictions/HASHES.txt`, do not revert those files; predictions are never edited after hashing. Ask the operator how to withdraw it.
5. **Run the dry run** until it prints `overall=pass`:

   ```bash
   python3 .github/actions/conformity/run.py --root . --config conformity/site-tier.json \
     --requirements conformity/requirements.json --out conformity --dry-run
   ```

   A revert can fail the gate when a rule or a check changed since the bad commit. Fix the failing check as in [Gate blocked a deploy](doc:eng/runbook-gate-blocked); until the gate passes, the bad build stays live.
6. **Open the revert pull request and merge it.** `git push -u origin HEAD`, `gh pr create --fill`, wait for the Conformity checks on the pull request (`gh pr checks --watch`), then merge (`gh pr merge --squash`). The merge starts the run on `main`. A run already in progress on `main` finishes first; the workflow does not cancel it (`cancel-in-progress: false`).
7. **Check the result.** The Conformity checks job and the Deploy to Pages job are green, the [status page](/inside/status/) shows the site as operational, and the page itself is right. Then move the incident record through `monitoring` to `resolved`.

## What a rollback does not restore

The deploy job rebuilds four files from live sources on every deploy and never commits them, so a rollback deploy carries their state at the time of the rollback, not the state of the bad deploy or of the one before it:

| File | Rebuilt from | If the step fails |
|---|---|---|
| `map/graph.json` | `scripts/crawl_map.py` against the live sites | The committed snapshot is deployed; it is also kept when the crawl returns fewer nodes or links |
| `inside/search.json` | `scripts/build_search.py`, from the docs, the services and the map | The committed index is deployed |
| `inside/deploys.json` | The last 15 Actions runs of machinebehavior.io and tychat.io | The step fails without failing the job |
| `inside/board/issues.json` | `scripts/board_snapshot.py`, from GitHub Issues | The step fails without failing the job |

Each of these steps may fail without failing the job, so a green deploy does not prove they ran; read the step log.

## When this does not help

- **GitHub Pages or Actions is down.** Nothing in this repository can deploy or roll back. Escalate to GitHub ([On-call and escalation](doc:obs/on-call)).
- **The fault is in the gate's rule table or tiers.** Changes to the gate go to the gate owner; tier changes are the operator's decision ([Conformity gate](doc:eng/conformity-gate)).

## Time

No rollback has been timed. The one recorded fix-forward, the blocked deploy of 2026-10-08, took 81 seconds from the failed run to the passing run.
