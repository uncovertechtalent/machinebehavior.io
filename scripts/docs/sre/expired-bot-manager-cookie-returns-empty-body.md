title: Expired Bot-Manager Cookie Returns Empty Body
summary: yt-dlp sends expired entries from a Netscape cookie jar as they are.
parent: incidents
order: 100
labels: root-cause, transcriber-incidents
type: root-cause
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Expired Bot-Manager Cookie Returns Empty Body.md
reviewed: no
---
yt-dlp sends expired entries from a Netscape cookie jar as they are. Akamai answers a stale bot-manager cookie (`ak_bmsc`, `bm_sv`) with an empty body, which yt-dlp reports as a JSON parse error at character 0. The session cookies can be valid for months while these two expire within days.

## Part of

- [[Transcriber Incident Register]]
