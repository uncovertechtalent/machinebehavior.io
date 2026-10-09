title: ADR-0001: Root-absolute links only
summary: Internal links are root-absolute directory URLs (`/man/`, `/style.css`), never relative and never ending in `.html`.
parent: decision-log
order: 1
adr: 1
status: accepted
created: 2026-10-07
labels: adr, decision
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

Pages moved between hosts, previews and directory URLs, and relative links broke when a page moved one level. Some links ended in `.html`, so one page answered at two URLs.

## Decision

Internal links are root-absolute directory URLs (`/man/`, `/style.css`), never relative and never ending in `.html`. Generators and hand-written pages follow the same rule, and the gate enforces it.

## Consequences

Every URL has one form and survives a move. A link written inside a JavaScript template string reads as relative to the check, so scripts build links with `a.href` in code. See [Link check flags a template string](doc:eng/runbook-template-href).
