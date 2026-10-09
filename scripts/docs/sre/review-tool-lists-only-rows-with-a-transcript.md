title: Review Tool Lists Only Rows With a Transcript
summary: reviewstatus.py reports on rows where length(transcript) > 0.
parent: incidents
order: 100
labels: root-cause, transcriber-incidents
type: root-cause
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Review Tool Lists Only Rows With a Transcript.md
reviewed: no
---
`review_status.py` reports on rows where `length(transcript) > 0`. A video made of on-screen text has no speech, Whisper returns nothing, and `status` still flips to complete. The row is neither backlog nor reviewable, so it is invisible from both directions.

## Part of

- [[Transcriber Incident Register]]
