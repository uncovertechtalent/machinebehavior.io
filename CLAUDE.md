# machinebehavior.io: notes for agents

Static site on GitHub Pages, deployed by `.github/workflows/conformity.yml`. Several sessions work in this repo; changes reach `main` through pull requests only. Harness, permissions and plugins: `scripts/docs/eng/agents.md`.

## Pull request flow

1. Branch from the current main: `git fetch origin && git switch -c <branch> origin/main`.
2. Run the gate dry run (below) until it prints `overall=pass`.
3. Push the branch and open the pull request with `.github/pull_request_template.md`. Commit subjects and the title name the issue (`#123`) or the decision (`ADR-NNNN`).
4. Wait for the Conformity checks job to pass on the pull request.
5. Run `/sdlc:change-review` on the pull request and put the review in its description.
6. Merge only on Stefan Coetzee's explicit go in this session; otherwise he merges.

Never push to `main`. Two automated writers do, each with its own deploy key: conformity-bot (`conformity/latest.json` and `conformity/index.html` after every run, `[skip ci]`) and the weekly decision-layer probe record. So `main` moves without you; the merge does not need an up-to-date branch, so rebase on `origin/main` only when GitHub reports a conflict. Never name hosts or addresses here; the repo is public.

## The deploy gate

Every push to `main`, a merged pull request included, runs the conformity checks first (`.github/actions/conformity/run.py` (the composite action; shared with tychat.io and uncovertechtalent.com)). The Pages deploy job depends on that job: a failing check blocks the deploy and the previous build stays live. A red run means a nonconformity on a published page, listed at https://machinebehavior.io/conformity/ and in `conformity/latest.json`.

Blocking (deploy stops): rule hits in the blocking tier (`service-closer`, `filler-idiom`, `hook-opener`; see `conformity/site-tier.json`), placeholder text on a page (`TODO`, `TBD`, `[Voice pass ...]` and the like), a prediction file whose sha256 differs from `predictions/HASHES.txt`, a page directory missing from `sitemap.xml`, a page without `<link rel="canonical">`, relative or `.html` internal links (root-absolute only: `/man/`, `/style.css`), a page whose eyebrow says self-assessment without "not a certification".

Warning (logged, never blocks): `praise-opener` hits, a page missing from `llms.txt`.

Exempt from the rule scan: code, blockquotes, `<q>`, spans with class `mono`, text inside double quotes. Quote a vestige; do not use it.

Check locally before pushing the branch (Python 3 and Node, no network):

```bash
python3 .github/actions/conformity/run.py --root . --config conformity/site-tier.json --requirements conformity/requirements.json --out conformity --dry-run
```

## Records and ownership

- Run records: workflow artifacts, 90 days. History and open findings: `conformity/latest.json` (git).
- Requirements under test and the crosswalk: `conformity/requirements.json`. Rule tiers and false-positive tests: `conformity/site-tier.json`.
- Owner of the gate: the legislation-track session (bead `vault-xyrs`, parent `vault-omu1`); Stefan Coetzee decides tier changes.
- False positive: do not edit the rule table in this repo. Note the page, line and rule in bead `vault-xyrs` (`bd update vault-xyrs --append-notes`), or message the legislation-track session. The owner records the test in `site-tier.json` and demotes the rule to warning if it fails. Meanwhile, rewriting the sentence unblocks the deploy.

New pages: `<name>/index.html`, self canonical, entry in `sitemap.xml` and `llms.txt`, root-absolute links. Page content is owned per the vault's session table; this file covers the gate only.
