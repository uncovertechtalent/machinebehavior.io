title: File Copy of a WAL-Mode Database Misses Recent Writes
summary: A SQLite database in WAL mode keeps recent writes in the -wal file.
parent: incidents
order: 100
labels: root-cause, transcriber-incidents
type: root-cause
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/File Copy of a WAL-Mode Database Misses Recent Writes.md
reviewed: no
---
A SQLite database in WAL mode keeps recent writes in the `-wal` file. Copying only the main `.db` file produces a backup that silently lacks them.

## Part of

- [[Transcriber Incident Register]]
