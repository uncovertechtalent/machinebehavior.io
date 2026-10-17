title: ADR-0037: A pager on Discord with a rotation, the board for every alert, and an outside heartbeat
summary: One Alertmanager serves both Prometheus servers in the house. A page becomes an incident in a PagerDuty-style pager on a private Discord server, with Acknowledge, Resolve and Escalate buttons, a rotation and an escalation policy in pager/rotation.yml, and a read-only responder agent as its second layer. Every page and ticket also opens an issue on the board, which keeps the page's redacted record; the on-call pages show the rotation, the last pages and the pager load from a public snapshot. An always-firing Watchdog per Prometheus pings a heartbeat check outside the house.
parent: decision-log
order: 37
adr: 37
status: accepted
created: 2026-10-17
supersedes: adr-0017-on-call-model
labels: adr, decision, on-call, alerts, alertmanager, pager, rotation, discord, heartbeat
owner: Stefan Coetzee
reviewed: 2026-10-17
review_by: 2027-01-15
type: explanation
---
## Context

[ADR-0017](doc:eng/adr-0017-on-call-model) stated the on-call model and proposed a routing that it left unwired, waiting for the operator's choice of receivers. Prometheus evaluated the platform's alert rules, and on 2026-10-17 the NAS monitoring Prometheus gained three rules for the UniFi gateway; none of them reached a person, and a dead Prometheus looked like a quiet night. On 2026-10-17 Stefan Coetzee chose Discord for pages and the board for tickets ([#36](https://github.com/uncovertechtalent/machinebehavior.io/issues/36)), then asked for Discord to work the way PagerDuty does, with a standby rotation to show, on a new server of its own.

## Decision

**One Alertmanager for both Prometheus servers.** It runs in the agent-observability compose stack. Each Prometheus names itself on every alert with an external label and signs in with its own user; every endpoint needs basic auth, because an alert posted to it can end up as a public issue.

**A pager between Alertmanager and the person.** A small service in the stack's repository (`pager/`) turns each page into an incident on a private Discord server: one message with Acknowledge, Resolve and Escalate buttons, updated on every action, and a thread under it for the timeline. Incidents are keyed by alert fingerprint; Alertmanager's resolve closes them, and an incident that hears nothing for 2.5 hours closes as stale. The bot is a separate Discord application with six permissions and no privileged intent, its token held on the home server only; it connects out to Discord, so nothing in the house is exposed.

**A rotation and an escalation policy in a file.** `pager/rotation.yml` uses PagerDuty's model: schedules with layers and restrictions, overrides from the file or a slash command, and an escalation policy. The primary is the operator from 08:00 to 22:00 Berlin time, mentioned again every 5 minutes up to 3 times without an acknowledgement. At 15 minutes the responder layer runs. A level with nobody on call passes the page on at once, so out of hours the responder takes it immediately and the operator hears at 08:00 if it is still open.

**The responder agent is read-only.** It posts the alert's runbook link and a diagnosis from Prometheus queries in the incident thread. It changes nothing and never acknowledges; a person still owns every page.

**Every page and ticket on the board.** `alert-issues` keeps one GitHub issue per alert fingerprint, labelled `kind:finding` and an area, and shows only scrubbed fields. The pager sends each page's redacted record (names from the rotation and times) to that issue. The on-call and standby pages read these records and the rotation in a snapshot that the deploy job refreshes, so the public view needs no endpoint into the house and shows no Discord ID or channel.

**What goes nowhere.** `info`, and the three AWS spend rules, which stay a showcase on the AWS spend dashboard.

**Watching the alerting path.** Each Prometheus carries an always-firing `Watchdog`; Alertmanager sends it to that Prometheus's heartbeat check outside the house every 5 minutes, and the check alarms when the pings stop. A down, disconnected or failing pager, and a notification Alertmanager gave up on, go to the alerting-path channel by webhook, past the pager.

## Consequences

A page reaches the operator in waking hours with a button to own it, and the responder's diagnosis is in the thread before anyone looks at a page that came at night. Each page leaves a board issue with its history and its time to acknowledge and to resolve, which the public snapshot counts per week. Nobody is woken at night, by design, so standby stays thin: one person and one human layer. The setup adds a published Alertmanager port with basic auth, a GitHub token that can write issues on one repository, a Discord bot token, a webhook for the alerting-path channel and two heartbeat checks, all held as mode-600 files on the home server, plus a deploy step that reads public GitHub data. `scripts/check-alerting.sh` checks the configuration, every rule's route and the unit tests of both services without sending anything. A public read-only feed channel can be added later as one more consumer of the same redacted record. Routing, rotation and rules: [On-call and escalation](doc:obs/on-call).
