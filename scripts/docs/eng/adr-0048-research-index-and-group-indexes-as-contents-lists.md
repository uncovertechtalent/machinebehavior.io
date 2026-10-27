title: ADR-0048: The research index and the group index pages are contents lists
summary: /research/ and the four generated group indexes list pages as lines, with no boxes and no copied descriptions. A group's label links to its index page; each page is a title with its publication date where it has one; pieces that live elsewhere keep their mark and the site they live on. The Section and Index pills and the dated eyebrows go. Replaces the description lists of ADR-0045.
parent: decision-log
order: 48
adr: 48
status: accepted
created: 2026-10-27
labels: adr, decision, research, navigation, site-chrome, design-system
owner: Stefan Coetzee
reviewed: 2026-10-27
review_by: 2027-01-25
type: explanation
---
## Context

[ADR-0045](doc:eng/adr-0045-sidebar-groups-open-with-an-index) gave every research group an index page and made it a list of cards: the page's title, the description the page gives itself, and a date. The research index listed every research page the same way, two cards under most of its six labels. After the paper theme ([ADR-0047](doc:eng/adr-0047-research-and-front-page-in-the-paper-theme)) went live on 2026-10-27, Stefan Coetzee asked for /research/ to be compressed: the fifteen boxes read as one block repeated six times, and each page's headline ran three times before the reader opened it, in the sidebar, as the card's title, and as the card's description, which is the page's own subtitle copied. The hierarchy should carry less and the pages more.

Measured on the live page at 1440 px wide: the list block was 3145 px tall and carried 600 words of copied description; every card said "updated 2026-10-26", because the date came from the sitemap and the sitemap date moves with every rebuild. Two layouts were mocked on the live page. A contents list with the group labels kept measured 711 px. A flat list with a kind prefix on every line was shorter still, but it loses the groups, four pages carry no publication date (the claims ledger, the slips log, the terms and the man pages), and the two overview pages became awkward lines. Stefan Coetzee chose the contents list.

## Decision

**The research index is a contents list.** `scripts/build_hubs.py` writes /research/ as one block per group, in the sidebar's order: the group's label in small capitals on the left, linking to the group's index page (the Experiments page, the red-team overview, or the generated hub); the group's pages on the right as the lines of an ordered list, each the page's title, a dotted leader and the date at the end of the line. No description. A page that is a group's index is the label and never a line, so "Experiments" and "Red team" appear once each. The programme's premise above the list and the two links below it stay.

**Dates are publication dates.** A line carries `published` from `site/nav.yml`, or nothing. The sitemap's date is gone from the lists. The page's own modified date, in its head and in the sitemap, still follows the last change of any page it lists.

**The group index pages use the same list.** A `hub: true` page is its title, its `about` line as the subtitle, and one list of its pages with their publication dates. Pieces listed `elsewhere` ([ADR-0046](doc:eng/adr-0046-articles-index-lists-pieces-elsewhere)) stay merged by date and marked ↗, with the date, the site they live on and any copy at the end of the line; the note above the list stays. Their `about` lines no longer appear on the page; `site/nav.yml` keeps them as the entry's own record, and the tree still requires them.

**The pills and the eyebrows go.** These pages carry no "Section" or "Index" pill and no "N pages · updated" line: the title and the one-line subtitle are the head. The breadcrumbs, the sidebar and the chrome's page-meta line are unchanged.

**The rules live in `style.css` under the paper theme.** `.toc-group` is a two-column grid with a 168 px label column that stacks below 820 px; a line is a flex row at the body size, the leader a dotted hairline in the line colour, the date in the dim text at 15 px; links keep the teal and drop the hairline; `.toc-out` adds the arrow. The card rule for `.mb-entry` in `design/components.css` stays for the topic hubs, which keep their cards.

**What this replaces.** The part of ADR-0045 that gives a hub page every page it holds with the page's own description and a date under an Index pill, and the research index's card list. ADR-0045's sidebar rules and the index pages themselves stand, and so does ADR-0046's list of pieces elsewhere.

## Consequences

The research index runs to thirteen lines under six labels where it ran to fifteen boxes, and the sheet is 1516 px tall at 1440 px wide where it was 3957. A headline appears on the index once, as a title; the one-line description waits on the page, where the subtitle carries it. A new page needs `published` in `site/nav.yml` to show a date on a list; a page without one shows its title alone. The sidebar on the index page still lists the same titles beside the list, under ADR-0045's rules; that duplication is known and left for a later decision. `scripts/test_site_chrome_side.py` checks the shape of the index and of the hub pages.
