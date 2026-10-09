title: Incident 2026-07-19 Pending Status on Finished Videos
summary: Twelve videos sat at statuspending while holding full transcripts and summaries.
parent: incidents
order: 100
labels: incident, transcriber-incidents
type: incident
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Incident 2026-07-19 Pending Status on Finished Videos.md
reviewed: no
---
Twelve videos sat at `status=pending` while holding full transcripts and summaries. Same class of error as trusting an agent's completion message.

## Caused by

- [[Re-Scrape Relinks Processed Rows As Pending]]

## Mitigated by

- [[Verify Transcript Length Never Status]]

## Part of

- [[Transcriber Incident Register]]
