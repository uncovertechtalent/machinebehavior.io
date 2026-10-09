title: Docs tree
summary: How this documentation is built from markdown sources and the knowledge vault, how front matter becomes the tree, labels and dates, and how pages enter the map.
order: 70
labels: docs, generator, front-matter
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: reference
---
The docs at [/inside/docs/](/inside/docs/) are static pages built by `scripts/build_docs.py` from markdown files in `scripts/docs/<space>/`. Four spaces are written by hand in the repository (Engineering, Observability, Research, FinOps); two come from the knowledge vault through `scripts/import_vault_docs.py`. A vault space can also hold hand-written pages: the SRE Handbook carries [Principles in practice](doc:sre/principles-in-practice), written in the repository. A page is hand-written when its front matter has no `origin` line, in any space.

## Build

```bash
python3 scripts/import_vault_docs.py ~/vault   # vault spaces: sre, std (only on the machine with the vault)
python3 scripts/build_changelog.py             # eng/changelog.md from closed issues and commits (needs the network)
python3 scripts/build_docs.py                  # all spaces, sitemap block, llms.txt section, docs search index
python3 scripts/build_inside.py                # bar sync, services, status, the site-wide search index
```

The build writes one `index.html` per page, `inside/docs/search.json` (an input to the site-wide index; see [Top bar and search](doc:eng/top-bar-and-search)), a managed block in `sitemap.xml` and a managed section at the end of `llms.txt`. Then run the gate dry run and push as usual.

## Front matter

| Field | Use |
|---|---|
| `title`, `summary` | Required. The summary is the meta description, the line in child-page lists and the search snippet |
| `parent` | Slug of the parent page in the same space; empty means under the space home |
| `order` | Sort key among siblings |
| `labels` | Comma-separated; written as `article:tag` metas and shown as chips that open the search results for the label |
| `created`, `updated` | Dates; without them the build uses the git date of the source file |
| `owner` | Who keeps the page true. Required on hand-written pages; a vault page without one takes the space owner |
| `reviewed` | The date the page was last checked against the system or source it describes, or `no`. For a hand-written page, the date it was written from the source counts as the first review. Vault pages start as `no` |
| `review_by` | The date of the next review; 90 days after `reviewed` by default |
| `type` | `tutorial`, `how-to`, `reference` or `explanation` ([Diátaxis](https://diataxis.fr/)). A vault note keeps its own note type, mapped to one of the four where the mapping is plain (`runbook` to how-to, `MOC` to reference, `position` to explanation) |
| `origin` | Vault pages only: the vault path. The import removes and rewrites only pages with this line |
| `state`, `source` | Principle pages only (children of `sre/principles-in-practice`): `in place`, `partial` or `gap`, and the source of the principle as markdown links. The build stops when `state` differs from the bold word that opens the page's `## State` section |

## Ownership and review

The byline of each page shows the owner, the review date and the next review date, or "not reviewed", or "review overdue since" in red. [Docs health](/inside/docs/health/) lists the pages past their review date, those due in the next 30 days, pages without an owner or a type, and the counts per space. The build stops on a malformed date or an unknown type, and prints a warning for a hand-written page that lacks one of the four fields. Nothing here blocks a deploy: whether the gate should check owners and review dates is an open decision for the gate owner.

## Decision records

A page with `adr: N` in its front matter is a numbered decision record under [Decision records](doc:eng/decision-log). It also carries `status` (`proposed`, `accepted`, `superseded`) and, when one record replaces another, `supersedes` on the new one and `superseded_by` on the old one. The build stops when the two sides disagree or two records share a number, and writes the index table where the parent page holds the marker `<!-- adr-index -->`.

## Links

- `[text](doc:space/slug)` links to another docs page; an unknown target stops the build.
- Vault notes keep their wikilinks. A wikilink to a note in the export becomes a link; a link to a note outside it shows as plain text with a dotted underline.
- Every page lists the pages that link to it under "Linked from".

## Principle pages

The pages under [Principles in practice](doc:sre/principles-in-practice) tie each SRE principle to the platform. Two markers, each on a line of its own, are filled at build time:

- `<!-- principle-services -->` on a principle page: the services whose YAML names the page under `principles:` (see [Service catalog](doc:eng/service-catalog)), as links.
- `<!-- principle-index -->` on the parent: a table of every principle with its source, state and services.

A `principles:` entry that names a page outside that section stops the build. The service page shows the same list under "SRE principles applied", so each link exists in both directions and the map records both.

## In the map

Each page carries `<meta name="docs-space">`, `article:tag` metas, dates and `<link rel="up">` to its parent. The [map crawler](doc:eng/map-crawler) turns those into `doc` nodes, `tree` links and labels, so the documentation is part of the [map of the work](/map/).

## Vault import rules (2026-10-09)

- In: `SRE/` without `homelab/`, `.claude/` and `CLAUDE.md`; 28 standards clusters under `pillars/`.
- Kept (since 2026-10-09): on each run the import removes only the files it wrote before, those with an `origin` line, and leaves hand-written pages in `scripts/docs/sre/` and `scripts/docs/std/` in place. A vault note whose slug equals a hand-written file name stops the import with an error; rename one of the two. Before this change the import deleted both folders.
- Redacted: private IPv4 addresses and LAN shorthand, e-mail addresses, the former employer's name, home directory paths, private host names. Each change is listed in `scripts/docs/IMPORT-REPORT.md`.
- ISO clause notes: blockquotes are dropped unread, so no standards text is machine-processed.
- Every vault page carries a label: not reviewed against the source.
