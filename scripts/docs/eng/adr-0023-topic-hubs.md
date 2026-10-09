title: ADR-0023: Topic hubs across research, docs, posts and tickets
summary: Seven topic hubs at /topics/<key>/ list every research page, Inside page, docs page, post and board issue on one subject; site/topics.yml holds the rules, and a Topics block in each sidebar marks the topics of the current page.
parent: decision-log
order: 23
adr: 23
status: accepted
created: 2026-10-09
labels: adr, decision, navigation, topics
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

The site is cut by kind: research pages, Inside, six docs spaces, posts on uncovertechtalent.com and Substack, and the board. A reader who comes for one subject, for example observability or the stance layer, has to visit each part. The labels already exist in three places: docs front matter (294 labels), the tag pages of uncovertechtalent.com on the map, and the area labels on the board. The hand-written pages have none.

## Decision

`site/topics.yml` defines seven topics (sycophancy and stance, conformity and law, operations and SRE, observability, FinOps, agents and harness, evaluation). Each topic names the rules that select its members: a list of hand-written and Inside pages (the tag map for pages without front matter), docs labels and whole docs spaces, tag pages on the map, words in Substack titles, and board labels or words in issue titles. `scripts/build_hubs.py` builds one hub per topic at `/topics/<key>/` and an index at `/topics/`, in the reading layout: research and Inside pages as cards, docs grouped by space with long spaces folded, posts listed once with the Substack copy linked beside the original, and tickets open first. The membership goes to `/topics/topics.json`. Topics is a section in `site/nav.yml` and in the top bar; every sidebar ends with a Topics block that marks the topics listing the current page, and the docs sidebar holds the block as a managed marker. The crawler treats the hubs as their own node kind, so they appear on the map in their own colour.

Board issues come from the GitHub API at build time. When the API cannot be read, the last list in `topics.json` stays, so a build without network does not empty the tickets.

## Consequences

A topic reads the labels that exist and adds none of its own: adding a docs label or a map tag that a topic names puts the page on its hub at the next build. Word rules can pick up a wrong title; each hub lists its sources, and a wrong match is fixed in `site/topics.yml`. The ticket lists date from the last build of the hubs; a deploy alone does not refresh them. Two hubs (conformity and law, operations and SRE) list whole vault spaces of about 200 and 100 pages; they show ten per space and fold the rest.
