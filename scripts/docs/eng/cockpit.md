title: Cockpit page
summary: How /inside/cockpit/ is built from the counts-only snapshot of the cockpit, what the snapshot contract allows, what the check in the deploy gate stops, and how to publish a new snapshot.
order: 66
labels: inside, cockpit, snapshot, how-to, privacy
owner: Stefan Coetzee
reviewed: 2026-10-14
review_by: 2027-01-12
type: how-to
---
The [cockpit page](/inside/cockpit/) shows Stefan Coetzee's work in the eight areas of the CTO job as counts: per area, the open, in progress, blocked, and recently closed items, the open items by kind, and the age of the oldest; for all areas, the totals and a 14-day trend; and the open pull requests and issues in public repositories. The cockpit itself is a local app, and its data stays on his machine. The page gets one file from it, the snapshot, through a pull request. Decision record: [ADR-0031](doc:eng/adr-0031-cockpit-from-a-counts-only-snapshot).

## Files

| File | What it is |
|---|---|
| `inside/cockpit/snapshot.json` | The published snapshot, served at [/inside/cockpit/snapshot.json](/inside/cockpit/snapshot.json) |
| `inside/cockpit/index.html` | The page; the build writes the blocks between `<!-- static:cockpit-* -->` markers, the rest is written by hand |
| `inside/cockpit/cockpit.css` | The page's styles, from the design tokens |
| `scripts/build_cockpit.py` | The contract check and the build |
| `scripts/test_build_cockpit.py` | Tests of the check and the blocks, run in the Script tests job |
| `scripts/fixtures/cockpit-snapshot.json` | The sample snapshot (source `fixture`) the tests start from |

## The snapshot contract (schema 1)

| Key | Allowed |
|---|---|
| `schema` | `1` |
| `generated` | A UTC timestamp, `2026-10-14T14:00:00Z` |
| `source` | `beads-desk@<commit>`, or `fixture` for the sample file; the page labels a fixture as sample figures |
| `areas` | The eight areas, each once: `key` and `name` from a fixed list (`direction` Direction, `delivery` Delivery, `operations` Operations, `money` Money, `security` Security, `ai` AI, `people` People, `knowledge` Knowledge), and the counts `open`, `in_progress`, `blocked`, `closed_7d`, `findings_open`, `decisions_open`, `actions_open`, `oldest_open_days` |
| `totals` | `open`, `in_progress`, `blocked`, `closed_7d`, each the sum over the eight areas |
| `trend` | Days in date order, each with `date`, `open` (items not closed by the close of that day), and `closed` (closed that day); the page shows the last 14 |
| `public_items` | Up to 200 items with `repo`, `kind` (`pr` or `issue`), `title`, `url`, and `state` (`open`, `closed`, or `merged`); the page lists the open ones |

Every count is an integer from 0. A key outside the table, a key that appears twice in one object, a missing key, or a value of another form fails the check. The title of a public item is the only free text: at most 300 characters, no control characters, no `<` or `>`. An item's owner must be on `PUBLIC_OWNERS` in `scripts/build_cockpit.py` (now `uncovertechtalent`), and its URL must be `https://github.com/<repo>/pull/<n>` for a pull request or `.../issues/<n>` for an issue.

The cockpit's exporter refuses to write a file that breaks the same contract. The check here does not trust that: it runs again wherever the file is used.

## Where the check runs

- `python3 scripts/build_cockpit.py` checks the snapshot before it writes the page, and stops on any violation.
- `python3 scripts/build_cockpit.py --check` runs as the step "Cockpit snapshot matches the contract and the page" in the Conformity checks job, before the gate. That job is the required check on pull requests, and the deploy waits for it. The step also fails when the page's blocks or its sitemap date differ from the snapshot.
- `python3 scripts/test_build_cockpit.py` runs in the Script tests job.

## Publish a new snapshot

1. On the machine that runs the cockpit: `python3 -m beads_desk export --public-json FILE`.
2. In a clone of this repository, on a branch from `origin/main`: `python3 scripts/build_cockpit.py --snapshot FILE`. It checks the file, copies it to `inside/cockpit/snapshot.json`, writes the page blocks, and sets the page's sitemap date to the snapshot's date.
3. Read the diff: counts, dates, and the public items, nothing else.
4. Run the gate dry run, then open a pull request titled `ADR-0031 Cockpit snapshot <date>` ([ADR-0029](doc:eng/adr-0029-changes-through-pull-requests)).

## Later: a scheduled export

Not built. The machine that runs the cockpit exports on a timer and pushes the snapshot to a branch with a deploy key of its own, which can write branches only; the machine account opens the pull request, and the contract check in CI stays the gate. Until then, a snapshot is published by hand as above.

## Related

- [Inside portal](doc:eng/inside-portal): the cockpit next to Mission Control, the board, and the status page.
- [Ticket board](doc:eng/board): the issues of this site, which the cockpit counts and links instead of listing.
