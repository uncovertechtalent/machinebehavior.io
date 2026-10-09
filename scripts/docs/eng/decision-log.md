title: Decision log
summary: Dated decisions behind the setup, each with the reason and the consequence, in the shape of architecture decision records.
order: 80
labels: adr, decisions, governance
---
Each entry records one decision: the date, what was decided, why, and what it costs. Newest first. Decisions are made by Stefan Coetzee unless the entry says otherwise.

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
