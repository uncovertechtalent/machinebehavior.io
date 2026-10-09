title: Inside portal
summary: Inside is one static page that reads live data in the browser: site status, the deploy feed, the latest work, experiments and the Grafana dashboards.
order: 60
labels: inside, portal, frontend
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: reference
---
[Inside](/inside/) is the front page for the whole body of work. It is one static HTML file, `inside/index.html`; every live panel is read in the visitor's browser when the page loads. Nothing runs on a server.

## Panels and their data

| Panel | Data | Notes |
|---|---|---|
| Site status | `/conformity/latest.json` of each of the three sites | GitHub Pages serves JSON with an open CORS header, so the page reads all three sites |
| Deploy feed | `/inside/deploys.json`, written by the deploy job from the GitHub Actions API for the two public repositories | A snapshot as of the last deploy of machinebehavior.io; the visitor's browser sends no request to GitHub |
| Front page (latest, most linked) | `/map/graph.json` | Cross-posts of one piece are merged; site order mb, UTT, TYChat, Substack |
| Experiments | Eval 04 figures in the page, plus `/conformity/probes/latest.json` for the weekly probe | |
| Dashboards | Grafana public dashboards in an iframe | Loaded when the section scrolls into view; `#dashboards/<key>` opens a tab (deploys, agents, llm, host, search) |
| Docs | [Inside docs](/inside/docs/) | The documentation tree; see [Docs tree](doc:eng/docs-tree) |
| Board | [Board](/inside/board/), from `/inside/board/issues.json` written by the deploy job | Work items from GitHub Issues; see [Ticket board](doc:eng/board) |
| Services | [Service catalog](/inside/services/), from `services/*.yml` | See [Service catalog](doc:eng/service-catalog) |
| Status | [Status](/inside/status/), from the gate records, `/inside/deploys.json` and `incidents/*.yml` | See [Status page](doc:eng/status-page) |
| Top bar and search | `scripts/inside_chrome.py`, `/inside/search.json` | The same bar on every Inside page; the search covers the docs, the services and the map. See [Top bar and search](doc:eng/top-bar-and-search) |

## Rules for the page

- No request to a third party when the page loads: fonts are served from `/fonts/`, the deploy feed from `/inside/deploys.json`. The Grafana frames load from grafana.scoetzee.de only when the dashboards section scrolls into view.

- Build links in script with `a.href = ...`, never with an interpolated `href` attribute in a template string; the gate reads those as relative links.
- Pages under `/inside/` are the platform, not pieces: the front page list skips them.
- The page has no search box of its own; the one in the top bar covers everything the old box did, plus the docs and services.
- Without JavaScript the page points to `/llms.txt`, `/map/graph.json` and `/conformity/`.
- Grafana frames only because Grafana runs with embedding allowed; see [Public dashboards](doc:obs/public-dashboards).

## Related

- The menu link "infrastructure" on every page opens `/inside/#dashboards`.
- The [map](/map/) opens pages of the three sites in a preview sheet and links back to Inside.
