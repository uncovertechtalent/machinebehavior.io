title: Runbooks
summary: Step-by-step fixes for the failures seen so far in the build and deploy of the sites.
order: 90
labels: runbook, operations
---
Each runbook covers one failure that has happened, with how to see it, the cause and the fix. Observability runbooks (Loki, Grafana) are in the [Observability space](doc:obs/runbooks).

| Symptom | Runbook |
|---|---|
| The deploy job did not run; the conformity job is red | [Gate blocked a deploy](doc:eng/runbook-gate-blocked) |
| `git push` is rejected after a successful run | [Push rejected after a deploy](doc:eng/runbook-push-rejected) |
| `site.consistency` fails with a relative link that is not in the page text | [Link check flags a template string](doc:eng/runbook-template-href) |
