title: ADR-0028: The home page as the front page of the portal
summary: The home page leads into the sections of the portal: a hero with the map, the receipts as tiles, cards for Research, Inside, Mission Control, Docs, Topics and Map, the latest research and the topics, written from site/nav.yml; the case-file list that repeated the claims is gone.
parent: decision-log
order: 28
adr: 28
status: accepted
created: 2026-10-09
labels: adr, decision, navigation, home
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

The home page was a single serif column: the thesis, a picture of the map, four receipts, the TYChat lessons, a list of ten case files, five other surfaces and the aim. Since [ADR-0021](doc:eng/adr-0021-one-navigation-source) the site has sections, a research front page, topic hubs and Mission Control, and the home page linked none of them. Stefan Coetzee found it dated on 2026-10-09 and named the list at the bottom as redundant: its entries are the receipts of the claims and sit on [Claims](/claims/), [Experiments](/experiments/) and [Terms](/terms/).

## Decision

The home page keeps its text and changes its layout, in the reading brand and up to 1160 px wide:

- a hero with the title, the subtitle, the thesis, the one-liner and three links (research, Inside, the tour), beside the picture of the map;
- the four receipts as tiles; the P0 incident tile links the P0 dissection, which no other page linked;
- one card per section (Research, Inside, Mission Control, Docs, Topics, Map) with the sentence `about` in `site/nav.yml` and the page count;
- the four research pages published last, by the `published` dates in `site/nav.yml`, with the description each page gives itself;
- the topics as links to their hubs;
- the TYChat lessons, the other surfaces as a compact list, and the aim.

The cards, the latest research and the topics sit between `<!-- static:home-... -->` markers and are written by `scripts/build_fallbacks.py`, so they follow the navigation source. The case-file list and the decorative network band above the title are gone; the map picture in the hero carries the same image.

## Consequences

A new section or a new research page with a `published` date shows on the home page at the next build. The text in the hero, the tiles, the lessons, the surfaces and the aim stays hand-written. The section sentences in `site/nav.yml` are new text and open to a voice pass.
