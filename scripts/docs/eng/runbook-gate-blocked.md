title: Gate blocked a deploy
summary: The conformity job failed, so the deploy did not run and the previous build is still live; find the failing check, fix the page, push again.
parent: runbooks
order: 10
labels: runbook, gate
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: how-to
---
**Symptom.** The Conformity workflow is red; the "Deploy to Pages" job shows as skipped; the live site still shows the previous build.

## Steps

1. Open the failed run, or run the dry run locally: the last line names each check with its result.
2. Read the failing check's evidence lines at [/conformity/](/conformity/) or in `conformity/latest.json`. Each line names the file and the reason.
3. Fix by type:
   - `site.consistency`: add the missing sitemap entry or canonical link, or make the link root-absolute.
   - `placeholders`: replace the placeholder with the real text or remove it.
   - `rules.blocking`: rewrite the sentence. If the hit is a false positive, record it with the gate owner as well.
   - `predictions.hashes`: a hashed prediction changed. Restore the file; predictions are never edited after hashing.
4. Run the dry run until it prints `overall=pass`, then `git pull --rebase` and push.

> [!warning] A chained command such as `grep -o 'overall=[a-z]*' && git push` pushes on a failing run, because `grep` succeeds on `overall=fail`. Compare the value: `[ "$R0" = "overall=pass" ] && git push`. This happened on 2026-10-08; the gate blocked the deploy.
