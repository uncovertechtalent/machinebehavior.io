title: Inside portal
summary: Inside is one static page that reads live data in the browser: site status, the deploy feed, the latest work, experiments and the Grafana dashboards.
order: 60
labels: inside, portal, frontend
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

## Rules for the page

- No request to a third party when the page loads: fonts are served from `/fonts/`, the deploy feed from `/inside/deploys.json`. The Grafana frames load from grafana.scoetzee.de only when the dashboards section scrolls into view.

- Build links in script with `a.href = ...`, never with an interpolated `href` attribute in a template string; the gate reads those as relative links.
- Without JavaScript the page points to `/llms.txt`, `/map/graph.json` and `/conformity/`.
- Grafana frames only because Grafana runs with embedding allowed; see [Public dashboards](doc:obs/public-dashboards).

## Related

- The menu link "infrastructure" on every page opens `/inside/#dashboards`.
- The [map](/map/) opens pages of the three sites in a preview sheet and links back to Inside.
