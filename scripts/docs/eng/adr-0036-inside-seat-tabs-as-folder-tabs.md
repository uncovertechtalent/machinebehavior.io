title: ADR-0036: The Inside seat cards become folder tabs joined to the dashboard panel
summary: The seat cards on the Inside landing page become compact folder tabs that carry only the seat code and one status pill (blocked beats open beats clear), with the areas and the counts moved into the dashboard panel below; the selected tab is white, taller and blue-outlined, and overlaps the panel's top border so the tab and the panel read as one outline. Six tabs stay on one row at every width, a phone shows PUB for the publisher and the count alone on each pill, the theme tokens of ADR-0034 give every colour, and the tab controller moves to inside/seat-tabs.js with its own test.
parent: decision-log
order: 36
adr: 36
status: accepted
created: 2026-10-17
labels: adr, decision, design-system, inside, seats, accessibility
owner: Stefan Coetzee
reviewed: 2026-10-17
review_by: 2027-01-15
type: explanation
---
## Context

[ADR-0034](doc:eng/adr-0034-inside-intranet-theme-and-seat-tabs) gave the Inside landing page one card per seat, each card carrying the seat code, the seat's areas, a status pill, and three counts, with the selected seat's dashboard below the row of cards. The cards and their dashboard repeated the same areas and counts, and a card that held four lines sat apart from the panel it controlled, so the row read as a second panel rather than as a set of tabs over one. On 2026-10-17, after six rounds of a clickable mockup, Stefan Coetzee approved a tighter design: the cards become folder tabs joined to the dashboard, each tab reduced to the one fact that tells a reader where to look.

## Decision

**A tab shows the seat code and one status pill.** The pill reports a single state: `N blocked` when the seat has a blocked item, else `N open` when it has an open item, else `clear`. Blocked beats open beats clear; a count of items in progress shows in the panel's tiles, not on the tab, so the tab carries at most one number and the eye lands on what is stuck. The seat's areas, its holder, and its four counts move into the dashboard panel, which already showed all of them, so nothing is lost and the tab stops repeating the panel.

**The tabs are folder tabs joined to the panel.** The tab row is flush with the panel's left edge and inset 14px on the right, so the panel's top-right corner stays rounded while its top-left corner is square. A back tab is grey, a little shorter, and has no bottom border; the selected tab is white, taller, outlined in the one blue accent, and overlaps the panel's top border by its own border width, so the selected tab and the panel read as one continuous outline. The panel takes the same blue outline, so the body the tab opens is clearly the body that tab controls.

**A phone keeps all six tabs on one row.** Below 600px the tab content stacks and centres, the publisher's code drops to `PUB` so the widest code fits, and each pill shows the count alone (`0` for a clear seat). The number tiles in the panel fall to two columns. No part of the page scrolls sideways at 375px. The markup carries both the long and the short form of the code and the pill, and the stylesheet switches between them by width, so the phone layout holds with or without a script.

**Colours come from the theme tokens.** Every colour is a token of the intranet theme ([ADR-0034](doc:eng/adr-0034-inside-intranet-theme-and-seat-tabs)): the grey back tabs, the white front tab and panel, the blue accent of the outline and the focus ring, and the status colours of the pills. The mockup's literal hex values are not used. The text on each surface meets WCAG 2.2 AA.

**The tabs stay reachable without a script, and the script is tested.** In the markup the tabs are a list of links and every dashboard follows in order, so a reader without a script, or a crawler, reaches every seat. The page script turns the list into a tablist: one dashboard shown, the selected tab marked with `aria-selected`, roving tabindex, Left and Right (and Up and Down), Home and End to move, Tab into the panel, a visible focus ring, and the choice in the URL hash so a link opens a seat and Back steps through them. Each tab's visible code and pill are hidden from a screen reader, which reads one label with the full title and state, for example "Chief executive, 8 blocked". The controller moves from an inline block to `inside/seat-tabs.js` and gains a test, `scripts/test_seat_tabs.mjs`, that drives it over a small DOM in the Script tests job; PR 103 left it untested.

## Consequences

The tab row carries less, so the dashboard panel is the one place that holds a seat's areas and counts, and a change to either lives in one place. The pill rule drops the in-progress state from the tab; a seat whose only live work is in progress reads as clear on its tab, while the panel's tiles still show the in-progress count. `scripts/build_inside_seats.py` writes the new tab from the same two files and the same required check holds it ([ADR-0034](doc:eng/adr-0034-inside-intranet-theme-and-seat-tabs)); the tab controller is now a first-party module beside `dashboards.js` and `bar.js`, loaded with `type="module"`.
