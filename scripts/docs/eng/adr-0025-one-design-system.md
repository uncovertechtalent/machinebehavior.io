title: ADR-0025: One design system, two layouts, light and dark from the system setting
summary: One token file for colour, type and spacing, component CSS for the chrome and the shared components, a reading layout and an app layout under one brand, light and dark from prefers-color-scheme with nothing stored on the device.
parent: decision-log
order: 25
adr: 25
status: accepted
created: 2026-10-09
labels: adr, decision, design-system, accessibility
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

The research pages had their own palette in `/style.css` (light and dark, serif, teal). Inside, the docs, the board, the tour and the map each defined a dark palette of their own, inline or in `/inside/docs/docs.css`, with about 170 colour values written into the pages and scripts. Inside had no light mode. A change of colour meant edits in eight places, and nothing checked contrast. Stefan Coetzee decided on 2026-10-09: shared navigation and a reading layout, and the couch stays as the mark.

## Decision

`/design/tokens.css` holds every colour, the type scale, spacing, radii and the layout widths, as custom properties starting with `--mb-`, with light values and dark values under `prefers-color-scheme`. Every page loads it through the chrome block of [ADR-0021](doc:eng/adr-0021-one-navigation-source), and `/style.css` and `docs.css` import it, so a page without the block keeps its colours. The older variables (`--ink`, `--paper`, `--line`, `--amber` ...) are mapped onto the tokens in the same file, so pages and generators written before this change follow it without edits, including the gate's `/conformity/` page.

`/design/chrome.css` styles the top bar, breadcrumbs, sidebars, Topics block, demo banner, footer and the two layouts. `/design/components.css` holds the shared components: page header (section label, title, meta line), pills, cards, panels, tables, entry lists and the focus ring. The older class names that render the same component (`.chip`, `.pill`, `.stage`, `.card`, `.claim` ...) are listed with the canonical `mb-` class, so they take the same shape.

Two layouts under one brand: the reading layout keeps the serif column of 660 px for long research pieces, with teal as its accent; the app layout keeps the portal look of Inside, the docs and the map, with amber as its accent. The top bar is dark in both schemes. Light and dark follow the visitor's system setting; the site stores no preference, so it sets no cookie and writes nothing to local storage (TDDDG § 25). The map canvas reads the same setting in its script and redraws when it changes.

Accessibility: a skip link is the first element of every page; the bar, breadcrumbs, sidebars and footer are landmarks with names; every interactive element shows a focus ring; text tokens reach at least 4.5:1 on the page and card surfaces in both schemes (WCAG 2.2 AA; the lowest pair is 4.6:1). Long hashes, URLs and code wrap inside the reading column, and wide tables and preformatted blocks scroll inside their own box, so no page scrolls sideways at 375 px.

## Consequences

A colour changes in one file. Data colours (site dots, board columns, map nodes) have a darker light-mode variant so they hold on a light surface; scripts write them as `var(--mb-data-...)` where the browser resolves CSS, and the map keeps a light and a dark set because a canvas cannot read CSS variables. `color-mix()` derives tints from the tokens, so browsers older than 2023 show the tints without transparency. A page that hard-codes a colour drifts again; a gate check for colour values outside the token file, and a design-system page in the docs, are later steps.
