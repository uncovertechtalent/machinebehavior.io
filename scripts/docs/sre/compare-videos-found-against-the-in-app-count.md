title: Compare Videos Found Against the In-App Count
summary: The owner's in-app count minus videosfound measures the gap.
parent: incidents
order: 100
labels: mitigation, transcriber-incidents
type: mitigation
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Compare Videos Found Against the In-App Count.md
reviewed: no
---
The owner's in-app count minus `videos_found` measures the gap. Read it as the number of gated posts saved in that cycle. With the cron unattended, this is the only check between a silent enumeration failure and weeks of nothing.

## Part of

- [[Transcriber Incident Register]]
