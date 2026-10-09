title: Site navigation and chrome
summary: One navigation source, site/nav.yml, writes the top bar, the breadcrumbs, the section sidebars and the footer of every page, and checks the sitemap and llms.txt against the tree.
order: 64
labels: navigation, frontend, site, breadcrumbs
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: reference
---
machinebehavior.io is one portal: "Machine Behavior" is the site, Inside is the portal within it. Every page carries the same top bar, breadcrumbs from Home to the page, and the same footer. The sections and their pages are defined once, in `site/nav.yml`; `scripts/site_chrome.py` writes the chrome of every page from that file.

## Sections

| Section | Front page | Pages |
|---|---|---|
| Home | `/` | |
| Research | `/research/` | claims, experiments, objections, evidence, slips, case files, articles, man pages, terms, the continuous-conformity definition and the self-assessment |
| Inside | `/inside/` | Mission Control, services (one page per service, from `services/*.yml`), status, board, gate runs, tour, search |
| Docs | `/inside/docs/` | the space tree, from `inside/docs/tree.json` (written by `scripts/build_docs.py`) |
| Topics | `/topics/` | one hub per topic in `site/topics.yml` |
| Map | `/map/` | |

`/research/` is built by `scripts/build_hubs.py` from the same file: every research page in its group, with the description the page gives itself. The same script builds the topic hubs.

## site/nav.yml

```yaml
sections:
  - key: research
    title: Research
    url: /research/
    pages:
      - title: Claims ledger
        url: /claims/
      - group: Case files          # a sidebar heading; no page, no breadcrumb
        pages:
          - title: Running conjobs for AI
            url: /running-conjobs-for-ai/
  - key: inside
    title: Inside
    url: /inside/
    banner: true                   # the public-demo strip on app pages of this section
    pages:
      - title: Services
        url: /inside/services/
        auto: services             # one child per service, from inside/services/services.json
```

`title` is the name in the breadcrumbs and the sidebar. `url` is a root-absolute page path, or an anchor on a page (`/inside/#dashboards`), which appears in the sidebar but is not a page. `legal` holds the Impressum and privacy links for the footer; it stays empty until the business address exists ([#10](https://github.com/uncovertechtalent/machinebehavior.io/issues/10), [#11](https://github.com/uncovertechtalent/machinebehavior.io/issues/11)).

## The managed blocks

`apply(html, rel)` in `scripts/site_chrome.py` writes five blocks. Each sits between `<!-- mb:NAME -->` and `<!-- /mb:NAME -->`; everything outside the markers is page content.

| Block | Where | What |
|---|---|---|
| `head` | before `</head>` | the design-system stylesheets, a JSON-LD `BreadcrumbList` and the page's JSON-LD graph |
| `bar` | after `<body>` | skip link, top bar (brand, sections, search), and on Inside and Docs app pages the demo banner |
| `crumbs` | top of `<div class="sheet">` (reading pages) or `<main>` (app pages) | the visible breadcrumbs |
| `side` | before the sheet or `<main>` | the section sidebar |
| `foot` | before `</body>` | conformity line, page source and history, report an issue, legal links |

A page that holds the markers keeps them where they are: the map puts its breadcrumbs and footer inside its panel. A page without them gets them at the anchors above. `apply()` also removes the chrome it replaces: the old research menu (`<nav class="nav">`), the old Inside bar and banner, and the old conformity line.

The footer links the page source. A generated page names its source in `<meta name="mb-source" content="scripts/docs/eng/x.md">`; a hand-written page is its own source.

## Who calls it

| Page | How it gets the chrome |
|---|---|
| Docs | `scripts/build_docs.py` calls `apply()` for every page it writes |
| Services and status | `scripts/build_inside.py` calls `apply()`, then runs the whole-site pass |
| Slips | `scripts/slips_page.py` calls `apply()` |
| `/research/` | `scripts/build_hubs.py` calls `apply()` |
| Hand-written pages | `python3 scripts/site_chrome.py` |
| `/conformity/` | rendered by the gate on every run; the deploy job runs `scripts/site_chrome.py` before the upload |

## Commands

```bash
python3 scripts/site_chrome.py           # write the chrome on every page, then report
python3 scripts/site_chrome.py --check   # write nothing; exit 1 if a page differs, a page is outside the tree,
                                         # or a page in the tree is missing from sitemap.xml
```

The report lists orphans (an `index.html` outside the tree), pages in the tree without a file, pages missing from `sitemap.xml`, sitemap URLs outside the tree, and pages missing from `llms.txt` (a warning).

## Sidebars

Research and Inside pages carry the section sidebar (`SIDEBARS` in `scripts/site_chrome.py`): every page of the section in the order of `site/nav.yml`, groups as headings, Services as a disclosure open on a service page, the current page marked. From 1100 px it is a sticky column of 264 px beside the content; below that it is a disclosure above the content, closed on load by `/inside/bar.js`. Docs pages keep the space tree from `scripts/build_docs.py`. See [ADR-0022](doc:eng/adr-0022-section-sidebars).

## Topics

`site/topics.yml` holds the topics and the rules that select their members: hand-written and Inside pages, docs labels and spaces, tag pages on the map, words in Substack titles, and board labels or words. `scripts/build_hubs.py` builds the hubs at `/topics/<key>/`, the index at `/topics/` and `/topics/topics.json`, then writes the chrome of every page again so the Topics block in each sidebar marks the topics that list the page. The docs sidebar holds the block as `<!-- mb:topics --><!-- /mb:topics -->`. See [ADR-0023](doc:eng/adr-0023-topic-hubs).

Build order: `build_docs.py`, `build_inside.py`, `build_hubs.py`; then `site_chrome.py --check`.

## Structured data

The head block also holds one JSON-LD graph per page: Stefan Coetzee as Person (from `site.person`), the site as WebSite with its search, the page as Article, TechArticle, CollectionPage or WebPage with headline, description and dates, and DefinedTermSet on `/terms/` and `/continuous-conformity/` with the wording on the page. A research page's publication date sits in `site/nav.yml` as `published`. `--check` fails on a JSON-LD block that does not parse. See [ADR-0027](doc:eng/adr-0027-structured-data).

## Layouts

Two layouts under one brand. The reading layout keeps the serif column of the research pages (`/style.css`, `<div class="sheet">`, teal accent). The app layout keeps the portal look of Inside, Docs and the map (amber accent). `apply()` picks the layout from the stylesheet the page loads and sets `mb-read` or `mb-app` and `mb-s-<section>` on `<body>`. Light and dark follow the system setting in both layouts. The styles are in `/design/`: `tokens.css` (colour, type, spacing; the older page variables map onto it), `chrome.css` (bar, breadcrumbs, sidebars, footer, layouts) and `components.css` (page header, pills, cards, panels, tables, lists). See [ADR-0025](doc:eng/adr-0025-one-design-system).

Hand-written pages show their owner and the date from `sitemap.xml` beside the breadcrumbs; generated pages carry their own byline.

Related: [Top bar and search](doc:eng/top-bar-and-search), [Add a page to machinebehavior.io](doc:eng/add-a-page), [ADR-0021](doc:eng/adr-0021-one-navigation-source).
