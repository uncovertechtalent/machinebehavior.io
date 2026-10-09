title: Unit Economics of Infrastructure
summary: Total cloud spend is the wrong metric.
parent: cost-optimization
order: 100
labels: cost-optimization, finops, practice
aliases: Unit Cost | Cost per Request | Infrastructure Unit Economics | FinOps Unit
type: practice
created: 2026-05-04
updated: 2026-05-04
origin: SRE/pillars/09-cost-optimization/Unit Economics of Infrastructure.md
reviewed: no
---
> Total cloud spend is the wrong metric. **Cost per business unit** — per request, per active user, per transaction, per GB delivered — is the only metric that survives growth. A bill that doubles is fine if traffic tripled. A bill that grows 5% while traffic is flat is the real problem.

## The unit is the lens

Pick the unit that matches the business:

- API platform → cost per million requests
- Streaming service → cost per stream-hour
- SaaS app → cost per active tenant per month
- Data pipeline → cost per GB processed
- ML inference → cost per inference call

The unit must be something the business already cares about. Otherwise FinOps becomes a cost-center reporting function instead of an engineering input.

## What the unit-cost view exposes

Aggregate spend hides the things that matter:

- A pricing tier that loses money at scale (free-tier abuse)
- A growth path that gets more expensive per user, not less (anti-economy of scale)
- A specific workload that dominates spend (often a forgotten cron, a dev environment never shut down, an over-provisioned analytics warehouse)
- An architecture choice with bad asymptotic behavior (per-request RDS connections, NAT gateway charges on egress-heavy services)

When the unit-cost trend turns up while traffic is flat, the system has degraded. When it turns down while traffic grows, engineering effort is paying off. Trends in unit cost are the signal; absolute spend is noise.

## The four interventions, ranked by leverage

| Intervention | Leverage | Cost |
|---|---|---|
| Eliminate waste (idle, orphaned, over-provisioned resources) | High | Low. Often a tagging-and-cleanup pass. |
| Right-size (shrink to actual demand) | High | Medium. Requires utilization data. |
| Commit / reserve (1y/3y RIs, savings plans) | Medium | Low money-cost, locks in workload assumptions. |
| Architectural change (smaller instance class, serverless, spot) | Highest | High. Engineering project. |

Most teams skip 1 and 2, jump to 3 prematurely (locking in inefficient utilization), and never get to 4. The right order is top-down. **Reserving capacity you don't need is more expensive than paying on-demand for what you actually use.**

## The discipline

- **Tag everything.** Every resource carries owner, project, environment. Untagged resources are unaccountable resources.
- **Show the bill back.** Engineering teams see the cost of what they ship, in their language. Cost lives in the dashboard alongside latency and error rate, not in a finance review.
- **Budget per project.** With alerts at 50%, 80%, 100%. The team owns the budget.
- **Continuous, not quarterly.** A quarterly cost review is theater. Drift compounds at the speed of new commits.

## Where SRE pays for itself

The Pillar 9 work that returns the most:

- Idle-resource killer: nightly automation that stops/scales-down dev environments, scratch clusters, abandoned RDS instances. Saves single-digit % to double-digit % of spend depending on hygiene.
- Spot-instance plumbing for stateless workloads. 60-90% discount with engineering work for handling termination.
- Egress audit. NAT gateway and inter-AZ egress are the silent cost lines. A single misrouted log shipper can dominate the bill.
- S3 lifecycle policies. Aged objects to IA / Glacier on schedule. Forgotten buckets are the most common single-point cost surprise.

## Anti-patterns

- **Optimizing percentage without checking absolute spend.** Saving 30% on a $200/month service while a $20K/month workload runs untouched.
- **Right-sizing for peak.** The whole point of cloud is to size for actual, not worst-case. Use autoscaling.
- **Reserved instances on a workload that will be retired.** RI commitments outlive products.
- **Cost reviews without a system-of-record.** The numbers move every week; without unit cost as the canonical metric, optimization conversations are anecdote-driven.

## See also

[[README]] · [[02-scalability]] · [[10-toil-reduction]]
