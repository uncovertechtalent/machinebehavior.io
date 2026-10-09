title: ADR-0024: SRE principles tied to the running platform
summary: Fourteen hand-written principle pages in the SRE Handbook space link each principle to the services, records and docs that apply it, with a state per page; services name their principles in YAML, and the vault import keeps hand-written pages.
parent: decision-log
order: 24
adr: 24
status: accepted
created: 2026-10-09
labels: adr, decision, sre, principles
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

The SRE Handbook space is imported from the knowledge vault: the manifesto, the ten pillars, patterns, runbooks and incident records. None of it linked to the platform the site runs on, and the service catalog, the status page and the gate did not link back to the handbook. A reader saw the principles and the practice on separate pages and had to join them. Stefan Coetzee asked on 2026-10-09 to work the SRE principles into the docs and the map. The import also deleted `scripts/docs/sre/` on every run, so a page written in the repository for that space would not have survived a re-import.

## Decision

- **Pages.** A section [Principles in practice](doc:sre/principles-in-practice) in the SRE Handbook, with one hand-written page per principle: Stefan Coetzee's framework first (the substrate principle, SRE as a role in Ops, standby, SRE as Ops plus software engineering, the pillars, the AI-era extensions), Part II of Google's SRE book as the reference. Each page gives the principle and its source, how the platform applies it with links to live records, a state (`in place`, `partial` or `gap`) with the reason, what a company of 10 to 200 people would do, and the open issues.
- **One source for the links.** Each service YAML lists its principles under `principles:`. The service page shows them; the build writes the list of services onto each principle page and the index table onto the parent, from the same field ([Docs tree](doc:eng/docs-tree), [Service catalog](doc:eng/service-catalog)).
- **State checked at build.** The state sits in the front matter and opens the page's State section; the build stops when the two differ, or when a principle page lacks a state or a source.
- **The import keeps hand-written pages.** `scripts/import_vault_docs.py` removes only the files it wrote (those with an `origin` line) and stops when a vault note would overwrite a hand-written file.
- **Gaps on the board.** Each gap found during the review became an issue: alert routing ([#36](https://github.com/uncovertechtalent/machinebehavior.io/issues/36)), SLOs for the tier-1 services and the agents ([#37](https://github.com/uncovertechtalent/machinebehavior.io/issues/37)), an error budget policy ([#38](https://github.com/uncovertechtalent/machinebehavior.io/issues/38)), the rebase toil ([#39](https://github.com/uncovertechtalent/machinebehavior.io/issues/39)), a CI rebuild check ([#40](https://github.com/uncovertechtalent/machinebehavior.io/issues/40)) and detection times on incident records ([#41](https://github.com/uncovertechtalent/machinebehavior.io/issues/41)).

## Consequences

On 2026-10-09 two principles are in place, ten partial and two gaps; the pages say so, and the parent table shows it at a glance. The state is a judgement made at each review, and it goes stale like any other claim in the docs; the review date on each page is the control, and it is not enforced ([#27](https://github.com/uncovertechtalent/machinebehavior.io/issues/27)). A principle no service names shows "No service in the catalog names this principle", as the standby page does today. The map gains body links between the twelve service pages and the principle pages in both directions. Closing a gap means changing the platform first, then the page and its state.
