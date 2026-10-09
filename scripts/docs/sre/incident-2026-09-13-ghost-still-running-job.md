title: Incident 2026-09-13 Ghost Still-Running Job
summary: A process check over SSH reported the batch job as still running after it had exited.
parent: incidents
order: 100
labels: incident, transcriber-incidents
type: incident
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Incident 2026-09-13 Ghost Still-Running Job.md
reviewed: no
---
A process check over SSH reported the batch job as still running after it had exited.

## Caused by

- [[Process Check Matches Its Own Shell]]

## Mitigated by

- [[Bracket Pattern Process Check]]

## Part of

- [[Transcriber Incident Register]]
