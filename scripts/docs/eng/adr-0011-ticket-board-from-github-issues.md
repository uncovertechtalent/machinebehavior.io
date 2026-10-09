title: ADR-0011: A public ticket board from GitHub Issues
summary: Work items are GitHub Issues on the public repository, shown on [the board](/inside/board/).
parent: decision-log
order: 11
adr: 11
status: accepted
created: 2026-10-09
labels: adr, decision
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

The backlog from the platform review needed one public system of record that agent sessions and readers can both use.

## Decision

Work items are GitHub Issues on the public repository, shown on [the board](/inside/board/). The deploy job writes `inside/board/issues.json` (`scripts/board_snapshot.py`), and the workflow gains `issues: read` but no `issues` trigger.

## Consequences

The board is as fresh as the last deploy. Only issues with a type label are shown, so a new report waits for triage before its text appears. An `issues` trigger would let anyone start a gate run and a deploy. See [Ticket board](doc:eng/board).
