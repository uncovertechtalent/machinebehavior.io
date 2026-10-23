title: ADR-0038: URL taxonomy and redirects
summary: The site adopts a small set of top-level pillars (Research, Conformity, Inside, Docs) with the CTO page as the action, nests the flat root registers and reference under their pillar, consolidates the three conformity routes under one /conformity/ hub, and freezes the URLs that carry external or legal weight. Moved URLs redirect two ways from one source, site/redirects.yml: a CloudFront 301 at the edge and a GitHub Pages stub with a canonical link. The decision is accepted; the moves land in phases 1 to 3.
parent: decision-log
order: 38
adr: 38
status: accepted
created: 2026-10-23
labels: adr, decision, information-architecture, urls, redirects, navigation
owner: Stefan Coetzee
reviewed: 2026-10-23
review_by: 2027-01-21
type: explanation
---
## Context

The site grew by accretion to about 490 URLs. Around 24 content routes sit flat at the root and mix five kinds of thing at one depth: program sections (`/research/`, `/red-team/`, `/aieo/`), proof registers (`/claims/`, `/experiments/`, `/objections/`, `/evidence/`, `/slips/`), reference (`/terms/`, `/man/`), single articles and case files, trust and legal (`/conformity/`, `/continuous-conformity/`, `/continuous-conformity-self-assessment/`, `/impressum/`, `/privacy/`), and navigation aids (`/topics/`, `/map/`). A local crawl of the built HTML shows the section hubs draw fewer inbound body links than their own children: `/research/` has 3, against 21, 27, 17, and 14 for its registers. The three conformity routes read as near-duplicates and sit in two different sections of the navigation.

[ADR-0001](doc:eng/adr-0001-root-absolute-links) fixed root-absolute links, and GitHub Pages issues no redirects, so [ADR-0021](doc:eng/adr-0021-one-navigation-source) recorded that URLs do not change once published. [ADR-0033](doc:eng/adr-0033-s3-and-cloudfront-next-to-pages) put CloudFront in front of Pages, and its viewer-request function now issues 301s, which lifts that constraint. This record updates the "URLs do not change" clause of ADR-0021: a URL may change when it carries a redirect from both layers.

## Decision

Stefan Coetzee, 2026-10-23. The decision is accepted; the moves land in phases 1 to 3 (all merged 2026-10-23), following [ADR-0019](doc:eng/adr-0019-definition-published-before-committee), which publishes a record before the work it governs.

1. Adopt a small set of top-level pillars: Research, Conformity, Inside, and Docs, with the CTO page as the action, and Topics, Graph, Search, and AIEO as utilities off the pillar bar.
2. Nest the flat root registers and reference under their pillar: `/research/{claims,experiments,objections,evidence,slips,terms}/` and `/research/red-team/`.
3. Consolidate the three conformity routes under one `/conformity/` hub: the live gate runs stay at `/conformity/` (the page path and its canonical are fixed by the shared gate action that tychat.io and uncovertechtalent.com pin, and `conformity/latest.json` is a data contract across the three sites), `/conformity/standard/` for the working draft and its entries, and `/conformity/self-assessment/`.
4. Freeze the URLs that carry external or legal weight: the product pages (`/your-next-cto/`, `/cto-powersuit/`, for the hashed answer-engine experiment), `/man/`, the legal notices, and the high-fan-in aids `/topics/` and `/map/`. A frozen URL still gets a home: the hub lists it by link. (Revised 2026-10-23: the articles and case files, frozen here at first, now nest too; see decision 7.)
5. Record every moved URL in `site/redirects.yml`, the one source for both redirect layers. `scripts/build_redirects.py` writes a GitHub Pages stub at the old path with a canonical link to the target, a meta refresh, and robots noindex; the CloudFront viewer-request function issues the 301 at the edge from the same list.
6. Add a convenience 301 from `/services/` to `/inside/services/`, so a plausible reader URL resolves instead of returning 404.
7. Nest the research pieces by kind, and make this the convention for every new piece: articles at `/research/articles/<slug>/`, case files at `/research/case-files/<slug>/`, red team at `/research/red-team/`. Revised 2026-10-23, reversing the freeze of the articles and case files in decision 4 and Q1 of the phase-0 decisions: the cost of moving a piece grows with every citation, one rule for all pieces is simpler than a frozen set, and the canonical for these pieces is on Substack, so the site URL carries little equity. Their redirects are permanent (see Consequences).

## Consequences

- About 14 redirect pairs across the phases (phase 1 adds four, and the gate page keeps `/conformity/` so it needs none), plus the `/services/` convenience redirect.
- The gate (`.github/actions/conformity/run.py`) and the chrome pass (`scripts/site_chrome.py`) skip a file only when its path is a `from` in `site/redirects.yml` and it carries the stub shape (the `<!-- mb:redirect -->` sentinel, `noindex`, a canonical), so a stub is neither scanned as a page, flagged as an orphan, nor given a top bar, while a sentinel at an unlisted path is still scanned and fails as missing from the sitemap. Both read `site/redirects.yml` through `scripts/mini_yaml.py`, the one parser `scripts/build_redirects.py` uses, so a change to that file changes gate behaviour.
- Every generated artefact regenerates on a move: the chrome and the JSON-LD breadcrumbs on every page, the managed blocks of `sitemap.xml` and `llms.txt`, the markdown twins and the passage index that the ask-mbio server searches (a moved URL resolves to a dead passage until this is rebuilt), the Inside search index, the map graph, and the topic membership in `site/topics.yml`.
- The CloudFront rule map lives in the infrastructure repository, which the site's workflow token cannot reach, so the owner applies it per phase from a prepared patch, after the deploy that serves the new paths is live, so the edge never 301s to a page that does not exist yet.
- A move that carries non-page files (phase 1 moved the self-assessment evidence under `second-rater/` with the page) gets no Pages stub, since `scripts/build_redirects.py` writes stubs for page directories only. Those old paths return 404 on Pages and are covered at the edge by a CloudFront prefix rule from the same patch. A `prefix` kind in `site/redirects.yml`, read by both layers, is a tracked follow-up.
- The redirect stub complements the withdrawn-page pattern of [issue #23](https://github.com/uncovertechtalent/machinebehavior.io/issues/23): the stub redirects a moved page, and the withdrawal notice keeps a retired page at its URL.
- Edge prefix rules match at the start of the path only, never as a substring. Phase 3 moves `/red-team/`, whose slug also sits inside the rule's own target `/research/red-team/` and inside the frozen powersuit module `/cto-powersuit/red-team/`; a substring match would loop on the target and 301 the module. The site-infra apply checks that `/research/red-team/` and `/cto-powersuit/red-team/` both return 200. The article and case-file moves (`/the-cheating-moved/`, `/chaos-engineering-for-behaviour/`, `/running-conjobs-for-ai/`, `/case-12-licence-rule-mid-task/`) get the same start-anchored prefix rules, so their markdown twins follow.
- The article and case-file redirects are permanent. Their old URLs are cited off site, so the stub-retirement cadence of issue #23 never retires them; they carry `permanent: true` in `site/redirects.yml`. The register, conformity and red-team redirects may be retired once inbound links fade; the permanent ones never are.

## Alternatives considered

- Fix only the bar and leave the URLs flat. Rejected: the flat namespace is the main small-site signal, and a crawler reads the sitemap, not the bar.
- Move every route, including the product and legal pages. Rejected: it breaks the hashed answer-engine experiment and the legal references for no structural gain.
- Group the frozen routes in the navigation without moving their URLs. Kept for the frozen set, rejected as the whole answer, because the sitemap still shows flat peers unless the registers nest.
