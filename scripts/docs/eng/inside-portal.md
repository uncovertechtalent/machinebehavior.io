title: Inside portal
summary: Inside is one static page that reads live data in the browser: site status, the deploy feed, the latest work, experiments and the Grafana dashboards.
order: 60
created: 2026-10-14
updated: 2026-10-28
labels: inside, portal, frontend
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: reference
---
[Inside](/inside/) is the front page for the whole body of work. It is one static HTML file, `inside/index.html`; every live panel is read in the visitor's browser when the page loads. Nothing runs on a server.

## Mission Control

The live operations view sits on its own page, [Mission Control](/inside/mission-control/): the gate and deploy state of the three sites, the last ten deploy runs, open incidents, this site's gate result and the dashboards as tabs, read from the same records as the panels below. The dashboard list is `/inside/dashboards.js`, shared by both pages. See [ADR-0026](doc:eng/adr-0026-mission-control).

## Cockpit

[The cockpit](/inside/cockpit/) is the CTO powersuit cockpit running on the public work: the issues and pull requests of the owner's public repositories by area of the CTO job, with a scorecard and the open items for each area, a 14-day trend, and the CTO powersuit plugins of each area. It is a static page, rebuilt at each deploy from the GitHub API behind a contract check. See [Cockpit page](doc:eng/cockpit) and [ADR-0031](doc:eng/adr-0031-cockpit-from-public-github-issues).
## Panels and their data

| Panel | Data | Notes |
|---|---|---|
| Site status | `/conformity/latest.json` of each of the three sites | GitHub Pages serves JSON with an open CORS header, so the page reads all three sites |
| Deploy feed | `/inside/deploys.json`, written by the deploy job from the GitHub Actions API for the two public repositories | A snapshot as of the last deploy of machinebehavior.io; the visitor's browser sends no request to GitHub |
| Front page (latest, most linked) | `/map/graph.json` | Cross-posts of one piece are merged; site order mb, UTT, TYChat, Substack |
| Experiments | Eval 04 figures in the page, plus `/conformity/probes/latest.json` for the weekly probe | |
| Dashboards | Grafana public dashboards in an iframe | Loaded when the section scrolls into view; `#dashboards/<key>` opens a tab (deploys, agents, llm, host, search) |
| Second brain (CKO seat) | `/map/` in an iframe | Loaded when the card scrolls into view; the frame ignores the pointer until the reader clicks "Click to explore"; a click on a node of this site inside the frame opens that page in the top window |
| Docs | [Inside docs](/inside/docs/) | The documentation tree; see [Docs tree](doc:eng/docs-tree) |
| Board | [Board](/inside/board/), from `/inside/board/issues.json` written by the deploy job | Work items from GitHub Issues; see [Ticket board](doc:eng/board) |
| Services | [Service catalog](/inside/services/), from `services/*.yml` | See [Service catalog](doc:eng/service-catalog) |
| Cockpit | [Cockpit](/inside/cockpit/), from `/inside/cockpit/cockpit.json`, written by the deploy job from the GitHub API | Issues of the public repositories by area of the CTO job; see [Cockpit page](doc:eng/cockpit) |
| Status | [Status](/inside/status/), from the gate records, `/inside/deploys.json` and `incidents/*.yml` | See [Status page](doc:eng/status-page) |
| Top bar and search | `scripts/site_chrome.py`, `/inside/search.json` | The same bar on every page of the site; the search covers the docs, the services and the map. See [Top bar and search](doc:eng/top-bar-and-search) |

## Rules for the page

- No request to a third party when the page loads: fonts are served from `/fonts/`, the deploy feed from `/inside/deploys.json`. The Grafana frames load from grafana.scoetzee.de only when the dashboards section scrolls into view.

- Build links in script with `a.href = ...`, never with an interpolated `href` attribute in a template string; the gate reads those as relative links.
- Pages under `/inside/` are the platform, not pieces: the front page list skips them.
- The page has no search box of its own; the one in the top bar covers everything the old box did, plus the docs and services.
- The landing page is the seat tabs: `#seats` holds one dashboard per seat, and each dashboard ends in a hand-written slot (`<!-- seat-extra:SEAT -->`) for the cards and tools of that seat. Today: CEO holds `#sites`; CTO holds the deploy feed, apps, experiments and the Grafana frames `#dashboards` (deploys, local LLM, host); CFO holds the Claude Code spend dashboard (`#dash-cfo`, first in the panel); Publisher holds the front page; CKO holds the second brain (`#map-embed`, first in the panel, the map framed behind a "Click to explore" button so a scroll over it does not zoom the graph, loaded when in view), living documents, repos and the search dashboard (`#dash-cko`); CHRO is empty. Each Grafana section lists its dashboards in `data-dashes`; a `#dashboards/KEY` link opens the seat that holds KEY. `scripts/build_inside_seats.py` writes the rest of the block and carries each slot over unchanged. The panel order is the generator's: head, lens, tiles, areas, work block (open items, or "Nothing open"), then the seat slot. A seat that needs a hand-written card higher up names its order in `LAYOUT` and puts the card in a part slot (`<!-- seat-extra:SEAT/PART -->`); a block or slot the layout does not name follows in the default order. CKO reads: second brain (`cko/map`), work block, search dashboard (`cko/dash`), then lens, tiles, and the seat slot (living documents, repos). CFO reads: cost dashboards (`cfo/dash`), then lens, tiles, work block. Edit a part slot in `inside/index.html` like the seat slot; the build refuses to run when the page holds content in a part slot that `LAYOUT` does not name. A hash that names an element inside a panel (`#dashboards/deploys`) opens that seat. `#sources` and an "In this area" nav (Seats, Data sources) sit around the block, and a "Leave Inside" nav at the foot links back to the public site. `main` carries `data-area="inside"` as the hook for scoping the area. The exit nav is hand-written, outside the chrome markers, so touch it when a section URL moves.
- Without JavaScript the page points to `/llms.txt`, `/map/graph.json` and `/conformity/`.
- Grafana frames only because Grafana runs with embedding allowed; see [Public dashboards](doc:obs/public-dashboards).

## Related

- The menu link "infrastructure" on every page opens `/inside/#dashboards`.
- The [map](/map/) opens pages of the three sites in a preview sheet and links back to Inside.
