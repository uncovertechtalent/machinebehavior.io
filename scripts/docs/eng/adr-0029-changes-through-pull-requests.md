title: ADR-0029: Changes reach main through pull requests
summary: Every change to main goes through a pull request whose Conformity checks pass, enforced by a branch ruleset on main; the merge is the review step; the gate bot and the probe record push through deploy keys.
parent: decision-log
order: 29
adr: 29
status: accepted
created: 2026-10-11
labels: adr, decision, sdlc, review, agents
owner: Stefan Coetzee
reviewed: 2026-10-12
review_by: 2027-01-10
type: explanation
---
## Context

The lifecycle audit of 2026-10-11 ([Software delivery lifecycle](doc:eng/sdlc)) found the review stage missing: branch protection off, no pull request template, and several agent sessions pushing to `main` directly. The gate ([ADR-0002](doc:eng/adr-0002-deploy-is-gated)) checks wording, links and records on every push; it does not read a change for what it was meant to do. Every human and agent commit in this repository uses one GitHub account, and GitHub never counts an author's approval of their own pull request, so a required approval could never be met.

## Decision

Stefan Coetzee, 2026-10-11:

- Every change reaches `main` through a pull request from a branch.
- A branch ruleset on `main` requires a pull request and a passing Conformity checks job, blocks force pushes and deletion of the branch, and requires no approvals. A branch need not be up to date before the merge, because the gate bot moves `main` after every run.
- The conformity workflow runs on every pull request to `main` and checks the merge result. A pull request run commits nothing and deploys nothing.
- The merge is the review step. Before asking for the merge, the session runs `sdlc:change-review` on the pull request and puts the review in the description. Stefan Coetzee merges, or a session merges on his go. The shared agent settings ask before `gh pr merge` in every permission mode ([Agents in this repository](doc:eng/agents)).
- Two writers keep pushing to `main` directly, each through a deploy key, the only bypass the ruleset allows: the conformity bot (`conformity/latest.json` and the page after each run, key in the secret `CONFORMITY_PUSH_KEY`) and the weekly decision-layer probe record. The built-in GitHub Actions app cannot be a ruleset bypass actor, so the bot pushes with a deploy key in place of the workflow token.

## Consequences

- A session branches from `origin/main`, runs the gate dry run, pushes the branch and opens a pull request. Once the ruleset is on, a push to `main` by a person or a session is rejected ([Push rejected](doc:eng/runbook-push-rejected)).
- A rollback is a revert pull request. It waits for one more check run than a direct push did ([Roll back a deploy](doc:eng/runbook-rollback)).
- GitHub records every merge under the one account, so it cannot tell a session's merge from Stefan's. The ask rule holds only sessions started in this repository; a session started in another folder does not load its settings.
- A pull request runs its own copy of the workflow and the gate: a pull request that edits `.github/` or `conformity/site-tier.json` can loosen the gate and pass its own required check. A required review for those paths would need a second account, so the merge is the only control: the person merging reads every change there first. A pull request from a fork runs with a read-only token; one from a branch of this repository runs with the workflow's write permissions.
- A manual run (`workflow_dispatch`) from a branch runs that branch's workflow file and, since #70 loads the gate with `uses: $/...`, that branch's gate code against main. The workflow gives the deploy key to the checkout, makes the bot commit and runs the deploy job only when `github.ref` is `refs/heads/main`, and the `github-pages` environment allows deployments only from `main` and `gh-pages`. The guard stops accidents only: a writer who edits the branch's workflow can remove it, and `CONFORMITY_PUSH_KEY` is a repository secret, which a run on any branch can read, so such a run could still push `latest.json` to main. Open step, a settings change for Stefan Coetzee: move `CONFORMITY_PUSH_KEY` to an environment secret of an environment limited to `main` (for example `conformity-bot`), then give the conformity job that environment on runs other than pull requests. A branch run then never receives the key. Tracked in #76.
- Until the deploy key and the ruleset exist, the flow is a convention that the shared settings and `CLAUDE.md` describe. Before the ruleset goes on, both keys are checked: the probe record's key is a deploy key with write access (checked 2026-10-11), and the conformity bot's key is in place and its next commit reached `main`. The bypass covers every deploy key of the repository; removing the probe key's bypass would stop the weekly record.
