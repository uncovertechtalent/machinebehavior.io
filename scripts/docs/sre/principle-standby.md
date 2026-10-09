title: Someone carries the pager
summary: The test for SRE work is standby, a person who is told when production breaks and acts. Here 17 alert rules reach nobody, the gate is the one control that acts at any hour, and three of four incidents were found by someone working at the time.
parent: principles-in-practice
order: 30
labels: principle, sre, on-call, alerting, standby
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
state: gap
source: [Manifesto](doc:sre/manifesto), the standby differentiator; [Google SRE book ch. 11](https://sre.google/sre-book/being-on-call/)
---
## The principle

If one test decides whether someone does SRE work, it is standby. SRE carries the pager and is the first rotation for production outages; platform and ops teams stand behind it on their own rotations. A team with the title and no standby is a platform team. Google's book adds the limits that keep standby sustainable: a cap on incidents per shift, time to follow up each one, and most of an SRE's time kept for engineering.

Source: the standby section of the [manifesto](doc:sre/manifesto); Google's [Being On-Call](https://sre.google/sre-book/being-on-call/).

## On this platform

- **Rules exist, delivery does not.** Prometheus evaluates 17 alert rules: 5 with severity page, 11 ticket and 1 info ([Alerts and SLOs](doc:obs/alerts-and-slos)). The stack runs no Alertmanager, so a firing alert stays in Prometheus and Grafana until someone looks ([On-call and escalation](doc:obs/on-call)).
- **One path reaches a person.** The AWS monthly budget in AWS Budgets sends an e-mail at 80% of actual spend. It sits outside the stack ([Budgets and alerts](doc:fin/budgets-and-alerts)).
- **One control acts at any hour.** The [conformity gate](/inside/services/conformity-gate/) stops a failing deploy and keeps the previous build live without anyone on call. On 2026-10-08 it blocked a deploy, and the fix passed 81 seconds later ([incident record](/inside/status/#2026-10-08-gate-blocked-map-push)).
- **How incidents were found.** Of the four records on the [status page](/inside/status/), the gate found one, the blocked deploy. Someone who was working at the time found the other three, and none of those three records the time of the first report or check.
- **A routing proposal.** The [on-call page](doc:obs/on-call) holds a routing: pages to the operator's phone in waking hours, tickets onto the [board](/inside/board/), an always-firing Watchdog with an outside heartbeat, and inhibition so one cause raises one alert.

## State

**Gap.** Nobody is on standby and no alert rule reaches anyone. The gate covers the largest tier-1 risk, a bad page in front of readers, without a person. Every other failure stays unseen until someone looks: a down search instance, a model server that stopped, a spend spike at night. The proposal is wired once the operator chooses the receivers ([#36](https://github.com/uncovertechtalent/machinebehavior.io/issues/36)).

## Services that name it

<!-- principle-services -->

## In a company of 10 to 200 people

- Start with one rotation for the services customers meet. Each person should be on call at most one week in four; with fewer people, share one rotation across teams.
- Page only on symptoms users feel, with a runbook link in every page. Everything else becomes a ticket with an owner.
- Pay for standby or give the time back, and review the pager load every month.
- Add a dead man's switch: an always-firing alert that an outside check expects, so a broken alert path raises an alarm too.

## Open work

- [#36 Alert routing: Alertmanager, a Watchdog and receivers chosen by the operator](https://github.com/uncovertechtalent/machinebehavior.io/issues/36)
- [#41 Incident records: when and how each incident was detected](https://github.com/uncovertechtalent/machinebehavior.io/issues/41)
