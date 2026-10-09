title: ADR-0027: Structured data on every page from the navigation source
summary: Every page carries one JSON-LD graph written by the chrome, for entity understanding (no claim that it drives AI citations): Stefan Coetzee as Person and author, the site as WebSite with its search, the page as Article, TechArticle, CollectionPage or WebPage with its dates, a BreadcrumbList, and DefinedTermSet on the two pages that define terms. The build fails on invalid JSON-LD.
parent: decision-log
order: 27
adr: 27
status: accepted
created: 2026-10-09
labels: adr, decision, structured-data, navigation
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

The site had a BreadcrumbList on every page since [ADR-0021](doc:eng/adr-0021-one-navigation-source) and one hand-written WebSite and Person block on the home page; no page said in markup who wrote it, and the canonical definitions on [Terms](/terms/) and in clause 3 of the [definition draft](/continuous-conformity/) were plain text. Stefan Coetzee wants these pages and terms to be found and attributed to him, on the honest side: every claim in the markup true and visible on the page.

Google's guidance on its AI features (developers.google.com/search/docs/fundamentals/ai-optimization-guide) says structured data is not required for them and that no special schema exists for them; it names indexable, snippet-eligible, useful pages, a good page experience and content that can be crawled without JavaScript. Google ignores llms.txt. Schema.org markup still states the author, the page type, the dates and the meaning of a term in a form that search engines and other tools can read, at little cost.

## Decision

`page_ld()` in `scripts/site_chrome.py` writes one JSON-LD graph in the head block of every page, next to the BreadcrumbList:

- **Person**: Stefan Coetzee, with the profiles in `site.person` of `site/nav.yml` (LinkedIn, Substack, GitHub, this site, X) and the job title the home page carried. One node, one `@id`, referenced as author and publisher of every page.
- **WebSite**: the site, with the site search as a `SearchAction` (`/inside/search/?q=`).
- **The page**: `Article` for research pages, `TechArticle` for docs pages, `CollectionPage` for the section and topic hubs, `WebPage` for the rest; headline, description, `datePublished`, `dateModified`, keywords, the breadcrumb by `@id`. Dates come from the page: docs front matter (created, updated), the `published` date a research page gives itself in its header (recorded in `site/nav.yml`), and the `sitemap.xml` date as the last change. A page without a publication date of its own gets none. Two pages name a model as their writer or scorer; their markup carries it as `contributor`.
- **DefinedTermSet**: on [Terms](/terms/) one DefinedTerm per entry and on the definition draft one per entry of clause 3, each with the wording on the page, read from the page at build time, so the markup cannot drift from the text.

The home page's hand-written block went into the shared Person; its subreddit links stayed out, because a community is not a profile of the person. No FAQPage markup: no page is questions and answers. `site_chrome.py` parses every JSON-LD block on every page and reports invalid JSON as an error, which fails `--check`.

## Consequences

A new page gets the markup on the next run of the chrome. A research page that states a publication date needs it in `site/nav.yml` as `published`. The legislation-track builders run the chrome after writing, so the definition draft's terms follow its text. The markup is not expected to bring citations in AI answers by itself; what Google names for that is useful, crawlable pages. So the pages that fill their lists in the browser (Inside, the board, Mission Control) also carry the same lists as static HTML, written at build time by `scripts/build_fallbacks.py`, and no page carries a `noindex` except the 404 page. Whether any of this changes citations is not measured here; the measurement needs search-console accounts and is a separate decision.
