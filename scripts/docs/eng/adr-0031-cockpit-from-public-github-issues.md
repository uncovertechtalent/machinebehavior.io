title: ADR-0031: The cockpit page is built from the public GitHub Issues of the owner's repositories
summary: /inside/cockpit/ shows the issues and pull requests of the owner's public repositories by area of the CTO job, written by scripts/build_cockpit.py at each deploy from the GitHub API; a contract check in the build and in the Conformity checks job lets only public GitHub data reach the page.
parent: decision-log
order: 31
adr: 31
status: accepted
created: 2026-10-14
labels: adr, decision, inside, cockpit, generated-pages, issues
owner: Stefan Coetzee
reviewed: 2026-10-14
review_by: 2027-01-12
type: explanation
---
## Context

Stefan Coetzee runs his work in the cockpit, a view that shows every task, finding, and decision by the eight areas of the CTO powersuit, with a scorecard per area and the trend. His own install runs on beads, a local issue tracker, and that data stays on his machine. On 2026-10-14 he asked for a version of the cockpit on Inside as a demo, and chose GitHub Issues as its data: an install can run the cockpit on beads or on GitHub Issues, and the public work is on GitHub already.

## Decision

[The cockpit page](/inside/cockpit/) is one page in the Inside section of `site/nav.yml`, after Mission Control. It is static: `scripts/build_cockpit.py` writes its blocks from `inside/cockpit/cockpit.json`, and the page reads nothing in the browser.

The data is the open issues and pull requests, and those closed in the last 14 days, of the owner's own public repositories (no forks, nothing archived). Two labels place an item: `area:<area>` for one of the eight areas, and `kind:<kind>` for finding, decision, action, or lead. Both exist on every public repository of the owner. An item reaches the page with its title only when a maintainer has given it an area label; other open items are counted per repository, without their text, as [the board](doc:eng/board) does with untriaged issues. Blocked and in progress come from the board's status labels, and an open pull request counts as in progress.

Only public GitHub data reaches the page:

- `--fetch` reads the repositories from the GitHub API, with `GH_TOKEN` if set and else with no token. In the deploy job `GH_TOKEN` is this repository's workflow token, which reads no private repository of the owner. The read stops, and writes nothing, on any repository that GitHub does not report as public or that belongs to another owner.
- `check()` allows exactly the keys of the contract at every level, no key twice, fixed forms for every value, and as free text only an item's title. Each item's URL must be the GitHub URL of that issue or pull request in a listed repository of the owner.
- The deploy job runs `--fetch` after the board's snapshot (artifact only, never committed), so the live page is as fresh as the last deploy. A failed read or check leaves the committed page in place.
- The Conformity checks job runs `--check` on the committed `cockpit.json`, before the gate. It also fails when the page's blocks or its sitemap date differ from the data, so nothing between the cockpit markers comes from anywhere else.

Each area row names the plugins that do its work and links their pages. The area titles, lines, and plugin lists come from `site/powersuit.yml` and `cto-powersuit/modules.json`. The board stays the view of this site's issues by status, and the cockpit is the view of all public repositories by area. Each page links the other.

## Consequences

Labelling is part of the work: an issue without an area label is only counted. The labels `area:<area>` and `kind:<kind>` have no space after the colon. The board's own labels (`area: docs`, `area: gate`) have one, and the two sets stay apart. A repository of another owner needs a reviewed change to `OWNER` in the script. Titles reach the live page at deploy time without the gate's text scan; on the committed copy, the gate scans them like any other page text.

The page carries the definition of the CTO powersuit in the same words as the other pages that use the term, so it is one more input to [the CTO powersuit experiment](/your-next-cto/experiment/). Steps and the contract: [Cockpit page](doc:eng/cockpit).
