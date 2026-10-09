title: Service Outage Response
summary: Generic triage runbook for production service unavailability.
parent: runbooks
order: 100
labels: incident-management, runbook, sev1
aliases: Outage Triage | Service Down Response
type: runbook
created: 2026-04-25
updated: 2026-06-08
origin: SRE/runbooks/Service Outage Response.md
reviewed: no
---
> Generic triage runbook for production service unavailability. Optimize for time-to-mitigation, not time-to-root-cause. Diagnosis happens after the bleeding stops.

## Trigger

- Synthetic monitor failing for > 2 consecutive checks
- Error rate > 5x baseline sustained for 60s
- p95 latency > 3x baseline sustained for 60s
- Customer-reported outage with reproduction steps
- Dependency failure cascade detected (cross-service)

If unsure whether to declare: declare. The cost of a false positive is a Slack message; the cost of a false negative is customer trust.

## Prerequisites

- [ ] Production access (read at minimum)
- [ ] On-call alerting tool credentials (PagerDuty, Opsgenie)
- [ ] Communication channel access (status page, customer Slack, exec bridge)
- [ ] Authority to invoke rollback (or escalation path)

## Steps

1. **Acknowledge the alert.** Stop further pages from this incident. Note the time.
2. **Open the incident channel.** One channel, one incident. All comms route through it.
3. **Assign roles.** Incident Commander (decisions), Communications (status updates), Subject Matter Experts (investigation). Do not start step 4 before step 3.
4. **Verify the outage scope.** Check from outside (synthetic monitor), inside (internal dashboard), and from a customer perspective. Distinguish between full outage, partial outage, and degraded performance.
5. **Check the deploy timeline.** What shipped in the last 4 hours? `git log --since="4 hours ago" --oneline` plus deploy-tool history. Recent deploys are guilty until proven innocent.
6. **Mitigate, do not investigate.** Decision tree:
   - Recent deploy + suspected correlation → roll back. See [[Rollback Deployment]].
   - Database primary unavailable → failover. See [[Database Failover]].
   - Capacity exhaustion → scale horizontally if autoscaling is broken.
   - Dependency outage → enable degraded mode (cached responses, feature flag off, queue drain).
   - Unknown → restart the affected service. Capacity-limited customers complain less than blocked customers.
7. **Communicate every 15 minutes.** Even with no new info, post a heartbeat. Silence equals panic on the customer side.
8. **Stabilize.** Verify metrics recovered to baseline. Wait for one full bake period (5-15 min) before declaring the incident over.
9. **Close the incident.** Summary in the channel: detected, declared, mitigated, restored. Open the postmortem doc.

## Verification

- All synthetic monitors green for one full bake period
- Error rate within 1.5x baseline
- p95 latency within 1.5x baseline
- No new customer reports for 15 minutes
- Pinned-down deploy or change is confirmed reverted, paused, or behind a flag

## Rollback

If mitigation made things worse: revert the mitigation immediately. The previous degraded state is better than an actively failing one. Document the reversion in the channel.

## Escalation

| Tier | Trigger |
|---|---|
| Secondary on-call | 15 minutes without progress |
| Engineering manager | Customer impact > $10k OR reputational risk |
| Incident Commander (senior) | Multi-service or multi-team impact |
| Executive bridge | Outage > 30 min, public-facing, OR media risk |

## Postmortem

Owner: incident commander. Due: 5 business days. Format: blameless, mechanism-focused, with concrete action items owned by named people. See [[04-incident-management]] pillar for postmortem standards.

## Regulatory reporting touchpoints

If the outage involves personal data, financial services, critical infrastructure, products with digital elements, or AI systems, reporting obligations may run in parallel:

- **Personal data breach**: [[GDPR Controller and Processor]] Art 33 — 72h notification to DPA. Art 34 — data subject notification if high risk.
- **NIS2 essential / important entity significant incident**: [[NIS2 Incident Reporting]] — 24h early warning + 72h notification + 1m final.
- **Financial entity major ICT incident**: [[DORA Incident Reporting]] — 4h initial + intermediate + 1m final.
- **Product cybersecurity (actively exploited or severe incident)**: [[CRA Essential Requirements]] Art 14 — 24h to ENISA.
- **AI Act high-risk serious incident**: [[EU AI Act High-Risk Obligations]] Art 73 — 15-day default, tighter for fundamental rights / widespread.

Treat reporting workflow as part of incident workflow; do not bolt on after.

## See also

[[Rollback Deployment]] · [[Database Failover]] · [[Certificate Rotation]] · [[Credential Rotation]] · [[04-incident-management]] · [[NIS2 Incident Reporting]] · [[DORA Incident Reporting]] · [[GDPR Controller and Processor]] · [[ISO 27001 Annex A.5 Organizational Controls]]
