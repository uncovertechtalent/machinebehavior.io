title: ADR-0046: The articles index lists the research pieces that live on Substack
summary: The Articles index page also lists research-facing pieces whose home is another site, from an `elsewhere` list on its entry in site/nav.yml, merged by date with the site's own articles. Each links to its canonical copy and names where it lives and any copy. The sidebar keeps listing this site's pages only; the research index lists the pieces too since ADR-0048.
parent: decision-log
order: 46
adr: 46
status: accepted
created: 2026-10-26
updated: 2026-10-27
labels: adr, decision, navigation, research, publishing
owner: Stefan Coetzee
reviewed: 2026-10-26
review_by: 2027-01-24
type: explanation
---
## Context

[ADR-0045](doc:eng/adr-0045-sidebar-groups-open-with-an-index) gave the Articles group an index page, and it listed two pieces: the two articles whose home is this site. The "Running the golem" series put most of its research writing on the Uncover Tech Talent blog with a full copy on Substack, and every one of those blog posts declares the Substack copy canonical (probed 2026-10-26). A reader of /research/articles/ saw two pieces of a body of about a dozen. On 2026-10-26 Stefan Coetzee asked for the research-facing pieces from Substack and the blog to be listed there, each with where it lives; a mockup was rendered first.

## Decision

**An `elsewhere` list on the index's entry.** The Articles entry in `site/nav.yml` carries `elsewhere:`, one item per piece: its title, `url` (the canonical copy), `also` (another copy, optional), `published` (the piece's first publication, on whichever copy came first, so a blog-first piece keeps the blog's date) and `about` (one line, the piece's own description). `scripts/build_hubs.py` merges them by date with the index's own pages, newest first, this site's pages first on the same day. Each outside entry carries an arrow after its title and a meta line that names where it lives ("on Substack, also on the Uncover Tech Talent blog"), and a line above the list says what the arrow means. Links are not copied in and no canonical changes. Since [ADR-0048](doc:eng/adr-0048-research-index-and-group-indexes-as-contents-lists) the `about` line is not shown: each piece is one line, the date at the end and the site in a note under the title, and the research index lists the pieces as well.

**Checked by the build.** `scripts/site_chrome.py` stops the build when an `elsewhere` item lacks a title, a line or a date in YYYY-MM-DD form, or when a URL is not https on a host in `ELSEWHERE_HOMES`, which also names each host on the page (Substack, the Uncover Tech Talent blog). Only a hub page with `order: newest` may hold the list, so the merge has an order to keep.

**Only the index lists them.** The sidebar keeps its five newest pages of this site, and the research index lists this site's pages, so neither depends on another site staying up. Replaced in part by [ADR-0048](doc:eng/adr-0048-research-index-and-group-indexes-as-contents-lists): the research index lists the pieces as well, as one line each; the sidebar still does not.

**Which pieces.** The research-facing pieces of the series and the earlier Substack case study: Knowledge Infrastructure for LLMs, The Stance Layer Is Still Toil, An RCA on Claudish, Which LLM User Are We Talking About?, Compaction Is the New OOM, What Operations Already Knows About Running Agents, Write for the Codec, The Golem Made of English and the Horizon of Consequences, The Trap File Is Longer Than the Instruction File, and Sycophancy Is Layered. Left out: Success Is the Engine Running and The Track, written for buyers, and the Substack copies of pages that live here.

This extends ADR-0045, whose index pages list only the pages they hold; the rest of ADR-0045 stands.

## Consequences

/research/articles/ shows the programme's research writing in one list, with the two pieces that live here among them by date. A new research piece published on Substack gets an `elsewhere` item, or a page of its own under the index when this site is its home. A piece that moves or disappears on Substack leaves a dead link here until its item changes; the map crawl does not check outside links. A new outside host needs its entry in `ELSEWHERE_HOMES`.
