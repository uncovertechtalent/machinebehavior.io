title: ADR-0021: One navigation source for the whole site
summary: site/nav.yml defines the sections and pages once; scripts/site_chrome.py writes the top bar, breadcrumbs, sidebar and footer of every page between markers and checks the sitemap and llms.txt against the tree.
parent: decision-log
order: 21
adr: 21
status: accepted
created: 2026-10-09
labels: adr, decision, navigation
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

The site had two menus. Research pages carried a hand-copied list of eight links; Inside pages carried the top bar from `scripts/inside_chrome.py` ([ADR-0012](doc:eng/adr-0012-one-top-bar-and-search)). The two halves read as two sites, the research pages had no breadcrumbs, the docs breadcrumbs started at Docs, and nothing checked that a page in the sitemap was reachable from a menu. Stefan Coetzee asked on 2026-10-09 for the site to work like an online portal: breadcrumbs on every page and a sidebar by section.

## Decision

One file, `site/nav.yml`, defines the sections (Home, Research, Inside, Docs, Map) and their pages. The docs tree and the service catalog are added from the files their builds write. `scripts/site_chrome.py` writes, on every page, the top bar, the breadcrumbs (visible, plus a JSON-LD `BreadcrumbList`), the section sidebar and one footer, each between `<!-- mb:NAME -->` markers. Page content outside the markers stays as written. The generators call the same function; the deploy job runs it once more before the upload, for pages that a generator outside this repository rewrites (the gate's `/conformity/`). The same run reports orphans and checks `sitemap.xml` and `llms.txt` against the tree. Details: [Site navigation and chrome](doc:eng/site-navigation).

URLs do not change. GitHub Pages cannot redirect, so Docs stays under `/inside/docs/` while it is a top-level section in the bar and the breadcrumbs. The one new URL is `/research/`, the front page of the Research section, which the breadcrumbs need.

## Consequences

A new page needs an entry in `site/nav.yml`; without one it is reported as an orphan and gets breadcrumbs of Home and its title only. Copying a menu into a page is no longer possible: the old research menu is removed on the next run. The top bar is dark in both colour schemes, so it reads the same on the light reading pages and the dark app pages. `/conformity/` in the repository lacks the chrome between a gate run and the next deploy; the deployed page has it. A gate check that every page carries the blocks and that the breadcrumbs match the tree is a later step.
