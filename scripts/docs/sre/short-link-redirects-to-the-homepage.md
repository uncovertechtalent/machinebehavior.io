title: Short Link Redirects to the Homepage
summary: Stored vm.tiktok.com short links for two collections now redirect to the site homepage.
parent: incidents
order: 100
labels: root-cause, transcriber-incidents
type: root-cause
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Short Link Redirects to the Homepage.md
reviewed: no
---
Stored `vm.tiktok.com` short links for two collections now redirect to the site homepage. yt-dlp exits with `Unsupported URL` and the batch script dies at enumeration. Fresh canonical URLs can only be copied out of the app by the account owner.

## Part of

- [[Transcriber Incident Register]]
