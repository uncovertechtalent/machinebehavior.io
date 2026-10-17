title: ADR-0035: Every page under /inside/ uses the intranet theme, set by the site chrome
summary: The site chrome sets data-mb-theme="intranet" on the html element of every page under /inside/ (Inside, its services, and Docs) and removes it from every other page, so the light intranet theme of ADR-0034 covers all of Inside, new pages get it with no step of their own, and site_chrome.py --check holds it in the required job.
parent: decision-log
order: 35
adr: 35
status: accepted
created: 2026-10-17
labels: adr, decision, design-system, inside, docs, site-chrome, accessibility
owner: Stefan Coetzee
reviewed: 2026-10-17
review_by: 2027-01-15
type: explanation
---
## Context

[ADR-0034](doc:eng/adr-0034-inside-intranet-theme-and-seat-tabs) gave Inside a light intranet theme as a set of tokens and switched it on for the landing page only, with every other page of Inside to follow as its own change once checked. On 2026-10-17 Stefan Coetzee asked for every page under /inside/ to look like the landing page: mission control, the cockpit, the board, status, the service catalog, the tour, search, the masthead, and the docs. A page that kept the dark look next to a light landing page read as a different product. The chrome of every page already comes from one source ([ADR-0021](doc:eng/adr-0021-one-navigation-source)), written by `scripts/site_chrome.py`, which every page generator calls before it writes.

## Decision

**The chrome sets the theme by URL.** `apply()` in `scripts/site_chrome.py` sets `data-mb-theme="intranet"` on the `<html>` element of every page whose URL starts with `/inside/`, and removes the attribute from every other page. The attribute is part of the managed chrome like the bar and the footer, so `python3 scripts/site_chrome.py --check` in the Conformity checks job fails when a page under /inside/ lacks it or a page outside carries it. A new page of Inside or Docs gets the theme from the generator that writes it, with no step of its own. This replaces ADR-0034's rule that each page opts in on its own; the tokens, the dark top bar, and the contrast floor of ADR-0034 stay as they are.

**Every Inside page type was checked in the theme before the switch.** The page styles of Inside (`inside/inside.css`, `inside/cockpit/cockpit.css`, `inside/masthead/masthead.css`, `inside/docs/docs.css`, and the page `<style>` blocks) name no colour outside the tokens, so they follow the theme with no edit. A script in the browser measured the contrast of every visible text element against its painted background on the landing page, the board, the cockpit, status, search, the tour, mission control, the service catalog and one service page, the masthead, the docs home, docs health, and docs pages with tables, code, panels, the changelog, and the decision log, at 1280 px and 375 px; every text pair reaches WCAG 2.2 AA. Pages outside /inside/ were measured the same way and keep their theme.

**Links and the accent in the docs follow the theme.** Docs and service pages coloured their links with the amber of the app layout. They now use the layout accent, which is amber on any page outside the theme and the intranet blue inside it, so the landing page and the docs show one link colour. The same goes for hover, focus, and current-page marks on Inside's own pages, and for the button on mission control. Amber that carries a meaning stays amber: the demo banner, a tier-2 service, a warning light, an incident under monitoring, a page that needs review, and a review date that has passed.

**The Grafana frames are light too.** The landing page and mission control frame the public Grafana dashboards through one URL function in `inside/dashboards.js`; it now asks Grafana for its light theme (`theme=light`), so a frame matches the page around it. A frame still loads only when the reader asks for it or scrolls to it ([ADR-0010](doc:eng/adr-0010-no-third-party-requests)).

## Consequences

All of Inside reads as one intranet in the light look, in both system settings; the public site keeps light and dark from the visitor's setting. The change touches every page under /inside/ by one attribute, which a word diff of the generated pages shows. A page under /inside/ cannot leave the theme without a change to `site_chrome.py` and a record that says why. The social preview images of the Inside pages still show the dark pages until they are taken again.
