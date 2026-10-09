title: ADR-0026: Mission Control, the live operations view inside the portal
summary: One screen at /inside/mission-control/ shows the gate and deploy state of the three sites, the deploy feed, open incidents, this site's gate result and the public Grafana dashboards as tabs that load on a click, with a slot for the internal AWS spend panel.
parent: decision-log
order: 26
adr: 26
status: accepted
created: 2026-10-09
labels: adr, decision, inside, observability
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

The live state of the platform was spread over four places: the site cards and the deploy feed on the [Inside](/inside/) front page, the open incidents on the [status page](/inside/status/), the run record of the [gate](/conformity/), and the Grafana frames at the bottom of Inside. An operator who wants the state now had to read all four. The old research menu linked "infrastructure" to the Grafana section of Inside. Stefan Coetzee asked on 2026-10-09 for a view called Mission Control.

## Decision

[Mission Control](/inside/mission-control/) is one page in the Inside section of `site/nav.yml`, the first entry of the Inside sidebar, in place of the "Dashboards" anchor. Inside keeps its name and URL and links Mission Control first in its apps. The page has four summary figures (sites passing the gate, last deploy, open incidents, this site's gate), the three sites with gate result, last gate run, open findings and last deploy run, the last ten deploy runs, the open incidents with stage and impact, this site's gate result with its last 30 runs, and the public dashboards as tabs.

Every figure is read in the browser from records the sites already publish: each site's `/conformity/latest.json`, `/inside/deploys.json` (written by the deploy job), and `/inside/status/incidents.json`. The dashboard list moved to `/inside/dashboards.js`, which Inside and Mission Control both load. A Grafana frame loads only after a click on a tab or the load button, so opening the page sends no request to the Grafana host ([ADR-0010](doc:eng/adr-0010-no-third-party-requests)). The AWS spend panel is internal: its slot states that and links to [Budgets and alerts](doc:fin/budgets-and-alerts), where the internal view is described.

The old research menu is gone since [ADR-0021](doc:eng/adr-0021-one-navigation-source), so no "infrastructure" link remains to rename. Mission Control is reached from the Inside entry in the top bar, the Inside sidebar on every Inside page and the Inside front page. It stays out of the top bar, which holds sections only.

## Consequences

The deploy feed on Mission Control is as fresh as the last deploy of this site; the live view of deploys is the Website deploys dashboard. A record that cannot be read shows as "not readable" in place of a figure. The page holds no figure of its own, so it cannot drift from the status page or the gate.
