title: Single Video URL As the Collection Argument
summary: A single video URL works as the --collection-url argument, so individual videos can be reprocessed without a working collection link.
parent: incidents
order: 100
labels: mitigation, transcriber-incidents
type: mitigation
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Single Video URL As the Collection Argument.md
reviewed: no
---
A single video URL works as the `--collection-url` argument, so individual videos can be reprocessed without a working collection link. The cost is one junk row in `collections` per video.

## Part of

- [[Transcriber Incident Register]]
