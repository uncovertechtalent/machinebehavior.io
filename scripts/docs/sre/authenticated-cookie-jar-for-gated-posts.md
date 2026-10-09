title: Authenticated Cookie Jar for Gated Posts
summary: An exported cookies.txt lets yt-dlp list and fetch gated posts.
parent: incidents
order: 100
labels: mitigation, transcriber-incidents
type: mitigation
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Authenticated Cookie Jar for Gated Posts.md
reviewed: no
---
An exported `cookies.txt` lets yt-dlp list and fetch gated posts. It puts an authenticated session on the server, which was the owner's decision to make. It is the fix for the cause; the count checks only measure the gap.

## Part of

- [[Transcriber Incident Register]]
