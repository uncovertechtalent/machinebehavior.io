title: Every incident ends in a record
summary: Each incident is written up without blame, with impact, timeline, cause and follow-up work, and the lesson becomes a runbook or a fix. Here four incident records sit on the status page with stages, write-ups and tickets; detection times, a template and an index are missing.
parent: principles-in-practice
order: 120
labels: principle, sre, incidents, postmortem, blameless
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
state: partial
source: [Pillar 4, blameless postmortems](doc:sre/blameless-postmortem-discipline); [Google SRE book ch. 15](https://sre.google/sre-book/postmortem-culture/)
---
## The principle

An incident ends when the service works again and the record is written. A blameless postmortem assumes everyone acted reasonably on the information they had, and asks what in the system let the failure happen and what would catch it earlier. The record holds the impact, the timeline, the cause and follow-up work with owners, and the lesson turns into a runbook, a test or a fix.

Source: [Incident Management](doc:sre/incident-management) and [Blameless Postmortem Discipline](doc:sre/blameless-postmortem-discipline); Google's [Postmortem Culture: Learning from Failure](https://sre.google/sre-book/postmortem-culture/).

## On this platform

- **Records with stages.** Each incident is a YAML file in [incidents/](https://github.com/uncovertechtalent/machinebehavior.io/tree/main/incidents) with impact, services, summary and dated updates through investigating, identified, monitoring and resolved. The build stops when the stages go backwards or a service is not in the catalog, and the [status page](/inside/status/) renders open and past incidents ([Status page](doc:eng/status-page)).
- **Write-ups linked from the record.** The [phantom spend](/inside/status/#2026-10-09-phantom-spend-counters) record links a FinOps case study, a runbook, the budgets page and an open follow-up ticket ([#29](https://github.com/uncovertechtalent/machinebehavior.io/issues/29)). The [tag pages](/inside/status/#2026-10-08-utt-tag-pages-xml) record names the guard the crawler kept afterwards. The [SearXNG](/inside/status/#2026-10-09-searxng-engine-suspensions) record, still open, lists every change made and the choice that remains.
- **A control working is also a record.** The [blocked deploy](/inside/status/#2026-10-08-gate-blocked-map-push) of 2026-10-08 had no reader impact; it is kept because a blocked deploy is the case the gate exists for, and its runbook was written the same day.
- **Runbooks from failures.** Each Engineering runbook covers one failure that has happened, with how to see it, the cause and the fix ([Runbooks](doc:eng/runbooks)); the Observability runbooks follow the same rule ([Observability runbooks](doc:obs/runbooks)).
- **Records name mechanisms.** The records say what broke and why; none names a person at fault. The handbook's own [incident records](doc:sre/incidents) from earlier work follow the same form and name their sources.

## State

**Partial.** Every incident on the platform has a record, a write-up and a fix. Three parts are missing. The records do not say when and how each incident was detected; three of four say the time was not recorded ([#41](https://github.com/uncovertechtalent/machinebehavior.io/issues/41)). There is no postmortem index across the records ([#22](https://github.com/uncovertechtalent/machinebehavior.io/issues/22)) and no template for a write-up ([#20](https://github.com/uncovertechtalent/machinebehavior.io/issues/20)). Follow-up work has a ticket for one of the four incidents.

## Services that name it

<!-- principle-services -->

## In a company of 10 to 200 people

- Write a record for every incident that reached a customer and for every near miss a control caught, within five working days.
- Use one template: impact, timeline with detection time, contributing causes, what went well, follow-up items with owners and dates.
- Review the records in a monthly meeting open to the whole engineering team, and track follow-up items on the same board as feature work.
- Ban names in the cause section. Ask what made the action reasonable at the time.

## Open work

- [#41 Incident records: when and how each incident was detected](https://github.com/uncovertechtalent/machinebehavior.io/issues/41)
- [#22 Postmortem index](https://github.com/uncovertechtalent/machinebehavior.io/issues/22)
- [#20 Templates space](https://github.com/uncovertechtalent/machinebehavior.io/issues/20)
- [#29 Cost counters: drop them or alert on their resets](https://github.com/uncovertechtalent/machinebehavior.io/issues/29)
