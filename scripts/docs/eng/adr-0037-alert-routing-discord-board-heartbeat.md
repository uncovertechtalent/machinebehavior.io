title: ADR-0037: Alerts go to Discord and the board, with an outside heartbeat on the alerting path
summary: One Alertmanager serves both Prometheus servers in the house. A page goes to Discord between 08:00 and 22:00 Berlin time and opens an issue on the board at any hour, a ticket opens an issue, info and the three AWS spend rules go nowhere, and an always-firing Watchdog per Prometheus pings a heartbeat check outside the house. Every Alertmanager endpoint needs basic auth, and an alert issue on the public board shows only scrubbed fields.
parent: decision-log
order: 37
adr: 37
status: accepted
created: 2026-10-17
supersedes: adr-0017-on-call-model
labels: adr, decision, on-call, alerts, alertmanager, discord, heartbeat
owner: Stefan Coetzee
reviewed: 2026-10-17
review_by: 2027-01-15
type: explanation
---
## Context

[ADR-0017](doc:eng/adr-0017-on-call-model) stated the on-call model and proposed a routing that it left unwired, waiting for the operator's choice of receivers. Prometheus evaluated the platform's alert rules, and on 2026-10-17 the NAS monitoring Prometheus gained three rules for the UniFi gateway; none of them reached a person. A dead Prometheus and a quiet night looked the same. On 2026-10-17 Stefan Coetzee chose the receivers: page alerts go to Discord, and tickets to a webhook that opens or updates an issue on the board, as [#36](https://github.com/uncovertechtalent/machinebehavior.io/issues/36) proposed.

## Decision

**One Alertmanager for both Prometheus servers.** It runs in the agent-observability compose stack. Each Prometheus names itself on every alert with an external label and signs in with its own user; every endpoint needs basic auth, because an alert posted to it can end up as a public issue.

**Severity picks the receiver.** A `page` goes to Discord between 08:00 and 22:00 Europe/Berlin, through Alertmanager's own Discord integration and a channel webhook, and opens an issue on the board at any hour. A `ticket` opens an issue. `info` goes nowhere, and so do the three AWS spend rules, which stay a showcase on the AWS spend dashboard; the stale-exporter rule beside them is a ticket. Inhibition keeps one cause to one alert: a down Ollama silences the SLO burns behind it, and a down SearXNG the other SearXNG alerts.

**One issue per alert.** A small receiver in the stack's repository, `alert-issues`, keeps one issue per alert fingerprint, labelled `kind:finding` and an area. A repeat refreshes the body, a resolve comments and closes the issue, and a new firing episode reopens it. The board is public, so the issue shows the alert name, the summary, the times and an allowlist of labels, with URLs and IP addresses removed and no mention or issue link possible.

**A heartbeat outside the house.** Each Prometheus carries an always-firing `Watchdog`. Alertmanager sends it to that Prometheus's heartbeat check outside the house every 5 minutes, and the check alarms when the pings stop.

Four points differ from the proposal in ADR-0017. Every page is also a ticket, day and night: a ticket route muted by day would drop the resolved notice of a page that started at night and leave its issue open, and the proposal's night route followed a route that already matched, so it could never fire. The three AWS spend rules are not delivered. Both Prometheus servers share the one Alertmanager. Basic auth and the scrubbing of issue text were not in the proposal.

## Consequences

The five page rules reach the operator in waking hours, and every page and ticket leaves an issue with a history on the board. Nobody is woken at night: a page then waits on the board and reaches Discord at 08:00 if it still fires, and Discord can keep showing a page as firing after it resolved at night, so the issue is the record. A dead Prometheus, Alertmanager, home server or uplink now raises an alarm from outside. The setup adds a published Alertmanager port with basic auth, a GitHub token that can write issues on one repository, a Discord webhook and two heartbeat checks, all held as mode-600 files on the home server. `scripts/check-alerting.sh` in the stack's repository checks the configuration, every rule's route and the receiver's unit tests without sending anything. Routing and rules: [On-call and escalation](doc:obs/on-call).
