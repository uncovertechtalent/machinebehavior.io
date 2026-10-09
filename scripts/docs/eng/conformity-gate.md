title: Conformity gate
summary: The checks every page passes before a deploy: blocking rule hits, placeholders, prediction hashes and site consistency, with warnings logged.
order: 30
labels: conformity, gate, quality
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: reference
---
The conformity gate is a set of mechanical checks run by `.github/actions/conformity/run.py` against every published page. A blocking failure stops the deploy; the previous build stays live. Results are rendered at [/conformity/](/conformity/) (self-assessment, not a certification) and stored in `conformity/latest.json`.

## Blocking checks

| Check | Fails when |
|---|---|
| `rules.blocking` | A page hits a rule in the blocking tier of the vendored rule table (`service-closer`, `filler-idiom`, `hook-opener`) |
| `placeholders` | A page carries placeholder text; the patterns are in `site-tier.json` under `placeholder_pattern` |
| `predictions.hashes` | A file in `predictions/` differs from the sha256 in `predictions/HASHES.txt` |
| `site.consistency` | A page is missing from `sitemap.xml`, has no canonical link, or links internally with a relative or `.html` path |
| `page.label` | A page says self-assessment near the top without the words "not a certification" |
| `components` | The vendored rule table differs from the sha256 recorded in the site configuration |

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
