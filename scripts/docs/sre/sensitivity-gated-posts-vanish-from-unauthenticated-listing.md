title: Sensitivity-Gated Posts Vanish From Unauthenticated Listing
summary: TikTok refuses to serve age-restricted or sensitivity-flagged posts to an unauthenticated client.
parent: incidents
order: 100
labels: root-cause, transcriber-incidents
type: root-cause
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Sensitivity-Gated Posts Vanish From Unauthenticated Listing.md
reviewed: no
---
TikTok refuses to serve age-restricted or sensitivity-flagged posts to an unauthenticated client. In `--flat-playlist` enumeration they drop out of the list with no error at the collection level. Gating can be applied after a video was first fetched. The loss is biased by topic, since health-adjacent content is the class that gets flagged.

## Part of

- [[Transcriber Incident Register]]
