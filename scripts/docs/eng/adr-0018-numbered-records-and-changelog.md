title: ADR-0018: Numbered decision records and a generated changelog
summary: Each decision is a numbered record (ADR-0001 onward) with a status (proposed, accepted, superseded), context, decision and consequences, one docs page each.
parent: decision-log
order: 18
adr: 18
status: accepted
created: 2026-10-09
labels: adr, decision
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

The decision log had the shape of architecture decision records, but an entry could not be cited by number or superseded cleanly, and there was no changelog.

## Decision

Each decision is a numbered record (ADR-0001 onward) with a status (proposed, accepted, superseded), context, decision and consequences, one docs page each. A superseded record stays and links its successor; the build checks that both sides of a link agree. Three earlier choices replaced by later records were added after the fact from their commits. The [changelog](doc:eng/changelog) is generated from closed issues and commits, grouped Added, Changed and Fixed.

## Consequences

A new decision is a new file with the next number. The changelog needs a network call to GitHub when it is rebuilt. See [Decision records](doc:eng/decision-log).
