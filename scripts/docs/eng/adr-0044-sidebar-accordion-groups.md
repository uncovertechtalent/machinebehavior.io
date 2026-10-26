title: ADR-0044: Sidebar groups fold out one at a time, the research sidebar includes the red team, and no sidebar lists the topics
summary: Sidebar groups become an accordion of details elements sharing one name, so opening a group closes the others with no script, and the group holding the current page opens on load. The research sidebar groups its pages in reading order and includes the red-team section, whose pages show it. The Topics block leaves every sidebar; Topics stays in the More menu and as a link in the research sidebar.
parent: decision-log
order: 44
adr: 44
status: accepted
created: 2026-10-26
updated: 2026-10-26
labels: adr, decision, site-chrome, navigation, research, accessibility
owner: Stefan Coetzee
reviewed: 2026-10-26
review_by: 2027-01-24
type: explanation
---
## Context

The research sidebar ([ADR-0022](doc:eng/adr-0022-section-sidebars)) opened with five ungrouped links (claims ledger, experiments, objections register, evidence index, slips), then three labelled groups (case files, articles, reference). The experiments page was a disclosure whose arrow sat outside the column. The red-team pages live under /research/red-team/ but form their own section, so they were missing from the research tree and showed a sidebar of three pages. Every sidebar ended with the Topics block of [ADR-0023](doc:eng/adr-0023-topic-hubs): all eight hubs, with a dot on those that list the current page, which a reader had no way to read. On 2026-10-26 Stefan Coetzee asked for the sidebar to be restructured, then for groups that fold out one at a time; a mockup was rendered, clicked through and chosen.

## Decision

**Groups are an accordion.** `side()` in `scripts/site_chrome.py` writes each group of `site/nav.yml` as `<details class="mb-side-acc" name="mb-side">` with the group name as its `<summary>`. Details elements that share a name are exclusive, so opening one closes the others with no script; Chrome 120, Safari 17.2 and Firefox 130 support it, and an older browser lets several stay open. The group holding the current page is open on load, and its heading keeps the accent colour while closed. Inside a group a page's children are listed under it, so the experiments register and the abliteration probe sit together with no second disclosure.

**The research sidebar in reading order.** The research section's pages form six groups: Experiments, Case files, Articles, Red team, Registers, Reference. Groups stay out of the breadcrumbs, so every page keeps its trail (Research, Experiments, the probe). A `side:` key gives a page a different name in the sidebar (the experiments page reads "All experiments" under the Experiments heading). Replaced by [ADR-0045](doc:eng/adr-0045-sidebar-groups-open-with-an-index): every group now opens with its index page, which joins the trail of the group's pages (Research, Case files, the case file).

**The red team is included.** A group with `include: red-team` lists the red-team section's overview (as "Overview") and its pages. `SIDEBAR_HOST` maps the red-team section to the research sidebar, so a red-team page shows the same tree with the Red team group open. The red-team section stays a section: its breadcrumbs, its door on the front page and its place in the menu do not change. Under ADR-0045 the overview is named "All red-team pages".

**No topic list in the sidebars.** The Topics block is removed from `side()`, from the docs sidebar of `scripts/build_docs.py` and from the styles, with its helpers. Topics stays in the top bar's More menu and on /topics/. The research sidebar's Reference group links it through a `link:` entry: a sidebar-only link, which is never indexed as a page of the section, so /topics/ keeps its own section and breadcrumbs.

**The research index follows the groups.** `scripts/build_hubs.py` lists the research index by the same groups: an included section's overview and pages, a page's children, and no sidebar-only links.

## Consequences

A research or red-team page shows six headings and the one group the reader is in, instead of twelve links in mixed order and eight topic hubs. A reader moving between the research pages and the red team keeps one tree. A new research page needs a group in `site/nav.yml`; a page outside any group would sit above the groups as a plain link. The topic hubs no longer show which topics list the current page; a hub still lists its pages. The research index counts fifteen pages, the red-team pages included.
