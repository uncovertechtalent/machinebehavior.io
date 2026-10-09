title: Symptoms over Causes for Alerting
summary: Page when users are affected.
parent: observability
order: 100
labels: alerting, observability, practice
aliases: Symptom-Based Alerting | User-Facing Alerting | Alert Discipline
type: practice
created: 2026-05-04
updated: 2026-05-04
origin: SRE/pillars/03-observability/Symptoms over Causes for Alerting.md
reviewed: no
---
> Page when users are affected. Investigate when components are unhappy. The discipline that distinguishes a useful alerting system from a noisy one is the rule that **only customer-visible symptoms wake humans up**. Everything else is a ticket.

## Why cause-based alerts fail

A "CPU > 80%" alert pages someone. They look. CPU is high because of a batch job. Users are fine. The page was wasted. Repeat 50 times. The on-call ignores the next one. The next one is real.

This is alert fatigue, and it is what happens when alerts fire on internal causes (CPU, queue depth, disk %) instead of external symptoms (error rate, latency, availability). The cause-based alert is a guess that *some* downstream symptom will appear. Often it does not — the system has slack, retries, fallback paths. The cause was real; the symptom never materialized.

## The discipline

Three tiers, with strict rules about what belongs in each:

| Tier | What fires it | What happens |
|---|---|---|
| **Page** | Customer-visible symptom: error rate, p99 latency, availability, broken user flow | Wakes someone up at 3am |
| **Ticket** | Internal anomaly likely to become a symptom: leaked file descriptors, queue growth, expiring cert | Fix during business hours |
| **Log** | Anything else worth being able to find later | Searchable, no notification |

The Four Golden Signals (latency, traffic, errors, saturation) belong on the page tier *only when expressed as user impact*. "Latency p99 > 500ms over 5 minutes" pages. "CPU is high" tickets at most.

## The mental model

Imagine you are paged. Before you look at anything, ask: **what user, doing what, is affected right now?** If you cannot answer that question from the alert itself, the alert was cause-based, not symptom-based. Demote it.

## What to actually alert on

For most request-driven services, two pages suffice:

- **Availability burn-rate:** error budget is being consumed faster than the SLO permits over a multi-window check (e.g. 2% budget burn in 1h AND 5% in 6h).
- **Latency burn-rate:** same shape, applied to the latency SLO.

That's it. Everything else — saturation, growth, capacity headroom — is a ticket. The page list should fit in your head.

## Anti-patterns

- **Alert on every metric.** Dashboard ≠ alert.
- **Static thresholds for traffic-driven systems.** 500 errors/sec is fine at peak, catastrophic at trough. Use rates, not counts.
- **Alerts without runbooks.** If the on-call cannot resolve it from the page, the page is a question, not an alert.
- **Severity drift.** Sev1 should be rare. If sev1 fires weekly, it has been redefined to mean "interesting", not "emergency".

## See also

[[CPU Cache Hierarchy and Speculative Execution]] · [[Service Outage Response]] · [[01-reliability]] · [[04-incident-management]]
