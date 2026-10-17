title: Someone carries the pager
summary: The test for SRE work is standby, a person who is told when production breaks and acts. Here a PagerDuty-style pager on Discord holds the rotation (the operator in waking hours, an agent responder at all hours) and the escalation policy, an outside heartbeat watches the alerting path, and the rotation, the last pages and the pager load are public.
parent: principles-in-practice
order: 30
labels: principle, sre, on-call, alerting, standby, pager, rotation
owner: Stefan Coetzee
reviewed: 2026-10-17
review_by: 2027-01-15
type: explanation
state: gap
source: [Manifesto](doc:sre/manifesto), the standby differentiator; [Google SRE book ch. 11](https://sre.google/sre-book/being-on-call/)
---
## The principle

If one test decides whether someone does SRE work, it is standby. SRE carries the pager and is the first rotation for production outages; platform and ops teams stand behind it on their own rotations. A team with the title and no standby is a platform team. Google's book adds the limits that keep standby sustainable: a cap on incidents per shift, time to follow up each one, and most of an SRE's time kept for engineering.

Source: the standby section of the [manifesto](doc:sre/manifesto); Google's [Being On-Call](https://sre.google/sre-book/being-on-call/).

## On this platform

- **A pager with a rotation.** One Alertmanager routes the rules of both Prometheus servers. A page goes to a PagerDuty-style pager on a private Discord server: an incident with Acknowledge, Resolve and Escalate buttons, the operator on call from 08:00 to 22:00 Berlin time, a mention again every 5 minutes, and at 15 minutes an agent responder that posts the runbook link and a read-only diagnosis. Out of hours the responder takes the page at once and the operator hears at 08:00. Every page and ticket is also an issue on the [board](/inside/board/) ([On-call and escalation](doc:obs/on-call), [Alerts and SLOs](doc:obs/alerts-and-slos)).
- **The alerting path is watched from outside.** Each Prometheus carries an always-firing Watchdog that pings a heartbeat check outside the house every 5 minutes; the check alarms when the pings stop. A down pager goes past itself, by webhook.
- **A second path for cost.** The AWS monthly budget in AWS Budgets sends an e-mail at 80% of actual spend. It sits outside the stack ([Budgets and alerts](doc:fin/budgets-and-alerts)).
- **One control acts at any hour.** The [conformity gate](/inside/services/conformity-gate/) stops a failing deploy and keeps the previous build live without anyone on call. On 2026-10-08 it blocked a deploy, and the run on the fix started 76 seconds later and passed ([incident record](/inside/status/#2026-10-08-gate-blocked-map-push)).
- **How incidents were found.** Of the four records on the [status page](/inside/status/) before alert routing, the gate found one, the blocked deploy. Someone who was working at the time found the other three, and none of those three records the time of the first report or check.

## On call now

The rotation, the escalation policy, the last pages with their time to acknowledge and to resolve, and the pager load per week, from the public snapshot that the [on-call page](doc:obs/on-call) also shows:

<!-- oncall-snapshot -->

## State

**Gap.** The pager, the rotation and the escalation policy run on the home server, and the routing is tested offline, but no test page has yet gone through the whole chain to a person: Discord message, acknowledgement, escalation without one, resolve ([#36](https://github.com/uncovertechtalent/machinebehavior.io/issues/36)). The state moves when one has. Even then, standby in the full sense stays thin: one person, one human layer, and nobody woken at night by design. The gate still covers the largest tier-1 risk, a bad page in front of readers, without a person.

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
