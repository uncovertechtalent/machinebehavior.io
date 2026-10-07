# machinebehavior.io: notes for agents

Static site on GitHub Pages, deployed by `.github/workflows/conformity.yml`. Several sessions push this repo.

## Before every push

```bash
git pull --rebase
```

A bot commits `conformity/latest.json` and `conformity/index.html` after every run (`[skip ci]`), so HEAD moves without you. Push without the rebase and the push is rejected.

## The deploy gate

Every push to `main` runs the conformity checks first (`conformity/run.py`). The Pages deploy job depends on that job: a failing check blocks the deploy and the previous build stays live. A red run means a nonconformity on a published page, listed at https://machinebehavior.io/conformity/ and in `conformity/latest.json`.

Blocking (deploy stops): rule hits in the blocking tier (`service-closer`, `filler-idiom`, `hook-opener`; see `conformity/site-tier.json`), placeholder text on a page (`TODO`, `TBD`, `[Voice pass ...]` and the like), a prediction file whose sha256 differs from `predictions/HASHES.txt`, a page directory missing from `sitemap.xml`, a page without `<link rel="canonical">`, relative or `.html` internal links (root-absolute only: `/man/`, `/style.css`), a page whose eyebrow says self-assessment without "not a certification".

Warning (logged, never blocks): `praise-opener` hits, a page missing from `llms.txt`.

Exempt from the rule scan: code, blockquotes, `<q>`, spans with class `mono`, text inside double quotes. Quote a vestige; do not use it.

Check locally before pushing (Python 3 and Node, no network):

```bash
python3 conformity/run.py --trigger manual --dry-run
```

## Records and ownership

- Run records: workflow artifacts, 90 days. History and open findings: `conformity/latest.json` (git).
- Requirements under test and the crosswalk: `conformity/requirements.json`. Rule tiers and false-positive tests: `conformity/site-tier.json`.
- Owner of the gate: the legislation-track session (bead `vault-xyrs`, parent `vault-omu1`); Stefan Coetzee decides tier changes.
- False positive: do not edit the rule table in this repo. Note the page, line and rule in bead `vault-xyrs` (`bd update vault-xyrs --append-notes`), or message the legislation-track session. The owner records the test in `site-tier.json` and demotes the rule to warning if it fails. Meanwhile, rewriting the sentence unblocks the deploy.

New pages: `<name>/index.html`, self canonical, entry in `sitemap.xml` and `llms.txt`, root-absolute links. Page content is owned per the vault's session table; this file covers the gate only.
