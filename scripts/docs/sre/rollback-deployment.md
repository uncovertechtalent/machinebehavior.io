title: Rollback Deployment
summary: Revert production to the last known good state.
parent: runbooks
order: 100
labels: deployment, incident-management, runbook
aliases: Deploy Rollback | Revert Production
type: runbook
created: 2026-04-25
updated: 2026-06-08
origin: SRE/runbooks/Rollback Deployment.md
reviewed: no
---
> Revert production to the last known good state. Optimize for speed; investigate after stability is restored. The rollback procedure must be faster than the deploy procedure or it is not a rollback, it is a redeploy.

## Trigger

- Error rate spike correlated with deploy timestamp
- Latency regression > 2x baseline post-deploy
- New error class appearing in logs since deploy
- Customer reports of new broken behavior post-deploy
- Health check failures on freshly-rolled instances
- Bake period not yet expired and metrics already breaching SLO

If unsure whether to roll back: roll back. The cost of an unnecessary rollback is engineering time; the cost of leaving a bad deploy is customer impact.

## Prerequisites

- [ ] Deploy tool access with rollback permissions
- [ ] Knowledge of the previous successful release artifact (tag, commit, image hash)
- [ ] Database migration status: forward-only or reversible? (See "Schema migration tax" below)
- [ ] Feature-flag state: is the broken behavior gated, or is it free-running code?
- [ ] Rollback path has been tested in non-prod within the last 30 days

## Steps

1. **Confirm the suspect deploy.** Deploy timestamp must precede the metric breach by less than the deploy propagation time (typically 0-15 minutes). If the timing does not match, the deploy is innocent; investigate elsewhere first.
2. **Check for schema migrations.** Run the deploy's migration manifest. If the migration is forward-only (added column, added table, added index), rollback is application-only and safe. If the migration is destructive (dropped column, dropped table, type change), you cannot simply roll back the application without data loss; jump to "Schema migration tax".
3. **Check for feature flags.** If the broken behavior is behind a flag, disable the flag instead of rolling back the deploy. Flag flip is faster than redeploy and avoids reverting unrelated good changes that shipped together.
4. **Trigger the rollback.** Tool-specific:
   - Kubernetes: `kubectl rollout undo deployment/<name>` or argocd revert
   - ECS/Fargate: previous task definition + service update
   - Heroku-style PaaS: previous slug release
   - Custom CI: re-promote previous artifact
5. **Verify the new (old) version is rolling out.** Health-check the new pods/instances. Watch the rollout progress. Do not assume it worked because the command returned 0.
6. **Watch the metrics.** Error rate, latency, custom business metrics. Recovery should begin within one full instance lifecycle. If recovery does not begin within 5 minutes, escalate; the rollback may not have worked or the bad behavior may not be caused by the deploy.
7. **Drain any compromised data.** If the bad deploy wrote bad data (corrupt records, wrong format, partial transactions), the rollback restores code but does not fix data. Open a follow-up data-cleanup incident.
8. **Communicate the rollback.** In the incident channel and to the deploy owner. Include the deploy hash that was rolled back so the owner can investigate without confusion about what is in production.
9. **Block re-deploy of the bad artifact.** Tag it as known-broken in the deploy tool. Most rollback regressions happen because someone re-deploys the bad artifact thinking the original failure was transient.

## Verification

- Error rate, latency, and custom metrics returned to baseline within 10 minutes
- No new error classes appearing in logs since rollback
- Synthetic monitors green for one full bake period
- The deploy tool shows the previous version active across all instances

## Rollback

The rollback of a rollback is a redeploy. Treat it as a new deploy event. Do not skip CI, do not skip canary, do not skip bake period.

## Schema migration tax

Forward-only schema is the operational discipline. Every migration should be:

1. **Backward-compatible at deploy time** (existing code still works against new schema)
2. **Forward-compatible at deploy+1** (new code works against new schema)
3. **Cleanup migration ships separately** (drop the unused column in a later release after the new code is stable)

If your migrations follow this pattern, you can always roll back the application code. If they do not, you have coupled application rollback to data loss, and you need to either restore from backup (separate runbook) or write code forward.

## Escalation

| Tier | Trigger |
|---|---|
| Deploy author | Always — they own debugging the bad change |
| Engineering manager | Rollback fails OR rollback creates new regression |
| Database/data team | Bad data was written and needs cleanup |
| Incident commander | Customer impact during rollback window |

## Regulatory and control mappings

- [[ISO 27001 Annex A.8 Technological Controls]] A.8.32 Change management. A.8.9 Configuration management. A.8.31 Separation of development, test and production environments.
- [[ITIL 4 Practices]] Change Enablement + Deployment Management + Release Management.
- [[NIS2 Security Measures]] Art 21(e) secure development + change management + vulnerability handling.
- [[DORA ICT Risk Management]] Art 9 protection (change controls).

## See also

[[Service Outage Response]] · [[Database Failover]] · [[06-cicd-deployment]] · [[01-reliability]] · [[ISO 27001 Annex A.8 Technological Controls]] · [[ITIL 4 Practices]] · [[README]] (runbooks)
