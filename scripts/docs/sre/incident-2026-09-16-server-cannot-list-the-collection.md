title: Incident 2026-09-16 Server Cannot List the Collection
summary: From 2026-09-16 the server could not enumerate the collection from any client or egress, while the laptop could with the same yt-dlp version through the same egress.
parent: incidents
order: 100
labels: incident, transcriber-incidents
type: incident
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Incident 2026-09-16 Server Cannot List the Collection.md
reviewed: no
---
From 2026-09-16 the server could not enumerate the collection from any client or egress, while the laptop could with the same yt-dlp version through the same egress. IP, yt-dlp version and impersonation were ruled out. By 2026-09-21 listing worked again with no change made: the first cookie attempt still fails with an empty body and the second succeeds. No cause node exists for this incident because none is known.

## Mitigated by

- [[Enumeration Retry With Unauthenticated Fallback]]

## Detected by

- [[Differential Test in the Same Minutes]]

## Part of

- [[Transcriber Incident Register]]
