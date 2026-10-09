title: Runbooks
summary: Operational procedures for common scenarios.
parent: index
order: 40
labels: moc, sre-runbooks
aliases: SRE Runbooks Cluster | SRE Runbooks MOC | Runbooks MOC
type: MOC
created: 2026-04-25
updated: 2026-10-09
origin: SRE/runbooks/README.md
reviewed: no
---
Operational procedures for common scenarios.

## Structure

Each runbook includes:
- **Trigger** — When to use this runbook
- **Prerequisites** — Access, tools needed
- **Steps** — Detailed procedure
- **Verification** — How to confirm success
- **Rollback** — How to undo if needed
- **Escalation** — When and who to contact

## Runbooks

### Incidents
- [x] [[Service Outage Response]] — generic outage triage, mitigate-before-investigate decision tree
- [x] [[Database Failover]] — promote replica to primary, engine-specific gotchas
- [x] [[Rollback Deployment]] — revert prod to last known good, schema-migration tax
- [x] [[Certificate Rotation]] — TLS cert renewal including emergency expiry response

### Operations
- [x] [[SearXNG Health]] — house search engine: rate-limited engines, proxy egress, pacing, Grafana wiring
- [ ] Scaling a service
- [ ] Database maintenance
- [ ] Log rotation
- [ ] Backup verification

### Security
- [x] [[Credential Rotation]] — secret rotation, scheduled vs compromise differentiation
- [ ] Security incident response
- [ ] Access revocation

## Template

```markdown
# [Runbook Title]

## Trigger
When to use this runbook.

## Prerequisites
- [ ] Access to X
- [ ] Tool Y installed

## Steps
1. First step
   ```bash
   command here
   ```
   Expected output: ...

2. Second step
   ...

## Verification
How to confirm the issue is resolved.

## Rollback
How to undo changes if needed.

## Escalation
- First: @on-call
- Then: @team-lead
- Finally: @incident-commander
```
