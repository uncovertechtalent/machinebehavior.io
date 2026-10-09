title: Back Up SQLite With the Backup Command
summary: Use sqlite3 .backup, or checkpoint the WAL first, to get a restore point that holds every write.
parent: incidents
order: 100
labels: mitigation, transcriber-incidents
type: mitigation
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Back Up SQLite With the Backup Command.md
reviewed: no
---
Use `sqlite3 .backup`, or checkpoint the WAL first, to get a restore point that holds every write.

## Part of

- [[Transcriber Incident Register]]
