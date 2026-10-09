title: Docs tree
summary: How this documentation is built from markdown sources and the knowledge vault, how front matter becomes the tree, labels and dates, and how pages enter the map.
order: 70
labels: docs, generator, front-matter
---
The docs at [/inside/docs/](/inside/docs/) are static pages built by `scripts/build_docs.py` from markdown files in `scripts/docs/<space>/`. Four spaces are written by hand in the repository (Engineering, Observability, Research, FinOps); two come from the knowledge vault through `scripts/import_vault_docs.py`.

## Build

```bash
python3 scripts/import_vault_docs.py ~/vault   # vault spaces: sre, std (only on the machine with the vault)
python3 scripts/build_docs.py                  # all spaces, sitemap block, llms.txt section, search index
```

The build writes one `index.html` per page, `inside/docs/search.json` for the search box, a managed block in `sitemap.xml` and a managed section at the end of `llms.txt`. Then run the gate dry run and push as usual.

## Front matter

| Field | Use |
|---|---|
| `title`, `summary` | Required. The summary is the meta description, the line in child-page lists and the search snippet |
| `parent` | Slug of the parent page in the same space; empty means under the space home |
| `order` | Sort key among siblings |
| `labels` | Comma-separated; written as `article:tag` metas and shown as chips |
| `created`, `updated` | Dates; without them the build uses the git date of the source file |
| `origin`, `reviewed` | Vault pages only: the vault path, and `no` for the review label |

## Links

- `[text](doc:space/slug)` links to another docs page; an unknown target stops the build.
- Vault notes keep their wikilinks. A wikilink to a note in the export becomes a link; a link to a note outside it shows as plain text with a dotted underline.
- Every page lists the pages that link to it under "Linked from".

## In the map

Each page carries `<meta name="docs-space">`, `article:tag` metas, dates and `<link rel="up">` to its parent. The [map crawler](doc:eng/map-crawler) turns those into `doc` nodes, `tree` links and labels, so the documentation is part of the [map of the work](/map/).

## Vault import rules (2026-10-09)

- In: `SRE/` without `homelab/`, `.claude/` and `CLAUDE.md`; 28 standards clusters under `pillars/`.
- Redacted: private IPv4 addresses and LAN shorthand, e-mail addresses, the former employer's name, home directory paths, private host names. Each change is listed in `scripts/docs/IMPORT-REPORT.md`.
- ISO clause notes: blockquotes are dropped unread, so no standards text is machine-processed.
- Every vault page carries a label: not reviewed against the source.
