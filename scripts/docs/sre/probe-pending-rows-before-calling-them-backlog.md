title: Probe Pending Rows Before Calling Them Backlog
summary: A pending count is unclassified until the rows are looked at.
parent: incidents
order: 100
labels: mitigation, transcriber-incidents
type: mitigation
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Probe Pending Rows Before Calling Them Backlog.md
reviewed: no
---
A pending count is unclassified until the rows are looked at. Of 52 pending on 2026-07-21, 12 were ad-filter rejects and 39 were off-topic. The absence of the `Ad filter: removed` log line is the all-clear. Tightening the regex is tracked as bead vault-lv0.

## Part of

- [[Transcriber Incident Register]]
