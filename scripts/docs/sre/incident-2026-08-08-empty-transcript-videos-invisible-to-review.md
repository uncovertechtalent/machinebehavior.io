title: Incident 2026-08-08 Empty-Transcript Videos Invisible to Review
summary: A reel made of on-screen text returned no transcript.
parent: incidents
order: 100
labels: incident, transcriber-incidents
type: incident
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Incident 2026-08-08 Empty-Transcript Videos Invisible to Review.md
reviewed: no
---
A reel made of on-screen text returned no transcript. It was reviewed only because the owner named it directly. Probed totals: 104 rows with a NULL review and an empty transcript.

## Caused by

- [[Review Tool Lists Only Rows With a Transcript]]

## Mitigated by

- [[Pull the Full Row List After Any Scrape]]
- [[No-Transcript Bucket in the Review Tool]]

## Part of

- [[Transcriber Incident Register]]
