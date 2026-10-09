title: Engineering
summary: How the three sites are built, gated and deployed, plus the map crawler, the Inside portal and this docs tree.
labels: moc, engineering
---
This space documents the systems behind machinebehavior.io, tychat.io and uncovertechtalent.com: how each site is built, the conformity gate that every push passes before it serves readers, the deploy job, the crawler that draws the [map of the work](/map/), the [Inside](/inside/) front page and this documentation tree.

> [!info] Three static sites, one gate. Each site is static files on GitHub Pages. Each deploy runs the same conformity checks first; a failed check stops the deploy and the previous build stays live.

## Systems

| System | What it does | Source | Page |
|---|---|---|---|
| machinebehavior.io | Research site: claims, experiments, case files, Inside, the map, these docs | [uncovertechtalent/machinebehavior.io](https://github.com/uncovertechtalent/machinebehavior.io) | [Site architecture](doc:eng/site-architecture) |
| Conformity gate | Checks every page on every push, weekly and by hand; blocks the deploy on a failed check | `.github/actions/conformity/run.py` | [Conformity gate](doc:eng/conformity-gate) |
| Deploy job | Refreshes the map, uploads the site, deploys to Pages | `.github/workflows/conformity.yml` | [Deploy pipeline](doc:eng/deploy-pipeline) |
| Map crawler | Crawls the three sites and Substack into one graph | `scripts/crawl_map.py` | [Map crawler](doc:eng/map-crawler) |
| Inside | Front page with live status, deploys, experiments and dashboards | `inside/index.html` | [Inside portal](doc:eng/inside-portal) |
| Docs tree | This documentation, from markdown and the knowledge vault | `scripts/build_docs.py` | [Docs tree](doc:eng/docs-tree) |
| Service catalog | Every service with owner, tier, lifecycle, SLOs, dashboard and runbooks | `services/*.yml`, `scripts/build_inside.py` | [Service catalog](doc:eng/service-catalog) |
| Top bar and search | One bar on every Inside page and one search index | `scripts/inside_chrome.py`, `scripts/build_search.py` | [Top bar and search](doc:eng/top-bar-and-search) |
| Ticket board | Work items from GitHub Issues in columns | `scripts/board_snapshot.py`, `inside/board/index.html` | [Ticket board](doc:eng/board) |
| Observability | Prometheus, Loki and Grafana behind the public dashboards | [agent-observability](https://github.com/uncovertechtalent/agent-observability) | [Observability space](doc:obs/index) |

## Where to start

- New to the setup: read [Site architecture](doc:eng/site-architecture), then [Deploy pipeline](doc:eng/deploy-pipeline).
- Adding a page: follow [Add a page to machinebehavior.io](doc:eng/add-a-page).
- A deploy did not go out: start at [Runbooks](doc:eng/runbooks).
- Why something is the way it is: the [Decision log](doc:eng/decision-log).
