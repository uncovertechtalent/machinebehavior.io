title: Handle-Based Ad Filter Matches Artist Accounts
summary: The creator rule \.(de|official)$ was written for brand and shop accounts.
parent: incidents
order: 100
labels: root-cause, transcriber-incidents
type: root-cause
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Handle-Based Ad Filter Matches Artist Accounts.md
reviewed: no
---
The creator rule `\.(de|official)$` was written for brand and shop accounts. Hardstyle and uptempo artists routinely use `.official` handles. Rejected videos stay at `status=pending` with an empty transcript and look identical to unprocessed backlog. When nothing is removed, no log line is written at all.

## Part of

- [[Transcriber Incident Register]]
