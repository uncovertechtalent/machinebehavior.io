title: Push rejected
summary: A push to main is rejected because changes reach main through pull requests; a branch push is rejected when the branch is behind. Open a pull request, or rebase the branch.
parent: runbooks
order: 20
labels: runbook, git
owner: Stefan Coetzee
reviewed: 2026-10-11
review_by: 2027-01-09
type: how-to
---
**Symptom.** `git push` to `main` fails with "protected branch" or "Changes must be made through a pull request".

**Cause.** A branch ruleset on `main` lets only the two deploy keys push there ([ADR-0029](doc:eng/adr-0029-changes-through-pull-requests)).

## Fix: open a pull request

```bash
git switch -c <branch>
git push -u origin HEAD
gh pr create --fill
```

Your local `main` still holds the commits; reset it with `git switch main && git reset --hard origin/main` once the pull request is open. The full flow is in `CLAUDE.md`.

## Pull request behind main

The bot commit after every run moves `main`, so an open pull request falls behind. The ruleset does not require an up-to-date branch, so it can merge as it is. Rebase only when GitHub reports a conflict:

```bash
git pull --rebase origin main
git push --force-with-lease
```

The bot only touches `conformity/latest.json` and `conformity/index.html`, so the rebase does not conflict unless you edited them by hand. The conformity page is generated; edit its configuration (`conformity/site-tier.json`) instead.
