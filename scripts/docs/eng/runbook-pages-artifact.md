title: Pages deploy finds no artifact
summary: Deploy to Pages fails with "No artifacts named github-pages were found" although the upload succeeded; the artifact list lagged the upload. Start a fresh run on main.
parent: runbooks
order: 50
labels: runbook, deploy, pages
owner: Stefan Coetzee
created: 2026-11-25
reviewed: 2026-11-25
review_by: 2027-02-23
type: how-to
---
**Symptom.** In the Conformity workflow on `main`, the conformity checks pass, "Upload site" succeeds, and the Deploy step of "Deploy to Pages" fails within a second with `Found 1 artifact(s)` and `No artifacts named "github-pages" were found for this workflow run`. "Deploy to S3 and CloudFront" and "Submit changed URLs to IndexNow" are skipped, so the live site stays on the previous build.

**Cause.** `actions/deploy-pages` lists the run's artifacts once, through the artifact service, and stops when `github-pages` is not among them. On 2026-11-25 that list lagged the upload by seconds, and five of seven deploys failed this way ([#252](https://github.com/uncovertechtalent/machinebehavior.io/issues/252)). The one artifact it found was the conformity record, uploaded earlier by job 1. The site and its artifact were fine: a fresh run of the same commit deployed.

The workflow now waits before the deploy (step 6 of job 2 in [Deploy pipeline](doc:eng/deploy-pipeline)), polling the run's REST artifact list for up to 150 seconds. That list stands in for the one the action reads, so the wait narrows the race and does not close it, and it never stops the deploy itself.

## Steps

1. **Check the log.** Open the failed run, the "Deploy to Pages" job, the Deploy step. The two lines above confirm this failure; the "Wait until the Pages artifact is listed" step prints how long it waited and how many of its API calls failed (`github-pages listed after N s (F failed calls)`), or a warning after 150 seconds with the last error.
2. **Do not re-run the "Deploy to Pages" job or the whole workflow:** neither "Re-run failed jobs" nor "Re-run all jobs" on the run page, nor `gh run rerun` with or without `--failed`. Each runs "Upload site" again, which adds a second `github-pages` artifact to the same run, and the deploy then stops with `Multiple artifacts named "github-pages" were unexpectedly found` (seen on 2026-11-25 in the second attempt of [run 45615883287](https://github.com/uncovertechtalent/machinebehavior.io/actions/runs/45615883287)).
3. **Start a fresh run on `main`,** unless one is already queued or running: the workflow does not cancel a run in progress on `main` ([Roll back a deploy](doc:eng/runbook-rollback)), and on a day with several merges a later push run may already be deploying the same `main`. Check first, and wait for that run if there is one:

   ```bash
   gh run list -R uncovertechtalent/machinebehavior.io --workflow conformity.yml --branch main --limit 5
   ```

   Otherwise:

   ```bash
   gh workflow run conformity.yml -R uncovertechtalent/machinebehavior.io --ref main
   ```

   A run started by hand from `main` deploys the current `main` ([Roll back a deploy](doc:eng/runbook-rollback) explains why), so it also carries every merge since the failed run.
4. **Confirm the deploy:** the new run's "Deploy to Pages" is green, then "Deploy to S3 and CloudFront" when it runs (only while the repository variable `S3_DEPLOY` is `on`), and the page that changed shows the change on the live site.
5. **If it keeps failing after the wait step printed `listed after N s`** (any N), the wait is not enough: note the runs in [#252](https://github.com/uncovertechtalent/machinebehavior.io/issues/252). The next change is a second attempt of the deploy step in the workflow.
