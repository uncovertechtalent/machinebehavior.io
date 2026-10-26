title: Site navigation and chrome
summary: One navigation source, site/nav.yml, writes the top bar, the breadcrumbs, the section sidebars and the footer of every page, and checks the sitemap and llms.txt against the tree.
order: 64
labels: navigation, frontend, site, breadcrumbs
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
created: 2026-10-09
updated: 2026-10-26
type: reference
---
machinebehavior.io is one portal: "Machine Behavior" is the site, Inside is the portal within it. Every page carries the same top bar, breadcrumbs from Home to the page, and the same footer. The sections and their pages are defined once, in `site/nav.yml`; `scripts/site_chrome.py` writes the chrome of every page from that file.

## Sections

| Section | Front page | Pages |
|---|---|---|
| Home | `/` | |
| Research | `/research/` | claims, experiments, objections, evidence, slips, case files, articles, man pages, terms |
| Conformity | `/conformity/` | the gate runs, the working-draft standard and the self-assessment |
| Inside | `/inside/` | Mission Control, services (one page per service, from `services/*.yml`), status, board, gate runs, tour, search |
| Docs | `/inside/docs/` | the space tree, from `inside/docs/tree.json` (written by `scripts/build_docs.py`) |
| Topics | `/topics/` | one hub per topic in `site/topics.yml` |
| Map | `/map/` | |

`/research/` is built by `scripts/build_hubs.py` from the same file: every research page in its group, with the description the page gives itself. It also writes each `hub: true` page, a group's index (/research/case-files/, /research/articles/, /research/registers/ and /research/reference/), and the topic hubs.

## site/nav.yml

```yaml
sections:
  - key: research
    title: Research
    url: /research/
    pages:
      - group: Case files          # a sidebar heading that folds out; no page, no breadcrumb
        pages:                     # one page, the group's index, with the group's pages under it
          - title: Case files
            url: /research/case-files/
            side: All case files   # the sidebar's name for the page, when it differs from the title
            hub: true              # a list of its pages, written by scripts/build_hubs.py
            order: newest          # its pages newest first by published; each needs a date
            about: Single incidents, each written up from its record.
            pages:
              - title: "Case 12: a licence rule mid-task"
                url: /research/case-files/case-12-licence-rule-mid-task/
                published: 2026-10-03
      - group: Red team
        include: red-team          # another section's overview and pages; that section's pages show this sidebar
      - group: Reference
        pages:
          - title: Reference
            url: /research/reference/
            side: All reference texts
            hub: true
            pages:
              - link: Topics       # a link in the sidebar only, not a page of this section
                url: /topics/
  - key: inside
    title: Inside
    url: /inside/
    banner: true                   # the public-demo strip on app pages of this section
    pages:
      - title: Services
        url: /inside/services/
        auto: services             # one child per service, from inside/services/services.json
```

`title` is the name in the breadcrumbs and the sidebar. `url` is a root-absolute page path, or an anchor on a page (`/inside/#dashboards`), which appears in the sidebar but is not a page. `legal` holds the Impressum and privacy links for the footer ([#10](https://github.com/uncovertechtalent/machinebehavior.io/issues/10), [#11](https://github.com/uncovertechtalent/machinebehavior.io/issues/11)); the two pages sit under the home entry.

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

Research and Inside pages carry the section sidebar (`SIDEBARS` in `scripts/site_chrome.py`): every page of the section in the order of `site/nav.yml`, the current page marked, Services as a disclosure open on a service page. Groups are headings that fold out one at a time: each is a `<details name="mb-side">`, so opening one closes the others with no script, and the group holding the current page is open on load. Each group opens with its index page ("All case files"), then at most five of the index's pages (`SIDE_RECENT`), newest first where the index says `order: newest`, plus the current page when it is older; the rest are on the index page. A group with `include:` lists another section, whose pages then show this sidebar (`SIDEBAR_HOST`): the red-team pages show the research sidebar. Sidebars do not list the topics; Topics is in the top bar's More menu and a link in the research sidebar's Reference group. From 1100 px it is a sticky column of 264 px beside the content; below that it is a disclosure above the content, closed on load by `/inside/bar.js`. Docs pages keep the space tree from `scripts/build_docs.py`. See [ADR-0022](doc:eng/adr-0022-section-sidebars), [ADR-0044](doc:eng/adr-0044-sidebar-accordion-groups) and [ADR-0045](doc:eng/adr-0045-sidebar-groups-open-with-an-index).

## Topics

`site/topics.yml` holds the topics and the rules that select their members: hand-written and Inside pages, docs labels and spaces, tag pages on the map, words in Substack titles, and board labels or words. `scripts/build_hubs.py` builds the hubs at `/topics/<key>/`, the index at `/topics/` and `/topics/topics.json`, then writes the chrome of every page again. See [ADR-0023](doc:eng/adr-0023-topic-hubs).

Build order: `build_docs.py`, `build_inside.py`, `build_hubs.py`; then `site_chrome.py --check`. `build_hubs.py` also runs `build_fallbacks.py`, which writes static versions of the lists that Inside, the board and Mission Control fill in the browser (between `<!-- static:NAME -->` markers), so the pages read the same without JavaScript.

## Home page

The front page carries the report theme and one lead finding chosen by hand in `index.html`. `scripts/build_fallbacks.py` writes two blocks between `<!-- static:home-... -->` markers: the doors, one per section in `HOME_DOORS` with its `door:` line from `site/nav.yml`, and `HOME_ROWS` research rows, the newest published pages whose kind pill is in `HOME_KINDS`, leaving out the lead. See [ADR-0041](doc:eng/adr-0041-front-page-in-the-report-theme), which replaces [ADR-0028](doc:eng/adr-0028-home-page-portal-front).

## Structured data

The head block also holds one JSON-LD graph per page: Stefan Coetzee as Person (from `site.person`), the site as WebSite with its search, the page as Article, TechArticle, CollectionPage or WebPage with headline, description and dates, and DefinedTermSet on `/research/terms/` and `/conformity/standard/` with the wording on the page. A research page's publication date sits in `site/nav.yml` as `published`. `--check` fails on a JSON-LD block that does not parse. See [ADR-0027](doc:eng/adr-0027-structured-data).

## Layouts

Two layouts under one brand. The reading layout keeps the serif column of the research pages (`/style.css`, `<div class="sheet">`, teal accent). The app layout keeps the portal look of Inside, Docs and the map (amber accent). `apply()` picks the layout from the stylesheet the page loads and sets `mb-read` or `mb-app` and `mb-s-<section>` on `<body>`. Every page is light, whatever the system setting ([ADR-0042](doc:eng/adr-0042-one-light-scheme)); the research section and the front page carry the report theme ([ADR-0039](doc:eng/adr-0039-research-report-theme), [ADR-0041](doc:eng/adr-0041-front-page-in-the-report-theme)) and Inside the intranet theme ([ADR-0035](doc:eng/adr-0035-intranet-theme-on-every-inside-page)). The styles are in `/design/`: `tokens.css` (colour, type, spacing; the older page variables map onto it), `chrome.css` (bar, breadcrumbs, sidebars, footer, layouts) and `components.css` (page header, pills, cards, panels, tables, lists). See [ADR-0025](doc:eng/adr-0025-one-design-system).

Hand-written pages show their owner and the date from `sitemap.xml` beside the breadcrumbs; generated pages carry their own byline.

Related: [Top bar and search](doc:eng/top-bar-and-search), [Add a page to machinebehavior.io](doc:eng/add-a-page), [ADR-0021](doc:eng/adr-0021-one-navigation-source).
