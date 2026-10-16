title: ADR-0032: The masthead is built from a public seats file
summary: /inside/masthead/ shows the seats of the house, the holder of each, the machinery that runs its staff work, and the gates that apply with where each one runs, written by scripts/build_masthead.py from inside/masthead/seats.json; a contract check in the required job refuses a file outside the contract; the house name sits in one field; the product of the seats is called the C-suit.
parent: decision-log
order: 32
adr: 32
status: accepted
created: 2026-10-16
labels: adr, decision, inside, masthead, generated-pages, seats
owner: Stefan Coetzee
reviewed: 2026-10-16
review_by: 2027-01-14
type: explanation
---
## Context

The one-person publishing effort behind this site became a publishing house run on the engineering practices of a CTO, with a seat for each C-level function whose staff work can be automated: chief executive, chief AI and technology officer, chief financial officer, chief human resources officer, publisher, and chief knowledge officer. Each seat reads some of the eight areas of the [cockpit](/inside/cockpit/), its staff work runs on the modules of the CTO powersuit, and a bundle per seat (a manifest over the shared modules plus one lens skill) is the plan. One person holds every seat today; a company that installs the same seats splits them across people as it grows.

A reader of the site needs to see who holds which seat, what machinery does the seat's work, and which checks a change in the seat's scope passes. The house's own rule applies: a claim that cannot be verified is labelled, so a gate that does not run on this site cannot be listed as if it did. The page also carries the editorial standards, which no page stated before.

## Decision

[The masthead](/inside/masthead/) is one page in the Inside section of `site/nav.yml`, after the cockpit. It is static: `scripts/build_masthead.py` writes its blocks from `inside/masthead/seats.json`, and the page keeps the static seats sections as its content with no script.

`seats.json` is the public copy of the seats file of the house. It holds, per seat, the key, the title, the holder, the areas, the bundle (null until one exists), the lens (two to six questions), the machinery (name and one line each), and the gates (check, where it runs, and one line each). Three choices sit in the file rather than in the page:

- The house name is the one field `house`; every mention in the generated blocks comes from it, so a rename is one edit.
- Every gate carries a `where` from the file's own `where` map: `site gate` (runs in this site's deploy gate), `module repository` (runs in the CTO powersuit's own checks), `pre-push` (runs on the holder's machine), `module` (ships with the module and runs where the module is fitted, which this site's gate does not), or `policy` (a rule followed by hand, with its open item where one exists). The page explains the map and shows the chip on every gate row.
- The seats together are named the C-suit: suit as in powersuit, one suit per seat, the whole suit for a company. The product is never written "C-suite". The repository of the modules keeps its name for now.

The page has one tab per seat next to the static seats tab. A seat's tab is its dashboard: the lens questions from `seats.json` (the questions the seat asks of a finding), then the cockpit's panels for the seat's areas only, rendered by the functions of `scripts/build_cockpit.py` from `inside/cockpit/cockpit.json`, the cockpit's one data source ([ADR-0031](doc:eng/adr-0031-cockpit-from-public-github-issues)); no new data source. The chief executive's tab shows every area at the level of the cockpit's totals, plus the open decisions across all areas. The tabs are radio inputs and styles with no script, and the seats tab is the default, so a reader without styles sees every panel in order. The deploy job rebuilds the page after the cockpit's fetch, artifact only, so the tabs are as fresh as the cockpit.

`check()` allows exactly the keys of the contract at every level, no key twice, no JSON constant, fixed forms for every value (a seat from the fixed list, each once and in masthead order; areas from the cockpit's eight; a bundle that is null or a slug; names and holders in a short allowed form), and bounded free text with no markup, no control or format character, and no URL. The area titles come from the cockpit generator, which reads them from `site/powersuit.yml` and `cto-powersuit/modules.json` ([ADR-0031](doc:eng/adr-0031-cockpit-from-public-github-issues)). The Conformity checks job runs `--check` before the gate: it fails when the file breaks the contract, when the page's blocks differ from what the file gives, or when the sitemap date of the page differs from the file's `updated` date, so nothing between the masthead markers comes from anywhere else. `scripts/test_build_masthead.py` runs in Script tests.

The editorial standards on the page state what the house does: sources and verification, the gates every piece passes, and how corrections are made. Where a mechanism is a policy or has an open item, the page says so and names the item.

## Consequences

A seat that moves to another person is one changed line in `seats.json`, then a rebuild. A gate added to a seat needs its `where`; a gate this site does not run cannot be listed as a site gate. The file is hand-edited until the seats file of the local cockpit exists and a local command writes the public copy from it; the plan for that step lives outside this repository.

The page carries the definition of the CTO powersuit in the same words as the other pages that use the term. Steps and the contract: [Masthead page](doc:eng/masthead).
