title: ADR-0042: The site has one light colour scheme
summary: The dark values that followed the visitor's system setting are removed from design/tokens.css, color-scheme becomes light, and the second-brain map drew its light palette (its canvas is dark under ADR-0043). The top bar and the report theme's title band stay dark as chrome. The /conformity/ page, written by the shared gate action, keeps its own dark block until that action changes.
parent: decision-log
order: 42
adr: 42
status: accepted
created: 2026-10-26
updated: 2026-10-27
labels: adr, decision, design-system, accessibility, map
owner: Stefan Coetzee
reviewed: 2026-10-26
review_by: 2027-01-24
type: explanation
---
## Context

[ADR-0025](doc:eng/adr-0025-one-design-system) gave the site one token file with light values and dark values under `prefers-color-scheme`, so a visitor with a dark system setting saw the public pages dark. Since then Inside took the light intranet theme ([ADR-0034](doc:eng/adr-0034-inside-intranet-theme-and-seat-tabs), [ADR-0035](doc:eng/adr-0035-intranet-theme-on-every-inside-page)) and the research section and the front page took the light report theme ([ADR-0039](doc:eng/adr-0039-research-report-theme), [ADR-0041](doc:eng/adr-0041-front-page-in-the-report-theme)), each skipping the dark values. What remained dark under a dark setting were the other public pages (the CTO pages, conformity, the man pages, Topics, AI search, the legal pages) and the map. Every consulting and research publisher read for ADR-0039 serves one light page. On 2026-10-26 Stefan Coetzee decided to drop the dark scheme.

## Decision

**One scheme.** The `@media (prefers-color-scheme: dark)` block in `design/tokens.css` is removed, `:root` declares `color-scheme: light`, and the intranet and report themes keep their own light values on top. No page changes with the visitor's system setting, and nothing is stored on the device.

**The map draws the light palette.** `map/index.html` drew its canvas from a dark or a light set by the system setting and redrew on a change. It now draws the light set only, and the dark colours are removed from its kinds. Replaced by [ADR-0043](doc:eng/adr-0043-map-draws-on-a-dark-canvas): the canvas behind the graph is dark again; the panel stays light.

**Dark stays where it is chrome.** The top bar (`--mb-bar-*`) and the report theme's title band (`--mb-band`) are dark in every page; they mark the frame and the title, not a scheme. Replaced by [ADR-0047](doc:eng/adr-0047-research-and-front-page-in-the-paper-theme) for the band: there is no title band, and the `--mb-band` tokens are gone.

**The dead hero styles go.** `/style.css` held a `.hero` band with a light and a dark map image for the old front page; no page used it.

**One gap.** The /conformity/ page is written by the shared gate action (`.github/actions/conformity/run.py`), whose inline styles carry their own dark block. The action is shared with tychat.io and uncovertechtalent.com and has its own owner, so that block changes in the action, as its own change.

## Consequences

A visitor sees the same page whatever their system setting, and every contrast check runs against one set of surfaces. Visitors who prefer dark pages lose that option on this site; a browser's own forced-dark or reader mode still applies. Data colours keep their darker light-mode values, which ADR-0025 introduced so that they hold on a light surface. Until the gate action changes, /conformity/ turns dark under a dark system setting while its chrome stays light.
