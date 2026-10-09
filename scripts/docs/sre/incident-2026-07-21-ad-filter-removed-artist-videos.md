title: Incident 2026-07-21 Ad Filter Removed Artist Videos
summary: Ten videos from artists with .official handles were rejected by the ad filter before transcription and looked like unprocessed backlog.
parent: incidents
order: 100
labels: incident, transcriber-incidents
type: incident
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Incident 2026-07-21 Ad Filter Removed Artist Videos.md
reviewed: no
---
Ten videos from artists with `.official` handles were rejected by the ad filter before transcription and looked like unprocessed backlog.

## Caused by

- [[Handle-Based Ad Filter Matches Artist Accounts]]

## Mitigated by

- [[Probe Pending Rows Before Calling Them Backlog]]

## Part of

- [[Transcriber Incident Register]]
