title: ADR-0050: The house ledger and the publishing pipeline reach Inside from the knowledge vault, label-gated
summary: The work the house tracks outside GitHub (the vault's bead records) and the pieces it is writing (the vault's drafts) reach Inside through two exports that a label or a front-matter line gates, each with a fixed contract, committed data, a check in the gate, and a refusal rather than a redaction when a record holds a private pattern; the board gains the ledger's lanes, every seat its ledger block, the publisher its pipeline in place of the placeholder.
parent: decision-log
order: 50
adr: 50
status: accepted
created: 2026-10-31
labels: adr, decision, inside, board, seats, publisher, vault
owner: Stefan Coetzee
reviewed: 2026-10-31
review_by: 2027-01-29
type: explanation
---
## Context

Inside shows the work of the house from GitHub only. [The board](/inside/board/) is the issues of this repository ([ADR-0011](doc:eng/adr-0011-ticket-board-from-github-issues)); [the cockpit](/inside/cockpit/) is the issues and pull requests of the owner's public repositories by area ([ADR-0031](doc:eng/adr-0031-cockpit-from-public-github-issues)); the seat dashboards on the landing page count and list those items ([ADR-0034](doc:eng/adr-0034-inside-intranet-theme-and-seat-tabs), [ADR-0049](doc:eng/adr-0049-seat-pane-grammar)). Most of the house's work is not an issue. Research runs, article drafts, the alignment of a practice with a doctrine, the monitoring fixes after a power cut, the FinOps dashboards: these are tracked as records in the bead tracker of the knowledge vault, a local repository with no remote, and written as drafts in the same vault. On 2026-10-31 the vault held 32 records closed in the previous two weeks and none of them appeared on any page, while the cockpit's done list for the same window was mostly alert records.

The publisher's dashboard has carried a placeholder since ADR-0034: "Publishing pipeline, not wired yet. No public data source feeds this panel yet, so it shows no count." The pieces it should list sit in the vault as drafts with a free-text status line.

The vault is private by design. It holds client names, household matters, host names and addresses of the home lab, and notes that must not leave the machine. [ADR-0009](doc:eng/adr-0009-vault-notes-with-review-label) already moves one part of it to the site, the SRE handbook and the standards clusters, through an import that redacts mechanically and labels every page as not reviewed against its source. The owner asked on 2026-10-31 for an overview of the house's work as tickets on Inside, and for the publisher's panel to show the pieces in the pipeline as teasers, the piece pending, the title and one line visible.

## Decision

**Two exports, gated at the source.** A bead reaches the site only when it carries the label `public`; a draft reaches the site only when its front matter says `teaser: public`. Nothing else in the vault is read. The exports run on the holder's machine, where the vault is (`scripts/export_ledger.py`, `scripts/export_pipeline.py`), and write two committed files, `inside/board/ledger.json` and `inside/publisher/pipeline.json`. The deploy job has no vault to read, so each file is as fresh as the last export, and every block that shows it says when that was.

**Fixed contracts, free text in one field each.** The ledger record is the bead id, the title, the area (one of the cockpit's eight, from the label `area:<key>`), the kind (`kind:<kind>`, else by the bead's type), the status, and the dates. No description, no notes, no close reason, no assignee, no link: a bead has no public page. The piece is the slug, the title, one standfirst, the stage (idea, drafting, review, live), the home surface, the address of a live piece on one of the house's surfaces, and the date its stage began. `scripts/build_ledger.py` and `scripts/build_pipeline.py` hold the contracts, in the form of the cockpit's: exactly these keys, fixed forms for every value, limits on length and count, and the checked file is the only thing a page renders.

**Refuse, never redact.** A title or a standfirst that holds a private pattern, a private or public address, a host shorthand, an e-mail address, a home path, a key path, the former employer's name, a placeholder word, is refused by name at export and again by the contract check in the gate, and nothing is written. ADR-0009 redacts on the way in because its pages are long and the redaction mark is itself information; a record is one line, and a redaction mark on a public ticket would say that something was there. So the record is fixed at its source and exported again. The patterns are the import's, kept in `scripts/vault_export.py`; the private user name the import redacts is not among them, because a bead title never carries a login. The pre-push hook on the holder's machine, which blocks the terms kept off this repository, stays the backstop and is not the control.

**Where it shows.** The board page gains a section under the board, the house ledger in four lanes, in progress, blocked, open, and done in the last 30 days (the board's own window), each record with its id, title, area, kind, and date. Every seat dashboard gains a block in its queue band ([ADR-0049](doc:eng/adr-0049-seat-pane-grammar)) with the ledger's records not done for the seat's areas, blocked first, and the done count and export time in its heading; a seat with no record in its areas gets nothing. The publisher's dashboard gets its pipeline in place of the placeholder: the counts by stage, then the pieces, the nearest to publication first (in review, drafting, idea), then the pieces live in the last 30 days, linked. The tab pill rule of [ADR-0036](doc:eng/adr-0036-inside-seat-tabs-as-folder-tabs) is unchanged: a tab's state still comes from the cockpit, since mixing two sources with two freshness times into one pill would hide which one is stale.

**No date a piece is due.** The house publishes when a piece is ready; a teaser shows the date its stage began and nothing that reads as a deadline.

**Checks.** The Conformity checks job runs `build_ledger.py --check`, `build_pipeline.py --check`, and the seat tabs' check, which now reads both files; data that breaks a contract can neither merge nor deploy, as the cockpit's cannot. Tests: `scripts/test_build_ledger.py`, `scripts/test_build_pipeline.py`, and the seat tabs' tests, which gain the two blocks.

## Consequences

The work of the house is visible as tickets a reader can count, by lane and by seat, including the work that never was an issue. The publisher's dashboard shows what is coming before it exists on any surface, which is the purpose of a teaser, and links each piece once it is live. The two files are as fresh as the last export, not the last deploy; each block says so, and an export is one command and one pull request. A stranger cannot inject a record: the vault is local, the label is set by hand, and the gate refuses a file that breaks the contract. The bead ids become stable public handles for work that has no issue number. What this does not do: link a record to a page (a next change may let a bead name one public address through a label), count the ledger into the tab pills, or import a record's body.

Built from `inside/board/ledger.json` by `scripts/build_ledger.py` and from `inside/publisher/pipeline.json` by `scripts/build_inside_seats.py`; the exports are `scripts/export_ledger.py` and `scripts/export_pipeline.py`.
