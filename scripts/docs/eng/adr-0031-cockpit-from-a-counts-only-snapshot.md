title: ADR-0031: The cockpit page is built from a counts-only snapshot behind a contract check
summary: /inside/cockpit/ shows the work in the eight areas of the CTO job as counts, written by scripts/build_cockpit.py from inside/cockpit/snapshot.json; a contract check in the Conformity checks job stops any key outside the contract and any free text outside the titles of public items; snapshots arrive by pull request.
parent: decision-log
order: 31
adr: 31
status: accepted
created: 2026-10-14
labels: adr, decision, inside, cockpit, generated-pages, privacy
owner: Stefan Coetzee
reviewed: 2026-10-14
review_by: 2027-01-12
type: explanation
---
## Context

Stefan Coetzee runs his work in the cockpit, a local app that shows every task, finding, and decision by the eight areas of the CTO powersuit, with a scorecard per area and the trend. The data is his own: item text, names, and private work. It stays on his machine. Under the [zero trust principle](doc:sre/principle-zero-trust), anything that leaves it is checked where it is used. On 2026-10-14 he asked for a version of the cockpit on Inside, so that the same structure is visible in public as the demo of the company version.

## Decision

[The cockpit page](/inside/cockpit/) is one page in the Inside section of `site/nav.yml`, after Mission Control. It is static: `scripts/build_cockpit.py` writes its blocks from `inside/cockpit/snapshot.json`, and the page reads nothing in the browser.

The snapshot is the output of the cockpit's `export --public-json`, schema 1. The build checks it against the contract before it writes anything, and stops on any violation:

- exactly the keys of the contract at every level, no key twice, no NaN;
- counts are integers from 0; the timestamp, the source, and the area keys and names have fixed forms;
- the totals are the sums of the eight areas, so no count from work outside the eight areas reaches the page;
- the only free text is the title of a public item, which is a pull request or an issue on GitHub in a repository of an owner on the list `PUBLIC_OWNERS` in the script, with a URL that matches its repository and kind.

The same check runs as `python3 scripts/build_cockpit.py --check` in the Conformity checks job, before the gate. That job is the required check on pull requests and the job the deploy waits for, so a snapshot that breaks the contract can neither merge nor deploy. `--check` also fails when the page or its sitemap date differ from the snapshot, so nothing on the page between the cockpit markers comes from anywhere else.

Each area row names the plugins that do its work and links their pages; the area titles, lines, and plugin lists come from `site/powersuit.yml` and `cto-powersuit/modules.json`. The page does not repeat the other Inside views: [Mission Control](/inside/mission-control/) shows the operations of the three sites, and [the board](/inside/board/) the issues of this site. The cockpit lists the open pull requests and the issues of other public repositories, and for this site's issues gives the count and links the board.

A new snapshot reaches the page through a pull request: export, `python3 scripts/build_cockpit.py --snapshot FILE`, review the diff, open the pull request ([ADR-0029](doc:eng/adr-0029-changes-through-pull-requests)). Steps: [Cockpit page](doc:eng/cockpit).

## Consequences

The page is as fresh as the last merged snapshot, and its date is on the page. Until the first export arrives, the snapshot is the sample file with the source `fixture`, and the page labels its figures as sample figures. An export that names a repository of another owner fails the check until a reviewed pull request adds the owner to `PUBLIC_OWNERS`. Titles of public items reach the page, where the gate scans them like any other page text.

A scheduled export is the later path and is not built: the machine that runs the cockpit exports on a timer, pushes the snapshot to a branch with a deploy key of its own that can write branches only, and the machine account opens the pull request; the contract check in CI stays the gate. The page carries the definition of the CTO powersuit in the same words as the other pages that use the term, so it is one more input to [the CTO powersuit experiment](/your-next-cto/experiment/).
