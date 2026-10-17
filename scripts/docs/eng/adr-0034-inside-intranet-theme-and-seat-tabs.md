title: ADR-0034: Inside gets a light intranet theme of the design system, and its landing page a tab per seat
summary: A page that sets data-mb-theme="intranet" on its html element gets light intranet tokens (white panels on light grey, one blue accent) in both system settings; the Inside landing page opts in first and shows the three site cards, then one card per seat as tabs, then the selected seat's dashboard from seats.json and cockpit.json, written by scripts/build_inside_seats.py and checked in the required job.
parent: decision-log
order: 34
adr: 34
status: accepted
created: 2026-10-17
labels: adr, decision, design-system, inside, seats, generated-pages, accessibility
owner: Stefan Coetzee
reviewed: 2026-10-17
review_by: 2027-01-15
type: explanation
---
## Context

Inside is the public demo intranet of the house and, since 2026-10-16, Stefan Coetzee's working dashboard. On that date he asked for it to look like an intranet or admin console that stands apart from the dark public site, with a tab per seat of the house next to the three site cards, and approved a clickable mockup of the landing page. [ADR-0025](doc:eng/adr-0025-one-design-system) allows one design system, with light and dark from the visitor's system setting, so a second stylesheet with its own palette was ruled out. The seats, their areas, and their lens questions already sit in the seats contract ([ADR-0032](doc:eng/adr-0032-masthead-from-a-seats-file)); the items and the area titles sit in the cockpit's ([ADR-0031](doc:eng/adr-0031-cockpit-from-public-github-issues)).

## Decision

**The theme is a set of tokens.** `/design/tokens.css` gains one theme, `intranet`. A page opts in with `data-mb-theme="intranet"` on its `<html>` element; the dark values skip such a page, and the theme block replaces the neutrals (page `#F3F4F6`, panels `#FFFFFF`, text `#18202B`, lines `#D9DDE3`), the status colours, and the accent (`#1F4FA8`, the one blue). The theme is light in both system settings on purpose, so every visitor sees the working view in the intranet look; this narrows ADR-0025's light and dark rule for opted-in pages only. The top bar keeps its dark tokens, the fonts stay the site's own (Space Grotesk, with JetBrains Mono for every number), and the light data colours stay. Text tokens reach 6.5:1 or more on the theme's surfaces; the lowest text pair on the page is the demo banner's amber at 5.2:1 (WCAG 2.2 AA). Nothing is stored on the device.

**The landing page opts in first.** Every other page of Inside keeps its current look until it adds the attribute; each one is its own change, so a page that has not been checked in the theme does not switch by accident. [ADR-0035](doc:eng/adr-0035-intranet-theme-on-every-inside-page) replaced this rule on 2026-10-17: the site chrome now sets the theme on every page under /inside/.

**The landing page follows the mockup.** Under the header, the three site cards keep their live data and their wording (each site's gate record and the deploy feed, read in the browser). Below them, one card per seat in masthead order shows the seat's code, its areas, a status pill, and its counts. Below the cards sits the selected seat's dashboard: the lens questions from `seats.json`; four counts (open, in progress, blocked, and done in the cockpit's 14 days) for the seat's areas; and the seat's items that are not done, blocked first, each linked to its issue or pull request. The chief executive's dashboard counts every area and shows one tile per area and the decisions waiting (kind decision, not done), as ADR-0032 set for the masthead's tab; the list of its own area's items below them is new in this record, the same list every other seat shows. The seat-to-area mapping is the contract's; the contract names areas for every seat, so the mockup's mapping is not used. A panel with no data source yet, the publisher's pipeline, is a dashed box labelled "not wired yet" with no number. The sections that were on the page before (front page, deploy feed, apps, experiments, living documents, repositories, and the Grafana dashboards) follow under "Work and tools", and the access-model banner stays. [ADR-0036](doc:eng/adr-0036-inside-seat-tabs-as-folder-tabs) refined the cards on 2026-10-17: each seat card became a compact folder tab that carries only the seat code and one status pill, joined to the dashboard panel, with the areas and the counts kept in the panel.

**One generator, one check.** `scripts/build_inside_seats.py` writes the block `<!-- static:inside-seats -->` from the two files, each read through its own loader and contract check, and the cockpit generator's area titles. The Conformity checks job runs `--check`, so a block edited by hand or data outside a contract can neither merge nor deploy; the deploy job runs the build after the cockpit's fetch, artifact only, so the tabs are as fresh as the cockpit; `scripts/build_powersuit.py` runs it after a pin move; `scripts/test_build_inside_seats.py` runs in Script tests.

**Tabs by progressive enhancement.** In the markup the seat cards are a list of links to the dashboards, and every dashboard follows in order, so a reader without a script, or a crawler, gets every seat. The page script turns the list into a tablist: one dashboard shown, the selected card marked, arrow keys and Home and End to move, Tab into the panel, and the choice in the URL hash so a link opens a seat; a click adds a history entry, so Back steps through the seats. The page has one hash, which the Grafana tabs further down also write, so a link keeps the last choice. At phone width the cards stack in one column and the item rows stack inside their card, so no page scrolls sideways at 375 px.

## Consequences

The theme is a few tokens in one file, so another page of Inside adopts it with one attribute and a check of its own page styles; a page whose styles name a colour outside the tokens needs that fixed first. The landing page shows numbers only from `seats.json` and `cockpit.json`, and "done" means done in the cockpit's 14-day window, because the data keeps no older closed item. The local cockpit app is to get the same layout over the private tracker; that backend never reaches this repository. The page's social preview image still shows the dark page from before this change, until it is taken again.
