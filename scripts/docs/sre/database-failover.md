title: Database Failover
summary: Promote a replica to primary when the current primary is unhealthy.
parent: runbooks
order: 100
labels: database, incident-management, runbook
aliases: DB Failover | Primary Replica Promotion
type: runbook
created: 2026-04-25
updated: 2026-06-08
origin: SRE/runbooks/Database Failover.md
reviewed: no
---
> Promote a replica to primary when the current primary is unhealthy. The procedure is identical for planned maintenance and unplanned outage; the difference is preparation time.

## Trigger

- Primary database unreachable for > 30s
- Primary disk full or critical resource exhausted
- Primary replication lag > 60s with no recovery trend
- Planned maintenance requiring primary downtime > 2 minutes
- Disaster recovery drill (run quarterly minimum)

## Prerequisites

- [ ] DB admin credentials (or break-glass access)
- [ ] Replica health verified within last 5 minutes
- [ ] Replica is in the same DR zone as the new traffic source, OR cross-zone latency is acceptable
- [ ] Application uses connection-string indirection (DNS, service discovery, or DB proxy) — NOT hardcoded primary IPs
- [ ] Knowledge of the specific DB engine's failover mechanics (Postgres streaming, MySQL GTID, MongoDB replica set, etc.)

## Steps

1. **Verify the primary is actually down.** Many "primary down" alerts are network partitions. Check from multiple monitoring sources before failing over. A split-brain incident is significantly worse than a 30-second wait.
2. **Identify the failover target.** Lowest replication lag, healthy, in the desired zone. List all replicas; do not assume.
3. **Stop writes to the primary.** If reachable: `ALTER SYSTEM SET default_transaction_read_only = on;` (Postgres) or equivalent. If unreachable: skip and accept potential write loss documented in step 8.
4. **Drain in-flight transactions.** Wait for active transactions to complete or timeout. Maximum wait: 30 seconds. Document any long-running transactions that hit the timeout.
5. **Promote the replica.** Engine-specific:
   - Postgres: `pg_ctl promote` or `SELECT pg_promote();`
   - MySQL/Aurora: `STOP REPLICA; RESET REPLICA ALL;` then redirect
   - Managed services: cloud-provider failover API (AWS RDS reboot-with-failover, GCP Cloud SQL, Azure failover group)
6. **Update connection routing.** DNS, service discovery, or proxy configuration. This is the cutover moment. Confirm propagation:
   - DNS: check from a few sample machines, expect 60s for TTL respect
   - Service discovery: confirm new endpoint registered, old marked unhealthy
   - Proxy: confirm health-check has switched
7. **Verify application reconnects.** Tail application logs for connection errors. Most apps need to drop their connection pool and rebuild against the new primary. Some need a forced restart.
8. **Document write loss, if any.** If step 3 was skipped, calculate the worst-case write loss (replication lag at failure × write rate). Communicate this to product/customer ops if customer-visible.
9. **Promote a new replica from the old primary.** Once the old primary is recoverable, reattach as a replica of the new primary. Do NOT run as a second primary; that is split-brain.

## Verification

- Application connection error rate returned to baseline
- Write transactions succeed against the new primary
- Replica replication established and lag < 5s within 5 minutes
- No customer-visible errors related to data unavailability

## Rollback

Rollback after promotion is a re-failover. Treat it as a new failover event with fresh prerequisites checked. Do not assume the old primary is healthy without re-validation.

## Escalation

| Tier | Trigger |
|---|---|
| DBA on-call | Replication lag > 60s post-failover |
| Engineering manager | Write loss > 0 |
| Database vendor (paid support) | Replica refuses to promote |
| Incident commander | Cascading impact on dependent services |

## Specific gotchas by engine

- **Postgres logical vs streaming replication**: behavior differs significantly on promote. Streaming is the supported failover path; logical typically is not.
- **MySQL GTID**: ensure GTID consistency before promotion or you cannot rejoin the old primary as a replica without re-sync.
- **Aurora**: failover is API-driven. The cluster endpoint follows automatically; the reader endpoint does not.
- **Self-hosted with proxy (PgBouncer, ProxySQL)**: the proxy's health check determines actual cutover. Test proxy behavior in a drill before relying on it.

## Regulatory and control mappings

- [[ISO 27001 Annex A.5 Organizational Controls]] A.5.29 Information security during disruption. A.5.30 ICT readiness for business continuity. A.8.13 Information backup. A.8.14 Redundancy of information processing facilities.
- [[ISO 22301 Clause Structure and Key Concepts]] business continuity management; BIA / RTO / RPO discipline.
- [[NIS2 Security Measures]] Art 21(c) business continuity (backup, disaster recovery, crisis management).
- [[DORA ICT Risk Management]] Art 11 response and recovery + Art 12 backup policies and procedures.

## See also

[[Service Outage Response]] · [[Rollback Deployment]] · [[01-reliability]] · [[04-incident-management]] · [[ISO 22301 Clause Structure and Key Concepts]] · [[DORA ICT Risk Management]] · [[README]] (runbooks)
