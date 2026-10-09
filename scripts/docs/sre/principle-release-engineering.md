title: Every change passes the same gate
summary: Release engineering makes every change go through one repeatable, recorded path, with builds that give the same output wherever they run. Here one workflow gates and deploys three sites and records every run; the generated pages are built on the author's machine, and the observability stack has no pipeline.
parent: principles-in-practice
order: 90
labels: principle, sre, release, ci-cd, deploy, gate
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
state: partial
source: [Pillar 6, CI/CD and deployment](doc:sre/cicd-deployment); [Google SRE book ch. 8](https://sre.google/sre-book/release-engineering/)
---
## The principle

Releases should be frequent, small and boring. Every change goes through the same path: a build that gives the same output from the same input on any machine, the same checks, the same deploy step, and a record of who changed what and when. Policy lives in the pipeline, so nobody has to remember it. Progressive delivery (canary, blue-green, feature flags) limits how many users a bad change reaches.

Source: [CI/CD & Deployment](doc:sre/cicd-deployment) and [Progressive Delivery Patterns](doc:sre/progressive-delivery-patterns); Google's [Release Engineering](https://sre.google/sre-book/release-engineering/).

## On this platform

- **One path for every change.** Every push to `main` runs one workflow with two jobs: the conformity checks, then the deploy to Pages, which runs only when the checks pass ([Deploy pipeline](doc:eng/deploy-pipeline), [ADR-0002](doc:eng/adr-0002-deploy-is-gated)). It also runs every Monday at 06:17 UTC and by hand.
- **One gate for three sites.** machinebehavior.io, tychat.io and uncovertechtalent.com run the same composite action, so a rule change reaches all three ([Conformity gate](doc:eng/conformity-gate)).
- **A failed check is a safe state.** When a check fails, the deploy does not run and readers keep the previous build. On 2026-10-08 a link in a template string failed the check; the fix passed 81 seconds later and nobody outside saw the broken page ([incident record](/inside/status/#2026-10-08-gate-blocked-map-push), [runbook](doc:eng/runbook-template-href)).
- **Every run is recorded.** The gate commits its result to `conformity/latest.json`; run artifacts are kept 90 days; the [deploy exporter](/inside/services/deploy-exporter/) writes each run, step and check to Loki and Prometheus, and the [Website deploys](https://grafana.scoetzee.de/public-dashboards/e0f6a0c8f3a64884a67faac5cf4c3ad4) dashboard shows them.
- **High change rate.** Several agent sessions push the same repository through the gate many times a day: 69 recorded runs between 2026-10-07 and 2026-10-09.
- **Rollback.** Undoing a live change is a revert pushed through the same gate. The handbook's [rollback runbook](doc:sre/rollback-deployment) is generic; the sites have no runbook of their own for it.

## State

**Partial.** The gate and the deploy path are in place and recorded. Two parts are missing. The generated pages (docs, services, status) are built on the author's machine and committed; CI does not rebuild them, so a source edited without a build, or generated HTML edited by hand, deploys unnoticed ([#40](https://github.com/uncovertechtalent/machinebehavior.io/issues/40)). And the observability stack has no pipeline: it is copied to its server by hand, with no gate in front of it ([Eliminate toil](doc:sre/principle-eliminate-toil)). Canary releases are not used: Pages replaces the whole site at once, and the risk on a text site sits in the content, which the gate checks.

## Services that name it

<!-- principle-services -->

## In a company of 10 to 200 people

- One pipeline per repository, the same stages for every team, and the deploy step only reachable through it.
- Build once in CI from a clean checkout and deploy exactly that artifact to every environment.
- Make rollback a deploy of the previous artifact, and practise it until it takes minutes.
- Add canaries and feature flags when there is traffic to split and a metric to judge the canary by.

## Open work

- [#40 CI check: generated pages match their sources](https://github.com/uncovertechtalent/machinebehavior.io/issues/40)
- [#39 Toil: the bot commit on main forces a rebase before every push](https://github.com/uncovertechtalent/machinebehavior.io/issues/39)
