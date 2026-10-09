title: Incident 2026-07-14 Short Scrape Looked Like a Quiet Feed
summary: Six runs in a row reported 19 videos found; a later run reported 32, and the owner's own count was closer than the database's.
parent: incidents
order: 100
labels: incident, transcriber-incidents
type: incident
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Incident 2026-07-14 Short Scrape Looked Like a Quiet Feed.md
reviewed: no
---
Six runs in a row reported 19 videos found; a later run reported 32, and the owner's own count was closer than the database's. A short scrape is indistinguishable from a quiet feed. The first fix was wrong and its correction is kept next to it. The earlier belief that the queue decays and videos were lost was overturned: nothing was lost, the missing videos were gated.

## Caused by

- [[Sensitivity-Gated Posts Vanish From Unauthenticated Listing]]

## Mitigated by

- [[Compare Videos Found Run to Run]]
- [[Compare Videos Found Against the In-App Count]]
- [[Authenticated Cookie Jar for Gated Posts]]

## Detected by

- [[Probe the Artifact Before Reasoning From Counts]]

## Part of

- [[Transcriber Incident Register]]
