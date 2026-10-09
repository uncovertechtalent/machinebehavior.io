title: Enumeration Retry With Unauthenticated Fallback
summary: Enumeration tries the cookie jar twice, then unauthenticated mode three times with backoff, and logs which path succeeded.
parent: incidents
order: 100
labels: mitigation, transcriber-incidents
type: mitigation
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Enumeration Retry With Unauthenticated Fallback.md
reviewed: no
---
Enumeration tries the cookie jar twice, then unauthenticated mode three times with backoff, and logs which path succeeded. Gated videos are lost on the fallback path, and the log says so. Since 2026-09-16 this retry also carries runs where the first attempt returns an empty body for an unknown reason.

## Part of

- [[Transcriber Incident Register]]
