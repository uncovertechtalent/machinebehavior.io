title: ADR-0045: Every sidebar group opens with its index page and lists its five newest pages
summary: Each research sidebar group holds one index page, named "All case files" and so on, with the group's pages under it, the Experiments layout. Case files, Articles, Registers and Reference get index pages written by build_hubs.py. Lists marked order newest run newest first by publication date, and the sidebar shows five pages per list at most, plus the current page when it is older.
parent: decision-log
order: 45
adr: 45
status: accepted
created: 2026-10-26
labels: adr, decision, site-chrome, navigation, research
owner: Stefan Coetzee
reviewed: 2026-10-26
review_by: 2027-01-24
type: explanation
---
## Context

[ADR-0044](doc:eng/adr-0044-sidebar-accordion-groups) made the research sidebar an accordion of six groups. Only Experiments opened with a link to a page listing the whole group ("All experiments"); Red team opened with "Overview", and Case files, Articles, Registers and Reference listed their pages with nothing above them, because /research/case-files/, /research/articles/, /research/registers/ and /research/reference/ did not exist. The groups grow with every new page, and a sidebar listing them all grows with them. On 2026-10-26 Stefan Coetzee asked for an "All" link at the top of every group with the five most recent pages under it; a mockup was rendered and chosen, with generated index pages and the labels below.

## Decision

**A group holds one page, its index.** In `site/nav.yml` each group holds exactly one page with the group's pages under it, or `include:`s a section, as Red team does. `side:` names the index in the sidebar: All experiments, All case files, All articles, All red-team pages, All registers, All reference texts. The red-team section carries its own `side:`, so "All red-team pages" replaces "Overview". `scripts/site_chrome.py` stops the build when a group holds anything else.

**The new index pages are generated.** A `hub: true` page is written by `scripts/build_hubs.py`: the group's name, its `about` line, and every page it holds with the page's own description and its publication date, or its last change when it gives none, under the report theme with an Index pill. Case files, Articles, Registers and Reference are hub pages; Experiments and Red team keep their written pages. The research index leaves the hub pages out of its lists, which already show the same pages.

**Newest first where a list asks for it.** `order: newest` on a page or section lists its pages newest first by `published`, ties in the written order, in the sidebar, on its index page and on the research index. Every page in such a list needs a date, and the build stops on one without. Experiments, Case files, Articles and Red team are ordered this way. Registers and Reference keep their written order, because most of their pages carry no publication date and the sitemap dates move with every rebuild.

**Five per list in the sidebar.** `SIDE_RECENT` caps each list under an index at five pages; older pages are on the index page. A page older than the five stays listed while it is the current page, so the sidebar always shows where the reader is. On 2026-10-26 no group holds more than four pages, so nothing is cut yet.

**The index joins the breadcrumbs.** The index is the parent of the group's pages, so a case file's trail reads Research, Case files, the case file, and the registers and reference pages gain their index the same way. URLs do not change.

This replaces two points of ADR-0044: "Overview" as the red-team label, and group pages keeping a trail without their group. The rest of ADR-0044 stands.

## Consequences

Every group reads the same way: one link to all of it, then its newest pages. A sidebar's length stops growing with the site, and an older page is one click away on its index. A new page goes under its group's index in `site/nav.yml`, with `published` where the list runs newest first. The sidebar counts nineteen research pages, the four index pages included; the research index still lists fifteen. The index pages carry no text of their own beyond the `about` line, so a group's introduction is a change to `site/nav.yml`.
