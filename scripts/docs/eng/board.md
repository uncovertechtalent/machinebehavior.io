title: Ticket board
summary: The board at /inside/board/ shows the work on the platform in columns, from GitHub Issues on the public repository, as a snapshot written at each deploy.
order: 65
labels: board, issues, workflow, inside
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: reference
---
The [board](/inside/board/) shows the open work on machinebehavior.io and the platform behind it, plus the work done in the last 30 days. GitHub Issues on [uncovertechtalent/machinebehavior.io](https://github.com/uncovertechtalent/machinebehavior.io/issues) is the system of record; the board is a read-only view of it.

## How the data gets to the page

1. The deploy job runs `scripts/board_snapshot.py` after the deploy feed step (see [Deploy pipeline](doc:eng/deploy-pipeline)).
2. The script reads the open issues and the issues closed in the last 30 days from the GitHub API, with the workflow token first and anonymously if that fails. Pull requests are skipped.
3. It writes `inside/board/issues.json` into the Pages artifact. The file is never committed (`.gitignore`).
4. The page reads that file. Opening the board sends no request to GitHub.

The board is as fresh as the last deploy of the site. Pushes to `main` deploy several times a day. To refresh without a push, run the workflow by hand:

```bash
gh workflow run conformity.yml --repo uncovertechtalent/machinebehavior.io
```

The workflow has no `issues` trigger, on purpose. Anyone can open an issue on a public repository, and each issue event would run the gate, write a bot commit and redeploy. See the [Decision log](doc:eng/decision-log).

## Triage and what the page shows

Only issues with a `type:` label are shown with their title and text. Only a maintainer can set labels, so the text of a new report reaches the page after someone has read it. The page counts untriaged reports and links to them on GitHub. Issues closed as not planned are left out.

## Labels

| Group | Labels | Meaning |
|---|---|---|
| Type | `type: feature`, `type: bug`, `type: chore`, `type: docs` | What kind of work. The board shows an issue only when it has one |
| Area | `area: inside`, `area: docs`, `area: map`, `area: gate`, `area: observability`, `area: legal`, `area: security`, `area: search` | Which part of the platform. An issue can carry more than one |
| Priority | `P0`, `P1`, `P2`, `P3` | P0 must close before anyone outside sees the platform; P3 is optional |
| Status | `status: ready`, `status: in progress`, `status: blocked` | The column. No status label means Backlog; closed means Done |

Milestones group the work by phase of the platform review: Phase 0 (legal and leaks), Phase 1 (enterprise layer), Phase 2 (depth) and Phase 3 (hosting).

## Workflow

1. **Report.** Anyone opens an issue, from the New issue button on the board or from the "report an issue" link on every docs page, which fills in the page title and URL.
2. **Triage.** A maintainer adds a type, an area and a priority, and a milestone when the work belongs to a phase. The issue shows in Backlog after the next deploy.
3. **Ready.** When the work is scoped (what, why, done when), add `status: ready`.
4. **In progress.** Whoever picks it up assigns it and changes the label to `status: in progress`.
5. **Blocked.** When it waits on a decision or an outside input, add `status: blocked` and write in the issue what it waits on.
6. **Done.** Close the issue with a comment that links the commit. It stays in Done for 30 days.

Issue text is public: plain English with what, why and done when, and no private addresses, host names, personal or financial details.

## Columns

| Column | Rule |
|---|---|
| Backlog | Open, no status label |
| Ready | Open, `status: ready` |
| In progress | Open, `status: in progress` |
| Blocked | Open, `status: blocked`; wins over the other two |
| Done | Closed as completed in the last 30 days |

Within a column, cards sort by priority, then by number. Done sorts by closing date, newest first. The filters for area, type and priority are kept in the URL (`?area=docs&priority=P1`), and `#issue-12` opens the drawer for issue 12.

## Related

- [Inside portal](doc:eng/inside-portal): the front page links the board as an app.
- Page source: `inside/board/index.html`. Snapshot script: `scripts/board_snapshot.py`.
