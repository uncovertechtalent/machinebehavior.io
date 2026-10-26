title: ADR-0043: The second-brain map draws its graph on a dark canvas
summary: The map's canvas, and only the canvas, is dark in every setting: the top bar's colour from --mb-bar-bg, with the bright node colours and light labels it used before ADR-0042. The panel, the hover tip and the preview sheet stay light, the legend dots get an outline so the bright colours hold on the light panel, and the stamp on the canvas uses the bar's text colours.
parent: decision-log
order: 43
adr: 43
status: accepted
created: 2026-10-26
labels: adr, decision, design-system, map, accessibility
owner: Stefan Coetzee
reviewed: 2026-10-26
review_by: 2027-01-24
type: explanation
---
## Context

[ADR-0042](doc:eng/adr-0042-one-light-scheme) gave the site one light scheme and had the second-brain map at /map/ draw its light palette. On the light page colour the graph lost depth: the nodes and the links between them read as thin marks on paper. Stefan Coetzee asked the same day for a black background behind the graph only.

## Decision

**The canvas is dark graph art.** The script draws the canvas on the top bar's colour, read from `--mb-bar-bg` in `design/tokens.css`, so the bar and the graph read as one dark field and the colour lives in one place. The nodes take the bright colours and the labels the light ink they had on the dark canvas before ADR-0042. The page's own background behind the canvas is the same colour, so nothing light shows before the canvas draws.

**Everything a person reads in a box stays light.** The panel, the hover tip and the preview sheet keep the light tokens, as on every page. The legend dots in the panel carry a thin dark outline, because the bright node colours alone are faint on white. The stamp at the bottom right sits on the canvas and uses the bar's text colours (`--mb-bar-dim`, `--mb-bar-soft`).

**The contrast floor holds on the canvas.** The stamp reaches 6.3:1, its link 11.8:1, the node labels about 11.6:1 against the canvas, and every node colour 5.1:1 or more.

This replaces the map paragraph of ADR-0042; the rest of ADR-0042 stands. The dark canvas joins the top bar and the report theme's title band as dark chrome on a light site.

## Consequences

The map looks the same in every system setting, with the graph on dark and the controls on light. A change to the top bar's colour changes the canvas with it. The second-brain image in the front page's title band was already a dark rendering of the same graph, so the front page and the map now agree.
