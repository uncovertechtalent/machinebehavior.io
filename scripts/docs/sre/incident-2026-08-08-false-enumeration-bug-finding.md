title: Incident 2026-08-08 False Enumeration Bug Finding
summary: A scrape found 46 videos and a re-enumeration minutes later found 48.
parent: incidents
order: 100
labels: false-finding, transcriber-incidents
type: false-finding
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Incident 2026-08-08 False Enumeration Bug Finding.md
reviewed: no
---
A scrape found 46 videos and a re-enumeration minutes later found 48. One of the extra videos had a publish date ten weeks old, and the session concluded that enumeration was non-deterministic. The owner had been saving videos to the collection while the scrape ran. The rule that would have prevented the error was already written in the same file.

## Caused by

- [[Publish Date Treated As Time In Collection]]

## Mitigated by

- [[Eliminate Concurrent Saves Before Blaming the Scraper]]

## Part of

- [[Transcriber Incident Register]]
