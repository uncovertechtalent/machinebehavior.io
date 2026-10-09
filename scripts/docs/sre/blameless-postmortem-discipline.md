title: Blameless Postmortem Discipline
summary: A blameless postmortem assumes the engineer behaved rationally given the information they had.
parent: incident-management
order: 100
labels: incident-management, postmortem, practice
aliases: Postmortem | Blameless Postmortem | Incident Review
type: practice
created: 2026-05-04
updated: 2026-05-04
origin: SRE/pillars/04-incident-management/Blameless Postmortem Discipline.md
reviewed: no
---
> A blameless postmortem assumes the engineer behaved rationally given the information they had. The investigation is about what *system* gave them that information — tooling, signals, processes, training. If your postmortem ends in "be more careful" or names a person, it failed.

## What blameless actually means

It does not mean "no consequences." It means **the consequence cannot be punishing the individual for an error that the system enabled**. The discipline rests on a single belief: people doing the work are usually trying to do the right thing. If they did the wrong thing, the system created the conditions for that to be the locally-rational choice.

Switch the lens from *who* to *what*:

- A junior engineer ran a destructive migration on prod. → What allowed prod credentials to land in a script run from a laptop? What signal would have warned them? Why did review not catch it?
- An on-call missed a page for 40 minutes. → What was the page-acknowledgement timeout? Was the alert tier correct? Was secondary on-call automatically engaged?

The named-person framing produces theatre. The system framing produces fixes.

## The artifact has a fixed shape

Every postmortem contains:

1. **Summary.** One paragraph. What happened, customer impact, duration.
2. **Timeline.** Detection, declaration, mitigation, resolution. Wall-clock times.
3. **Impact.** Users affected, requests failed, revenue/SLO budget consumed.
4. **Root cause.** Mechanism, not person. Often a chain of contributing factors.
5. **What went well.** Detection, mitigation, communication that worked.
6. **What went poorly.** Specifically, mechanically. No adjectives.
7. **Action items.** Each has an owner (named person), a due date, and a tracking link. No "we should consider..."

A postmortem without owned action items is a story, not a postmortem.

## The 5-business-day rule

The postmortem doc opens when the incident closes. The first draft is due within 5 business days. Memory decays fast — facts that everyone "obviously" remembers in week one become contested in week three. The ICs and SMEs who were in the channel are the right authors; do not delegate to someone who was not on the bridge.

## What kills the discipline

- **Postmortems used in performance reviews.** Once. Then nobody admits anything in the next one.
- **Skipping postmortems for "small" incidents.** Small ones are where the systemic patterns live. The big ones are usually the small ones, repeated.
- **Action items without owners.** Or with the owner being "the team."
- **Action items that never close.** A postmortem with three open action items 90 days later is a signal the discipline has broken.
- **Sanitizing the document for executive consumption.** Two documents diverge; neither is honest.

## The forcing function

Read postmortems weekly across the org. Patterns reveal themselves. If three incidents in a quarter all touched the same fragile config system, the system is the next project — not the engineers who tripped on it.

## See also

[[Service Outage Response]] · [[01-reliability]] · [[10-toil-reduction]] · [[README]]
