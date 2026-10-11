title: Software delivery lifecycle
summary: The stages a change moves through on machinebehavior.io, from request to a live page and back, with the entry and exit criteria, the owner and the record of each stage, and the stages with no practice yet.
order: 15
labels: sdlc, process, delivery
owner: Stefan Coetzee
reviewed: 2026-10-11
review_by: 2027-01-09
type: reference
---
Every change to machinebehavior.io moves through the stages below, in this order. The site serves readers, so a stage that fails lets a reader see a wrong or broken page. A stage is done when its exit criteria hold and its record exists. Each record links the one before it, so a line on a live page traces back to the issue that asked for it.

The branch model is short-lived branches and pull requests to `main` ([ADR-0029](doc:eng/adr-0029-changes-through-pull-requests)): agent sessions and the operator branch from `origin/main`, push the branch and open a pull request; a passing Conformity checks job is required before the merge. Only two automated writers push to `main` directly, through deploy keys. Only the workflow deploys, on a push to `main` that passes the conformity gate ([ADR-0002](doc:eng/adr-0002-deploy-is-gated)). Releases are continuous, several deploys a day.

## Stages

| Stage | Entry | Exit | Owner | Record | Served by |
|---|---|---|---|---|---|
| Request | Someone needs a change, or a reader reports a problem | An issue with a type, an area and a priority label; scoped issues carry `status: ready` | Stefan Coetzee | GitHub issue on [uncovertechtalent/machinebehavior.io](https://github.com/uncovertechtalent/machinebehavior.io/issues) | Issue templates in `.github/ISSUE_TEMPLATE/`, triage per [Ticket board](doc:eng/board), `sdlc:ticket` |
| RFC | The change touches more than one site or the shared gate, or is hard to undo | A decision record with status `accepted` | Stefan Coetzee | Decision record with status `proposed` | No comment round; see Gaps |
| Decision | A choice was made that others need to know | Decision record with status `accepted` | Stefan Coetzee | `scripts/docs/eng/adr-NNNN-*.md`, listed in [Decision records](doc:eng/decision-log) | Numbered records ([ADR-0018](doc:eng/adr-0018-numbered-records-and-changelog)); the docs build checks numbers and supersede links |
| Build | Issue in `status: ready`; whoever picks it up assigns it and sets `status: in progress` | Commits on a branch from `origin/main`, pushed, a pull request open with the template | Stefan Coetzee | Commits, pull request | Agent sessions, `sdlc:work-item`, `.github/pull_request_template.md` |
| Review | Pull request open, Conformity checks passed on it | The change review is in the pull request description; Stefan Coetzee merges, or a session merges on his go | Stefan Coetzee | Pull request with the review and the merge | `sdlc:change-review`; the shared agent settings ask before `gh pr merge` ([Agents in this repository](doc:eng/agents)) |
| Test | Code or a page changed | The gate dry run prints `overall=pass`; the docs build finishes without stopping | Stefan Coetzee | Local dry run output | Gate dry run, checks in `scripts/build_docs.py` ([Docs tree](doc:eng/docs-tree)) |
| Gate | Pull request to `main` (required check), then the push to `main` the merge makes | The Conformity checks job passes | Stefan Coetzee | Workflow run and its artifacts (90 days), `conformity/latest.json` in git | [Conformity gate](doc:eng/conformity-gate), `.github/workflows/conformity.yml` |
| Release | Gate passed | The Deploy to Pages job succeeded; the rollback path is known | Stefan Coetzee | Deploy run in the `github-pages` environment, [changelog](doc:eng/changelog) | [Deploy pipeline](doc:eng/deploy-pipeline), [Roll back a deploy](doc:eng/runbook-rollback), `sdlc:release` |
| Observe | Deployed | The [status page](/inside/status/) shows the site as operational and the Website deploys dashboard shows the run green | Stefan Coetzee | `/inside/deploys.json`, the [Website deploys dashboard](https://grafana.scoetzee.de/public-dashboards/e0f6a0c8f3a64884a67faac5cf4c3ad4) | [Deploy exporter](doc:obs/deploy-exporter), [Status page](doc:eng/status-page) |
| Incident | A reader-visible symptom, a failed gate run, or an alert someone sees | Record resolved, write-up linked under `postmortem`, follow-up work as issues under `tickets` | Stefan Coetzee | `incidents/YYYY-MM-DD-short-name.yml` | [Status page](doc:eng/status-page), [On-call and escalation](doc:obs/on-call) |

Follow-up work from an incident goes back to Request as issues, listed in the record's `tickets` field.

## Gaps

Stages with no module or practice yet:

| Stage | What is missing | Fills it |
|---|---|---|
| RFC | No comment round before a decision; a record goes from `proposed` to `accepted` on the operator's call | `decisions:rfc`, or comments on the issue that links the proposed record |
| Review | No second person: every commit and every merge comes from one GitHub account, so GitHub cannot require an approval or tell a session's merge from Stefan's. The ask rule on `gh pr merge` holds only sessions started in this repository. The branch ruleset waits for the deploy key of the conformity bot | The ruleset per [ADR-0029](doc:eng/adr-0029-changes-through-pull-requests); a second account for reviews if one is ever needed |
| Test | No unit tests for the Python generators in `scripts/`, and no check after a deploy that the pages answer | `sdlc:test-strategy` |
| Build | Commit subjects do not name the issue or the decision, so a commit cannot be traced to its request | `sdlc.traceability` gate check on `warn` with `since: 2026-10-11` |
| Release | No way to redeploy an earlier build: both jobs check out `main`. Rollback time is not measured | Owner decision; see [Roll back a deploy](doc:eng/runbook-rollback) |
| Observe | No SLO for the site, and no alert reaches a person ([ADR-0017](doc:eng/adr-0017-on-call-model)) | `reliability:slo`; the proposed routing in [On-call and escalation](doc:obs/on-call) |

## Tickets

GitHub Issues on [uncovertechtalent/machinebehavior.io](https://github.com/uncovertechtalent/machinebehavior.io/issues) is the system of record; the [board](/inside/board/) is a read-only view of it. Labels, as set at triage by a maintainer:

| Group | Labels | Meaning |
|---|---|---|
| Type | `type: feature`, `type: bug`, `type: chore`, `type: docs` | What kind of work. An issue without a type label is untriaged and the board does not show its text |
| Area | `area: inside`, `area: docs`, `area: map`, `area: gate`, `area: observability`, `area: legal`, `area: security`, `area: search` | Which part of the platform. An issue can carry more than one |
| Priority | `P0`, `P1`, `P2`, `P3` | P0 must close before anyone outside sees the platform; P3 is optional |
| Status | `status: ready`, `status: in progress`, `status: blocked` | The board column. No status label means Backlog; closed means Done |

The issue templates set no labels, so a new report stays untriaged until a maintainer reads it. Close an issue with a comment that links the commit. Issue text is public: no private addresses, host names, personal or financial details.

Commit subjects should name the issue (`#123`) or the decision (`ADR-0007`). Commits before 2026-10-11 do not.

## Test strategy

| Level | What it covers | Where it runs |
|---|---|---|
| Unit | None yet for the generators in `scripts/` | Nowhere |
| Build checks | `scripts/build_docs.py` stops on a malformed date, an unknown page type, an unknown `doc:` link, or decision records that disagree | Locally, when the docs are built |
| Gate | Blocking rule hits, placeholders, prediction hashes, site consistency, page labels, the vendored rule table | Locally as a dry run; in the workflow on every push to `main` |
| Smoke | None after a deploy. The status page reads each site's `/conformity/latest.json` in the visitor's browser and shows a site that does not answer as an outage | Nowhere in the pipeline |

Before pushing a branch, run:

```bash
git fetch origin && git rebase origin/main
python3 .github/actions/conformity/run.py --root . --config conformity/site-tier.json \
  --requirements conformity/requirements.json --out conformity --dry-run
```

Push the branch only when the dry run prints `overall=pass`. In a script, compare the value; a `grep` for `overall=` succeeds on a failing run too. The same checks run on the pull request before the merge.

## Release and rollback

- Changelog: [changelog](doc:eng/changelog), generated by `scripts/build_changelog.py` from closed issues and commits, by day, grouped Added, Changed and Fixed. There are no version tags.
- Rollback: [Roll back a deploy](doc:eng/runbook-rollback).
- Feature flags: none in this repository.
