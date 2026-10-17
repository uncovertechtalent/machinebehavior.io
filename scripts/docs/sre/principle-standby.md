title: Someone carries the pager
summary: The test for SRE work is standby, a person who is told when production breaks and acts. Here alerts reach the one operator, pages in Discord in waking hours and every page and ticket as an issue on the board, an outside heartbeat watches the alerting path, and nobody is woken at night.
parent: principles-in-practice
order: 30
labels: principle, sre, on-call, alerting, standby
owner: Stefan Coetzee
reviewed: 2026-10-17
review_by: 2027-01-15
type: explanation
state: partial
source: [Manifesto](doc:sre/manifesto), the standby differentiator; [Google SRE book ch. 11](https://sre.google/sre-book/being-on-call/)
---
## The principle

If one test decides whether someone does SRE work, it is standby. SRE carries the pager and is the first rotation for production outages; platform and ops teams stand behind it on their own rotations. A team with the title and no standby is a platform team. Google's book adds the limits that keep standby sustainable: a cap on incidents per shift, time to follow up each one, and most of an SRE's time kept for engineering.

Source: the standby section of the [manifesto](doc:sre/manifesto); Google's [Being On-Call](https://sre.google/sre-book/being-on-call/).

## On this platform

- **Alerts reach a person.** Since 2026-10-17 one Alertmanager routes the rules of both Prometheus servers: the 5 page rules to Discord between 08:00 and 22:00 Berlin time and onto the [board](/inside/board/) as issues at any hour, 12 ticket rules onto the board, and the info rule and the three AWS spend rules nowhere ([On-call and escalation](doc:obs/on-call), [Alerts and SLOs](doc:obs/alerts-and-slos)).
- **The alerting path is watched from outside.** Each Prometheus carries an always-firing Watchdog that pings a heartbeat check outside the house every 5 minutes; the check alarms when the pings stop.
- **A second path for cost.** The AWS monthly budget in AWS Budgets sends an e-mail at 80% of actual spend. It sits outside the stack ([Budgets and alerts](doc:fin/budgets-and-alerts)).
- **One control acts at any hour.** The [conformity gate](/inside/services/conformity-gate/) stops a failing deploy and keeps the previous build live without anyone on call. On 2026-10-08 it blocked a deploy, and the run on the fix started 76 seconds later and passed ([incident record](/inside/status/#2026-10-08-gate-blocked-map-push)).
- **How incidents were found.** Of the four records on the [status page](/inside/status/) before alert routing, the gate found one, the blocked deploy. Someone who was working at the time found the other three, and none of those three records the time of the first report or check.

## State

**Partial.** Alerts reach the operator, and a dead alerting path raises its own alarm ([#36](https://github.com/uncovertechtalent/machinebehavior.io/issues/36)). Standby in the full sense is missing: one person, no rotation, and a page at night waits on the board until 08:00 by design. The gate still covers the largest tier-1 risk, a bad page in front of readers, without a person.

## Services that name it

<!-- principle-services -->

## In a company of 10 to 200 people

- Start with one rotation for the services customers meet. Each person should be on call at most one week in four; with fewer people, share one rotation across teams.
- Page only on symptoms users feel, with a runbook link in every page. Everything else becomes a ticket with an owner.
- Pay for standby or give the time back, and review the pager load every month.
- Add a dead man's switch: an always-firing alert that an outside check expects, so a broken alert path raises an alarm too.

## Open work

- [#41 Incident records: when and how each incident was detected](https://github.com/uncovertechtalent/machinebehavior.io/issues/41)
