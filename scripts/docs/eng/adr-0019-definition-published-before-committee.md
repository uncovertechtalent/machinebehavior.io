title: ADR-0019: Publish the definition draft before the committee route
summary: The working draft "Continuous Conformity for Deployed AI Systems" (0.3, 36 requirements) is public as a reference at /continuous-conformity/ before any standards committee has seen it, reversing the committee-first order of 2026-10-04.
parent: decision-log
order: 19
adr: 19
status: accepted
created: 2026-10-09
labels: adr, decision, conformity, standards
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
## Context

The definition draft (terms, requirements with M/A/H marks, crosswalk to the AI Act, DORA, GDPR and NIST) was written for a standards committee. On 2026-10-04 the plan was committee first: comment on ISO/IEC DIS 23282 through the national body, seek a seat in the AI mirror committee, and publish the definition after the committee route had seen it. The draft was already in use on this site: the conformity gate runs its mechanical requirements and the self-assessment scores the author's setup against it, so the requirement texts were public in [/conformity/requirements.json](/conformity/requirements.json) without the document around them.

## Decision

Publish the draft now as a reference page, [/continuous-conformity/](/continuous-conformity/), labelled a working draft, not a standard, not a certification scheme, with version, date, limits and a way to comment by clause number. Stefan Coetzee, 2026-10-09: "add it now, i'd rather build it and have it out in public as reference". The committee route stays open: the DIS 23282 comments (deadline 2026-11-25) cite the public draft instead of waiting for it.

## Consequences

The document can be cited, linked from the gate, the self-assessment and the docs, and read by models through llms.txt. Comments arrive in public before any committee review, and the draft carries one author's view until outside raters or a committee change it. Changes are versioned on the page; the vault source stays the single source of truth and the page is rebuilt from it (`articles/continuous-conformity-definition/build.py` in the author's vault). See [Conformity gate](doc:eng/conformity-gate) and [Conformity self-assessment, run 1](doc:res/conformity-self-assessment).
