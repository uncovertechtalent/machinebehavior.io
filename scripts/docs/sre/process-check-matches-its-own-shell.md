title: Process Check Matches Its Own Shell
summary: pgrep -f <pattern> run over SSH matches the remote shell whose command line contains the pattern.
parent: incidents
order: 100
labels: root-cause, transcriber-incidents
type: root-cause
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Process Check Matches Its Own Shell.md
reviewed: no
---
`pgrep -f <pattern>` run over SSH matches the remote shell whose command line contains the pattern. The check reports the job as running when it has finished.

## Part of

- [[Transcriber Incident Register]]
