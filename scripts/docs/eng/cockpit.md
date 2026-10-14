title: Cockpit page
summary: How /inside/cockpit/ is built from the GitHub Issues of the owner's public repositories, which labels place an item, what the contract check allows, and where it runs.
order: 66
labels: inside, cockpit, issues, labels, how-to
owner: Stefan Coetzee
reviewed: 2026-10-14
review_by: 2027-01-12
type: how-to
---
The [cockpit page](/inside/cockpit/) is the CTO powersuit cockpit running on Stefan Coetzee's public work. It shows the issues and pull requests of the owner's public repositories on GitHub by area of the CTO job. For each area it has the open, in progress, blocked, and recently closed counts, the open items by kind, the age of the oldest, and the open items as cards. It also shows the totals and a 14-day trend. Decision record: [ADR-0031](doc:eng/adr-0031-cockpit-from-public-github-issues).

## Labels

Every public repository of the owner has these labels. The area and kind labels have no space after the colon. The board's own labels, such as `area: docs`, have one.

| Label | Meaning |
|---|---|
| `area:direction` | Where the company stands, and the big technical decisions |
| `area:delivery` | How code gets from an idea to production |
| `area:operations` | Keeping it running, and seeing what it does |
| `area:money` | What the platform costs, and where the money goes |
| `area:security` | Protecting systems and data, staying compliant, testing for failure |
| `area:ai` | Running AI in the company, and being found by AI |
| `area:people` | Hiring the team, and handing the work over |
| `area:knowledge` | The layer under every module: what agents know and how they answer |
| `kind:finding` | A gap that an audit or a review found |
| `kind:decision` | A choice still to make |
| `kind:action` | Work to do |
| `kind:lead` | A sales lead or an application |

An item reaches the page with its title only when it has an area label and its author is the owner, a member, or a collaborator. Anyone can open an issue on a public repository and edit its title later, so a label does not let a stranger's title onto the page. Other open items are counted per repository, without their text. The status of an open item comes from the board's labels: `status: blocked`, then `status: in progress`. An open pull request counts as in progress, and every other open item as open. Closed in 7 days counts issues closed as completed and pull requests merged. Issues closed as not planned or as duplicates, and pull requests closed without a merge, are left out of it.

To place an item, add its labels:

```bash
gh issue edit 83 --repo uncovertechtalent/machinebehavior.io --add-label area:security,kind:action
```

To give a new public repository the labels, create the twelve labels of the table on it, one at a time:

```bash
gh label create area:delivery --repo uncovertechtalent/<new-repo> --color C77D00 --description "CTO area: how code gets from an idea to production"
```

## How the data gets to the page

1. The deploy job runs `python3 scripts/build_cockpit.py --fetch` after the board's snapshot step. The job's token is this repository's workflow token, which reads no private repository of the owner.
2. The script lists the owner's repositories and stops if GitHub reports any of them as private or as another owner's. It skips forks, archived repositories, and repositories without issues.
3. From each repository it reads the open issues and pull requests, and those closed in the last 14 days. It keeps the items with an area label from the owner, members, and collaborators, and counts the other open items. Titles lose control characters and the characters that reorder or hide text.
4. It checks the result against the contract below and writes `inside/cockpit/cockpit.json` and the page blocks into the Pages artifact. If the read or the check fails, nothing is written and the committed page stays live.

The committed `cockpit.json` and page come from the same command, run by hand in a pull request. The area rows also take titles, lines, and plugins from `site/powersuit.yml` and `cto-powersuit/modules.json`, so `scripts/build_powersuit.py` rebuilds the page from its committed data after a pin move. The Conformity checks job runs `python3 scripts/build_cockpit.py --check` on them, before the gate. That job is the required check and the job the deploy waits for. The check fails when `cockpit.json` breaks the contract, or when the page's blocks or its sitemap date differ from it.

## The contract (schema 1)

| Key | Allowed |
|---|---|
| `schema` | `1` |
| `generated` | A UTC timestamp, `2026-10-14T14:00:00Z` |
| `owner` | `uncovertechtalent`, the value of `OWNER` in the script |
| `repos` | The repositories read, each `uncovertechtalent/<name>`, each once |
| `items` | Up to 1000 items with exactly `repo` (a listed repository), `number`, `pr` (true or false), `title`, `url`, `area` (one of the eight), `kind` (one of the four, or null), `status` (`open`, `in_progress`, `blocked`, `done`, or `dropped`), `created` (a date), and `closed` (a date, or null while open) |
| `untriaged` | Per listed repository, the count of open items shown without their text: no area label, or an author outside the owner's account and its collaborators |

A key outside the table, a key that appears twice in one object, a missing key, or a value of another form fails the check. An item's `url` must be `https://github.com/<repo>/issues/<number>`, or `.../pull/<number>` for a pull request. The title is the only free text: at most 300 characters, with no control characters and no characters that reorder or hide text (bidi overrides and isolates, zero widths). The page escapes it.

## Run it

```bash
python3 scripts/build_cockpit.py --fetch    # read GitHub, check, write cockpit.json and the page
python3 scripts/build_cockpit.py --check    # no network: the committed data meets the contract and matches the page
python3 scripts/test_build_cockpit.py       # the tests, also run in the Script tests job
```

Run `--fetch` without a token in your shell; the anonymous limit is enough for one read.

## Related

- [Ticket board](doc:eng/board): the issues of this site by status, with filters.
- [Inside portal](doc:eng/inside-portal): the cockpit next to Mission Control, the board, and the status page.
