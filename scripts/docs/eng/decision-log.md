title: Decision log
summary: Dated decisions behind the setup, each with the reason and the consequence, in the shape of architecture decision records.
order: 80
labels: adr, decisions, governance
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
Each entry records one decision: the date, what was decided, why, and what it costs. Newest first. Decisions are made by Stefan Coetzee unless the entry says otherwise.

## 2026-10-09: state the on-call model, propose Alertmanager routing

- **Decision.** An [On-call and escalation](doc:obs/on-call) page states the model as it runs: one operator, agent sessions as responders, the deploy gate as the only control that acts on its own, and 13 alert rules with no Alertmanager, so nothing pages anyone. It proposes a routing (pages to a push receiver in waking hours, tickets to the board, a Watchdog heartbeat, inhibition) and leaves it unwired.
- **Why.** A founder checking the setup asks who gets woken up. Saying "nobody" is accurate; wiring a page to a personal device needs the operator's choice of receiver.
- **Consequence.** Alerts stay visible only to someone who looks. The four incidents of the week were all found that way.

## 2026-10-09: a public-demo banner and a stated access model

- **Decision.** Every Inside page except the map carries a banner saying the intranet is a public demo and that in production it sits behind single sign-on, linking an [Access model](doc:eng/access-model) page: public, internal and restricted spaces, who grants each, and access per user and device without a network perimeter. No login and no credential form exist on the site.
- **Why.** A visitor should know the intranet is public on purpose, and a founder reading it should see how access would work in a company.
- **Consequence.** The model is a description; the one part of it that runs is the Grafana front door, which passes only the public paths. Hosting stays on GitHub Pages.

## 2026-10-09: owner and review dates on every docs page

- **Decision.** Docs front matter gains `owner`, `reviewed`, `review_by` and `type` (Diátaxis). All 50 hand-written pages carry the four fields, with the date each was written from its source as the first review and the next review 90 days later. Vault pages start as not reviewed and take the space owner. The byline shows the state and [Docs health](/inside/docs/health/) lists what is missing or late.
- **Why.** The pages carried dates, but none said who keeps it true or when it was last checked.
- **Consequence.** The first reviews fall due in January 2027. No gate check: whether a missing owner or an overdue review should block a deploy is an open decision, owned with the gate. See [Docs tree](doc:eng/docs-tree).

## 2026-10-09: a status page from records the site already publishes

- **Decision.** `/inside/status/` reads each site's `conformity/latest.json`, `/inside/deploys.json` and the map snapshot time in the browser, and shows the incident history from `incidents/*.yml` with the stages Investigating, Identified, Monitoring and Resolved. Services the site has no record for say "No live check" and link their dashboard; the page does not call Grafana or Prometheus.
- **Why.** A visitor could see metrics on the dashboards but not, at a glance, whether a service is healthy or what went wrong last week. Reading only published records keeps the rule of no third-party request on load.
- **Consequence.** Six of twelve services have a live check on the page. The incident history starts with four real incidents from 2026-10-08 and 2026-10-09; times without a record behind them are shown as "time not recorded". See [Status page](doc:eng/status-page).

## 2026-10-09: a service catalog from YAML in the repository

- **Decision.** Every service is one YAML file in `services/`; `scripts/build_inside.py` validates the files and builds `/inside/services/`, a page per service and `services.json`. The reader is a strict subset parser in the standard library (`scripts/mini_yaml.py`), so the build needs no package. Service pages are `service` nodes in the map, and the public dashboards they link become `dashboard` nodes.
- **Why.** The systems were documented page by page, but nothing listed them in one place with who answers for each, how much it matters and where its runbooks are.
- **Consequence.** A service without docs or runbooks shows the gap on its page. Twelve services at the start, all owned by one person: the owner field names who is accountable, and no team structure sits behind it. See [Service catalog](doc:eng/service-catalog).

## 2026-10-09: one top bar and one search index for Inside

- **Decision.** Every Inside page carries one top bar, written by `bar()` in `scripts/inside_chrome.py`: generators call it, hand-written pages hold a marked block the script rewrites. One index, `/inside/search.json`, merges the docs, the services and the map; the search box is a form that submits to `/inside/search/`, so Enter opens a results page. The deploy job rebuilds the index after the map refresh, artifact only.
- **Why.** There were three navigations (site menu, Inside header, docs bar) and two search boxes over two indexes, and docs search opened the first hit on Enter. A reader could not search the docs from Inside, or the published work from the docs.
- **Consequence.** A new Inside page must carry the marked block and be listed in `SYNCED`; `python3 scripts/inside_chrome.py --check` reports drift. The index is about 190 KB and loads when the box gets focus. See [Top bar and search](doc:eng/top-bar-and-search).

## 2026-10-09: a public ticket board from GitHub Issues

- **Decision.** Work items are GitHub Issues on the public repository, shown on [the board](/inside/board/). The deploy job writes `inside/board/issues.json` from the Issues API in a new artifact-only step (`scripts/board_snapshot.py`), and the workflow permissions gain `issues: read`. The workflow gets no `issues` trigger.
- **Why.** The backlog from the platform review belongs in one public system of record. Reading a snapshot keeps visitors' browsers off the GitHub API, as for the deploy feed. An `issues` trigger would let anyone who opens an issue start a gate run, a bot commit and a deploy.
- **Consequence.** The board is as fresh as the last deploy; a manual run of the workflow refreshes it. Only issues with a type label are shown, so a new report waits for triage before its text appears on the site. See [Ticket board](doc:eng/board).

## 2026-10-09: no third-party requests on page load

- **Decision.** Fonts (Space Grotesk, JetBrains Mono) and d3 are served from the site itself, and the Inside deploy feed is a JSON written by the deploy job. Opening a page sends no request to Google, a CDN or the GitHub API.
- **Why.** A request to a font or script server passes the visitor's IP address to that company; the LG München I judgment of 2022-01-20 (3 O 17493/20) found this unlawful for Google Fonts loaded without consent. It also removes the GitHub API rate limit of 60 requests per hour per visitor.
- **Consequence.** The deploy feed on Inside is as fresh as the last deploy of this site; the live view is the Website deploys dashboard. Font and d3 updates are manual (`fonts/`, `vendor/`).

## 2026-10-09: publish vault notes with a review label

- **Decision.** The SRE folder and 28 standards clusters of the knowledge vault are published as docs spaces, with private addresses, e-mail addresses and the former employer's name redacted, and a label on every page saying it has not been reviewed against its source.
- **Why.** The vault holds the reference work; the label keeps the accuracy claim at the level the evidence supports.
- **Consequence.** About 300 pages carry the label until each is checked. See [Docs tree](doc:eng/docs-tree).

## 2026-10-09: docs pages are map nodes

- **Decision.** Docs pages carry their front matter as meta tags, and the crawler adds them to the graph with parent links.
- **Why.** One graph for everything published, so a reader or a model can walk from a claim to the reference note it rests on.
- **Consequence.** The graph grows from about 120 to over 400 nodes; the map gets a filter for docs.

## 2026-10-08: deploys feed Grafana without changing the workflows

- **Decision.** A separate exporter polls the GitHub Actions API and writes runs, steps and gate checks to Loki and Prometheus.
- **Why.** The site workflows stay as they are; the private repository's titles, SHAs and URLs are never stored.
- **Consequence.** Data arrives on the exporter's polling interval. See [Deploy exporter](doc:obs/deploy-exporter).

## 2026-10-08: the map refresh keeps the larger snapshot

- **Decision.** The deploy job replaces `map/graph.json` only when the new crawl has at least as many nodes and links.
- **Why.** Substack answers some runners with 403; a partial crawl would shrink the map.
- **Consequence.** A real removal shows only after a local crawl is committed.

## 2026-10-07: the deploy is gated

- **Decision.** GitHub Pages deploys from Actions, and the deploy job depends on the conformity job.
- **Why.** A check that runs after the page is live only detects; a gate prevents.
- **Consequence.** A false positive blocks a deploy until the sentence is rewritten or the rule is demoted. See [Conformity gate](doc:eng/conformity-gate).

## 2026-10-07: root-absolute links only

- **Decision.** Internal links are root-absolute directory URLs (`/man/`), never relative and never `.html`.
- **Why.** Pages move between hosts and previews without broken links, and every URL has one form.
- **Consequence.** Generators and hand-written pages follow the same rule; the gate enforces it.
