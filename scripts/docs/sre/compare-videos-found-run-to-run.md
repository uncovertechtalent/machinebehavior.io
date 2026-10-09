title: Compare Videos Found Run to Run
summary: First fix for the short scrape: treat any drop in videosfound between runs as suspect.
parent: incidents
order: 100
labels: mitigation, transcriber-incidents
type: mitigation
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Compare Videos Found Run to Run.md
reviewed: no
---
First fix for the short scrape: treat any drop in `videos_found` between runs as suspect. Proven insufficient two days later, when the count rose from 32 to 37 while the app showed 47. A rising number proves nothing.

## Superseded by

- [[Compare Videos Found Against the In-App Count]]

## Part of

- [[Transcriber Incident Register]]
