title: Conformity gate
summary: The checks every page passes before a deploy: blocking rule hits, placeholders, prediction hashes, site consistency, and pinned actions from listed owners, with warnings logged.
order: 30
labels: conformity, gate, quality
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
created: 2026-10-09
updated: 2026-10-23
type: reference
---
The conformity gate is a set of mechanical checks run by `.github/actions/conformity/run.py` against every published page. A blocking failure stops the deploy; the previous build stays live. Results are rendered at [/conformity/](/conformity/) (self-assessment, not a certification) and stored in `conformity/latest.json`. The requirements under test come from the working draft published at [/conformity/standard/](/conformity/standard/) ([ADR-0019](doc:eng/adr-0019-definition-published-before-committee)).

## Blocking checks

| Check | Fails when |
|---|---|
| `rules.blocking` | A page hits a rule in the blocking tier of the vendored rule table (`service-closer`, `filler-idiom`, `hook-opener`) |
| `placeholders` | A page carries placeholder text; the patterns are in `site-tier.json` under `placeholder_pattern` |
| `predictions.hashes` | A file in `predictions/` differs from the sha256 in `predictions/HASHES.txt` |
| `site.consistency` | A page is missing from `sitemap.xml`, has no canonical link, or links internally with a relative or `.html` path |
| `page.label` | A page says self-assessment near the top without the words "not a certification" |
| `components` | The vendored rule table differs from the sha256 recorded in the site configuration |
| `actions.pinned` | A workflow or composite action under `.github/` references an outside action by tag, branch or short SHA, or a Docker image by tag; a commit SHA cannot be moved to other code |
| `actions.owners` | An outside action, reusable workflow or Docker image comes from an owner outside `actions_owners_allow` in `site-tier.json`; a pinned commit from a lookalike repository still passes `actions.pinned` |

## Local check (dry run only)

| Check | Fails when |
|---|---|
| `private.terms` | A tracked file, a file name or a published file of the build output carries a term from the owner's private term list: names of prospective employers or clients, internal shorthand, family names in business copy, private hosts and addresses |

The term list stays on the owner's machine, outside every repository, so this check runs only in a dry run with `--private-terms <file>`, never in CI, and never appears on [/conformity/](/conformity/). A pushed commit is public before CI runs; the owner's pre-push hook from the CTO powersuit (`security.private-terms`) is what stops a term before it leaves the machine. Hits show the file, the line and the term's label, never the term. Intended mentions go into `.private-terms-allow` at the repository root: a path glob, a label, and a reason. The matcher runs on every CI run against made-up terms in `fixtures-private-terms.jsonl`, through `grader.fixtures`.

## Warnings (never block)

- `praise-opener` rule hits.
- A page missing from `llms.txt`.
- Freshness: pages whose newest date is older than 90 days, or with no date.

## Exemptions from the rule scan

Code, blockquotes, `<q>`, spans with class `mono` and text inside double quotes. Quote a phrase to discuss it; the scan skips it.

## Records

- Run records: workflow artifacts, kept 90 days.
- History and open findings: `conformity/latest.json` in git, kept indefinitely. A finding closes only when a later run passes.

## Ownership and false positives

The legislation-track session owns the gate; Stefan Coetzee decides tier changes. A false positive is never fixed by editing the rule table in the site repository. Record the page, line and rule with the owner; rewriting the sentence unblocks the deploy in the meantime. See [Gate blocked a deploy](doc:eng/runbook-gate-blocked).

## Sites that share the gate

tychat.io and uncovertechtalent.com run this gate pinned to a commit of main. A change to `.github/actions/conformity/`, an engine fix included, reaches them only when the gate owner bumps that commit in both repositories. Dependabot does not propose the bump, because this repository has no release tags. The bump step is in `conformity/README.md`.
