title: Toil vs Engineering and the 50 Percent Rule
summary: SRE without a toil cap drifts into operations.
parent: toil-reduction
order: 100
labels: automation, practice, toil
aliases: Toil | 50 Percent Rule | Toil Budget | SRE Toil Cap
type: practice
created: 2026-05-04
updated: 2026-05-04
origin: SRE/pillars/10-toil-reduction/Toil vs Engineering and the 50 Percent Rule.md
reviewed: no
---
# Toil vs Engineering — The 50 Percent Rule

> SRE without a toil cap drifts into operations. Operations without an automation mandate stays operations. The 50% rule — no SRE spends more than half their time on toil — is what makes SRE a different role from senior ops. The rule is a forcing function, not a target.

## What counts as toil

Google SRE's working definition: work that is **manual, repetitive, automatable, tactical, devoid of enduring value, and scales linearly with service growth**. All six properties together. Specifically:

- Manual: requires a human, even briefly
- Repetitive: looks the same as the last 5 times
- Automatable: a machine could do it
- Tactical: reactive, not proactive
- No enduring value: when it's done, the system is in the same state, not a better one
- Scales linearly: 2x users → 2x of this work

Examples that almost always score 6/6: clicking through a runbook, re-running a flaky job, manually rotating a credential, pasting log lines into a ticket, restarting a service whose memory leaks.

## What is *not* toil (even when it feels tedious)

- **Engineering work that has enduring value.** Writing a runbook is not toil even though it is sometimes tedious — it removes future toil.
- **Investigation during an active incident.** Reactive but not repetitive in the same shape; each incident is different.
- **Code review.** Manual but enduring.
- **Postmortem authoring.** Tactical-feeling but produces enduring system understanding.

This distinction matters because the temptation is to label all unpleasant work as toil. The discipline is sharper: toil is *specifically* the work that, if you shipped automation, you would never do again.

## Why 50%

Below 50%, SRE has bandwidth for projects that eliminate the toil itself. Above 50%, the team becomes reactive, automation projects starve, the toil compounds, the team exits SRE in everything but title.

The number is not magical. The function is: **leave enough engineering time that automation gets built faster than new toil gets discovered**. If new toil > automation throughput, the team is losing ground. The 50% cap catches that early.

## Measuring toil honestly

Subjective self-report works if the team is small and has a culture of candor. As soon as it's used for performance review, the numbers stop being honest. Better:

- Ticket-based time tracking, with a tag for toil vs. project
- Quarterly toil retrospective: list every recurring task, score it, identify the top 3 by total team-hours, fund automation for those next quarter
- Post-incident audit: every action item answers "could a script have done this?" If yes, that's toil to schedule out

The output is a ranked list. The top 3 each quarter become engineering projects. The bottom 90% stays toil until it bubbles up.

## The hard part: cultural

SRE teams that hit 80% toil are not under-staffed. They are usually under-protected — nobody is saying "no, we will not do that ad-hoc request, it goes into the queue with a real priority." The 50% cap requires:

- Manager air cover to push back on dropping engineering work for one-off requests
- A backlog that converts toil into projects with explicit ROI
- A culture that treats "we don't do that work manually anymore" as the default answer

Without those, the rule becomes a slide in a quarterly deck.

## Anti-patterns

- **Counting reactive work as engineering.** Investigating an incident is not building automation.
- **Hero patterns.** The one engineer who handles all the manual work "because it's faster" is the team's biggest toil sink and biggest single point of failure.
- **Automation that creates toil.** A script that requires manual intervention every time it runs is not automation. It's manual work with a wrapper.
- **Exempting "important" toil.** "We have to do this manually because it's critical." If it's critical and manual, it's the highest-priority automation target.

## See also

[[Service Outage Response]] · [[Idempotence as the IaC Invariant]] · [[Blameless Postmortem Discipline]] · [[01-reliability]] · [[09-cost-optimization]]
