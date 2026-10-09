title: Re-Scrape Relinks Processed Rows As Pending
summary: Re-scraping a collection re-links videos that were already processed and sets them back to statuspending without flipping them to complete again.
parent: incidents
order: 100
labels: root-cause, transcriber-incidents
type: root-cause
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Re-Scrape Relinks Processed Rows As Pending.md
reviewed: no
---
Re-scraping a collection re-links videos that were already processed and sets them back to `status=pending` without flipping them to complete again. The row keeps its transcript and summary while its status says otherwise.

## Part of

- [[Transcriber Incident Register]]
