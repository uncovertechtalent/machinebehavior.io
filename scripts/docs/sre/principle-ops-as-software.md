title: Operations work done as software
summary: SRE is operational knowledge plus software engineering, with automation in place of manual steps and tools in place of one-off scripts. Here generators build the catalog, status page, docs, map, board and changelog from sources in git, and each build checks its input.
parent: principles-in-practice
order: 40
labels: principle, sre, automation, generators
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
state: in place
source: [Manifesto](doc:sre/manifesto), SRE = Ops + software engineering; [Google SRE book ch. 7](https://sre.google/sre-book/automation-at-google/)
---
## The principle

SRE = operational knowledge + software engineering practices. The ops knowledge comes first, because nobody can automate work they do not understand. On top of it go automation in place of manual runbooks, tools in place of one-off scripts, SLOs in place of gut feel, and blameless postmortems. Google's chapter on automation ranks what automation gives: consistency first, then a platform others can extend, then faster repair and faster action, and time saved last.

Source: the formula in the [manifesto](doc:sre/manifesto); Google's [The Evolution of Automation at Google](https://sre.google/sre-book/automation-at-google/).

## On this platform

Each page an operator would otherwise update by hand is built from a source in git, and each build checks its input before it writes anything.

| Output | Source | Generator | What the build checks |
|---|---|---|---|
| [Service catalog](/inside/services/) | `services/*.yml` | `scripts/build_inside.py` | Unknown or missing fields, values outside the allowed set, docs links to missing pages, unknown dependencies |
| [Status page](/inside/status/) | `incidents/*.yml`, the gate record, the deploy feed | `scripts/build_inside.py` | Impact values, stages in order, services that exist in the catalog, ticket numbers |
| [Docs](/inside/docs/) | `scripts/docs/<space>/*.md` and the knowledge vault | `scripts/build_docs.py`, `scripts/import_vault_docs.py` | Unknown doc links, malformed dates, unknown types, decision records that disagree, principle state |
| [Map](/map/) | The three sites and Substack | `scripts/crawl_map.py` | Keeps the committed snapshot when a crawl comes back smaller ([ADR-0004](doc:eng/adr-0004-map-refresh-keeps-larger-snapshot)) |
| [Board](/inside/board/) | GitHub Issues | `scripts/board_snapshot.py` | Shows only issues with a type label |
| [Changelog](doc:eng/changelog) | Closed issues and commits | `scripts/build_changelog.py` | |
| Top bar, breadcrumbs, footer | `site/nav.yml` | `scripts/site_chrome.py` | Orphan pages, sitemap and llms.txt against the tree ([Site navigation and chrome](doc:eng/site-navigation)) |
| Grafana dashboards | `grafana/build.py` in agent-observability | The same file | A rebuild in a clean directory gave identical JSON on 2026-10-09 ([Dashboards as code](doc:obs/dashboards-as-code)) |
| Alert rules | `prometheus/rules/*.yml` in agent-observability | promtool | 21 test cases ([Alerts and SLOs](doc:obs/alerts-and-slos)) |

The YAML reader is `scripts/mini_yaml.py`, a strict subset in the standard library, so the builds need nothing installed beyond Python.

## State

**In place.** For the sites, the catalog, the status page, the docs, the map and the dashboards, the source is in git and a generator writes the output. Two exceptions are named on other pages: the builds run on the author's machine and CI does not repeat them ([Release engineering](doc:sre/principle-release-engineering)), and the observability stack is copied to its server by hand ([Eliminate toil](doc:sre/principle-eliminate-toil)).

## Services that name it

<!-- principle-services -->

## In a company of 10 to 200 people

- Before automating a task, have the person who does it by hand write it down as a runbook. The runbook is the specification for the automation.
- Prefer one generator per kind of page or config, with a schema check, over a wiki that people update by hand.
- Fail the build on bad input. A catalog that accepts an unknown field keeps a typo for a year.
- Judge automation by the consistency it gives first and by the hours it saves second.

## Open work

- [#40 CI check: generated pages match their sources](https://github.com/uncovertechtalent/machinebehavior.io/issues/40)
