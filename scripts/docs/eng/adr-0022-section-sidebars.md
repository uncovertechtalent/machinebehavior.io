title: ADR-0022: Section sidebars from the navigation source
summary: Research and Inside pages carry a sidebar with every page of their section, written from site/nav.yml; a column beside the content from 1100 px, a closed disclosure above it on narrower screens.
parent: decision-log
order: 22
adr: 22
status: accepted
created: 2026-10-09
labels: adr, decision, navigation
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

The docs had a page tree beside every page; the research pages and the Inside pages had none. A reader on a claims page could not see that experiments, registers, case files and reference texts sit next to it, and an Inside page showed its siblings only in the top bar. Backlog issue [#28](https://github.com/uncovertechtalent/machinebehavior.io/issues/28) asked for a sidebar on Inside pages; Stefan Coetzee asked on 2026-10-09 for a sidebar by section across the site.

## Decision

`side()` in `scripts/site_chrome.py` writes the sidebar of the Research and Inside sections (`SIDEBARS`) from `site/nav.yml`, between `<!-- mb:side -->` markers, before the reading column or `<main>`. It lists every page of the section: groups (Case files, Articles, Reference) as headings, a page with children (Services) as a disclosure that is open when the current page is inside it, and the current page marked with `aria-current="page"`. The Docs section keeps its own space tree from `scripts/build_docs.py`; Home and Map have no sidebar.

From 1100 px the sidebar is a column of 264 px beside the content, sticky under the top bar, and the page body becomes a two-column grid. Below 1100 px it is a disclosure above the content that names the section and its page count; `/inside/bar.js` closes it on load, and without JavaScript it stays open. The reading column keeps its width of 660 px in both cases.

## Consequences

A page added to a section in `site/nav.yml` appears in the sidebar of every page of that section on the next run, so the sidebars cannot drift from the tree. Each page carries the whole section list in its source: about 1.5 KB for Research and 2 KB for Inside. The map crawler reads sidebar links as navigation links, which the map hides by default. Issue #28 is closed by this change.
