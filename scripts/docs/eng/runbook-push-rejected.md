title: Push rejected after a deploy
summary: The conformity bot commits after every run, so main moves without you; rebase on it and push again.
parent: runbooks
order: 20
labels: runbook, git
---
**Symptom.** `git push` fails with "rejected, fetch first" right after a run, although nobody else pushed.

**Cause.** Every conformity run commits `conformity/latest.json` and `conformity/index.html` as `conformity-bot` with `[skip ci]`. Your local `main` is one commit behind.

## Fix

```bash
git pull --rebase
git push
```

The bot only touches those two files, so the rebase does not conflict unless you edited them by hand. The conformity page is generated; edit its configuration (`conformity/site-tier.json`) instead.
