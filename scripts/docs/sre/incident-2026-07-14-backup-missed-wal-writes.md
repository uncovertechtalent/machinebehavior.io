title: Incident 2026-07-14 Backup Missed WAL Writes
summary: A pre-change backup copied the main database file only, while the database was in WAL mode with a multi-megabyte WAL file.
parent: incidents
order: 100
labels: incident, transcriber-incidents
type: incident
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Incident 2026-07-14 Backup Missed WAL Writes.md
reviewed: no
---
A pre-change backup copied the main database file only, while the database was in WAL mode with a multi-megabyte WAL file.

## Caused by

- [[File Copy of a WAL-Mode Database Misses Recent Writes]]

## Mitigated by

- [[Back Up SQLite With the Backup Command]]

## Part of

- [[Transcriber Incident Register]]
