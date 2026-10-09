title: 4. Incident Management
summary: "It's not about preventing all failures.
parent: pillars
order: 40
aliases: Incident Management Cluster | SRE Incident Management Cluster | 04-incident-management
created: 2026-04-25
updated: 2026-09-21
origin: SRE/pillars/04-incident-management/README.md
reviewed: no
---
> "It's not about preventing all failures. It's about recovering fast."

## What is Incident Management?

The structured approach to identifying, responding to, resolving, and learning from service disruptions.

## Incident Lifecycle

```
Detection → Triage → Response → Resolution → Review → Prevention
```

## Key Concepts

### Severity Levels

| Level | Definition | Response |
|-------|------------|----------|
| SEV1 | Critical — Major customer impact, revenue loss | All hands, war room |
| SEV2 | High — Significant degradation, workaround exists | On-call + escalation |
| SEV3 | Medium — Minor impact, limited scope | On-call handles |
| SEV4 | Low — Minimal impact, cosmetic | Next business day |

### Incident Roles
- **Incident Commander (IC)** — Coordinates response, makes decisions
- **Communications Lead** — Updates stakeholders, status page
- **Operations Lead** — Technical investigation and remediation
- **Scribe** — Documents timeline and actions

### MTTX Metrics
- **MTTD** — Mean Time To Detect
- **MTTA** — Mean Time To Acknowledge
- **MTTR** — Mean Time To Resolve
- **MTBF** — Mean Time Between Failures

## Topics

- [ ] On-call rotations
- [ ] Escalation paths
- [ ] War room protocols
- [ ] Status page management
- [ ] Customer communication
- [ ] Postmortem process
- [ ] Blameless culture
- [ ] Runbook development
- [ ] Incident tooling
- [ ] Chaos engineering

## On-Call

### Sustainable On-Call
- No more than 25% of time in on-call
- Maximum 2 incidents per shift
- Compensatory time off after pages
- Clear escalation when overwhelmed

### On-Call Checklist
- [ ] Laptop and connectivity
- [ ] VPN access working
- [ ] Alert routing confirmed
- [ ] Runbooks accessible
- [ ] Escalation contacts known

## Postmortems

### Structure
1. **Summary** — What happened, impact, duration
2. **Timeline** — Detailed sequence of events
3. **Root Cause** — Why it happened (5 Whys)
4. **Impact** — Users affected, revenue lost
5. **Action Items** — Specific, assigned, time-bound
6. **Lessons Learned** — What we'll do differently

### Blameless Culture
- Focus on systems, not individuals
- "What failed" not "who failed"
- Assume good intentions
- Share learnings widely

## Runbooks

### Good Runbook
- Clear trigger (when to use)
- Step-by-step actions
- Expected outcomes at each step
- Escalation criteria
- Rollback procedures
- Recently tested

## Tools

| Tool | Purpose |
|------|---------|
| PagerDuty | Alerting and on-call |
| Opsgenie | Incident management |
| Statuspage | External communication |
| Jira/Linear | Action item tracking |
| Slack/Teams | War room coordination |
| Rootly/Incident.io | Incident automation |

## Anti-Patterns

- Hero culture (one person fixes everything)
- Blame-driven postmortems
- Action items that never get done
- Runbooks that don't work
- Alert fatigue leading to ignored pages

## Regulatory and standard mappings

### Incident management controls

- [[ISO 27001 Annex A.5 Organizational Controls]] A.5.24-A.5.28 — incident management planning, assessment, response, learning, evidence collection.
- [[ITIL 4 Practices]] Incident Management + Problem Management + Service Continuity Management.
- [[NIST CSF Core Functions]] RESPOND function + RECOVER function.
- [[NIST AI RMF Core Functions]] MANAGE function — AI incident response.

### Mandatory incident reporting timelines

- [[GDPR Controller and Processor]] Art 33: 72h to DPA for personal data breach. Art 34: data subject notification when high risk.
- [[NIS2 Incident Reporting]] Art 23: 24h early warning + 72h notification + 1m final report for significant incidents.
- [[DORA Incident Reporting]] Art 19: initial 4h + intermediate + final 1m for major ICT-related incidents.
- [[Cyber Resilience Act Cluster]] Art 14: 24h for actively exploited vulnerabilities and severe incidents.
- [[EU AI Act Cluster]] Art 73: 15-day default + tighter timelines for fundamental rights and widespread harm cases.

Integrated incident response workflow should accommodate multi-regime parallel reporting.

## Reading

- Google SRE Book: Chapters 12-15 (Effective Troubleshooting, Emergency Response, Postmortem Culture)
- Incident Management for Operations (O'Reilly)
## People-substrate cross-cluster

Incidents fire the nervous system. The operator's defense response under incident pressure is the lagging indicator of substrate. Blameless postmortems require real emotional maturity; without it, postmortems produce scapegoat-child dynamics at organizational scale.

- Bridge essay: [[interview-training-psychology-parallels|Interview Training as Applied Clinical Psychology]] -- Item 7 (the debrief room is a miniature dysfunctional family unless engineered against)
- Developmental-position: [[pillars/developmental-position/Defense-Response Model|Defense-Response Model]] -- which defense (fight / flight / freeze / fawn) the operator runs under incident pressure; the response is data, not character
- Developmental-position: [[pillars/developmental-position/Freeze Cascade|Freeze Cascade]] + [[pillars/developmental-position/Denial Cascade|Denial Cascade]] -- the failure cascades that produce MTTR blow-out
- Psychology: [[pillars/psychology/nervous-system-regulation-patterns|Nervous-system regulation patterns]] -- communication shutdown under dysregulation = the MTTR-degrading mechanism at the human layer
- Psychology: [[pillars/psychology/real-emotional-maturity|Real emotional maturity]] -- prerequisite for blameless postmortem to land; without it, "blameless" is performed while substrate runs blame
- Anti-pattern (scapegoat): [[pillars/psychology/scapegoat-child-in-dysfunctional-families|Scapegoat-child dynamics]] -- the team-level pattern that hijacks postmortems; one person absorbs the system's projection
- Competency: [[conflict-capacity|Conflict Capacity]] + [[emotional-regulation|Emotional Regulation]] -- the dimensions incident commanders need; SEV1 reveals which dimension is under-developed

## Atoms

- [[Blameless Postmortem Discipline]]
- [[Transcriber Incident Register]]: a worked incident record as typed atoms (11 incidents with causes, mitigations, detection methods), added 2026-09-21
