title: ADR-0012: One top bar and one search index for Inside
summary: Every Inside page carries one top bar, written by `bar()` in `scripts/inside_chrome.py`.
parent: decision-log
order: 12
adr: 12
status: accepted
created: 2026-10-09
supersedes: adr-0007-docs-search-own-index
labels: adr, decision
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

There were three navigations (the site menu, the Inside header, the docs bar) and two search boxes over two indexes, and docs search opened the first hit on Enter.

## Decision

Every Inside page carries one top bar, written by `bar()` in `scripts/inside_chrome.py`. One index, `/inside/search.json`, merges the docs, the services and the map. The search box is a form that submits to `/inside/search/`, so Enter opens a results page. The deploy job rebuilds the index after the map refresh.

## Consequences

A new Inside page must carry the marked bar block; `python3 scripts/inside_chrome.py --check` reports drift. The index is about 200 KB and loads when the box gets focus. See [Top bar and search](doc:eng/top-bar-and-search).
