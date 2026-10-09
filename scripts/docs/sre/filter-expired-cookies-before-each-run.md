title: Filter Expired Cookies Before Each Run
summary: cookieargs() writes a filtered copy of the cookie jar with expired entries dropped, logs each drop, and passes the filtered file to yt-dlp.
parent: incidents
order: 100
labels: mitigation, transcriber-incidents
type: mitigation
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Filter Expired Cookies Before Each Run.md
reviewed: no
---
`_cookie_args()` writes a filtered copy of the cookie jar with expired entries dropped, logs each drop, and passes the filtered file to yt-dlp. Every logged drop is a crash that did not happen. Applied 2026-09-13.

## Part of

- [[Transcriber Incident Register]]
