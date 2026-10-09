title: Pull the Full Row List After Any Scrape
summary: Do not take the review tool's count as the batch size.
parent: incidents
order: 100
labels: mitigation, transcriber-incidents
type: mitigation
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Pull the Full Row List After Any Scrape.md
reviewed: no
---
Do not take the review tool's count as the batch size. After a scrape, list every row and check `length(transcript)` per row.

## Part of

- [[Transcriber Incident Register]]
