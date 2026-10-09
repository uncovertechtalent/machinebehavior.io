title: Error Budgets as Reliability Currency
summary: An error budget is the only mechanism that makes the reliability-vs-velocity trade-off concrete.
parent: reliability
order: 100
labels: error-budget, practice, reliability, slo
aliases: Error Budget | SLO Error Budget | Reliability Currency
type: practice
created: 2026-05-04
updated: 2026-05-04
origin: SRE/pillars/01-reliability/Error Budgets as Reliability Currency.md
reviewed: no
---
> An error budget is the only mechanism that makes the reliability-vs-velocity trade-off concrete. Without it, "ship faster" and "stay reliable" are unfalsifiable opinions. With it, they are competing claims on the same finite ledger.

## The math is the point

A 99.9% SLO over 30 days is not a target — it is **a budget of 43.2 minutes of failure per month**. That budget belongs to the engineering org, not the SRE team. Every minute the service is unavailable, error-budget burns. Every minute it isn't, the budget refills toward the cap.

| SLO | Allowed downtime / month |
|---|---|
| 99% | 7.3 hours |
| 99.9% | 43.2 minutes |
| 99.95% | 21.6 minutes |
| 99.99% | 4.32 minutes |
| 99.999% | 26 seconds |

Each additional 9 costs roughly 10x in engineering effort. The right SLO is the **lowest one your customers will tolerate**. Above that, you are spending engineering hours on reliability that has no business return.

## The error-budget policy is the contract

The number alone changes nothing. The policy attached to it does:

- **Budget green:** ship freely. Risk-tolerant releases are encouraged.
- **Budget yellow (50% burned, halfway through window):** slow rollouts, increase canary bake times, defer risky migrations.
- **Budget red (exhausted):** feature freeze. The team's engineering capacity diverts to reliability work until the budget recovers.

This is non-negotiable and pre-agreed. The point is to remove the in-the-moment debate about whether to ship or fix.

## Why this beats "the system should be reliable"

"Reliable" is a statement about feeling. "We have 12 minutes of error budget left in this window" is a statement about reality. The product team can choose to spend it on a risky launch. The SRE team can choose to demand it back. Both sides have skin in the same currency.

When the budget conversation reduces to *what is left*, both teams stop talking past each other. That is the cultural unlock — the metric is secondary.

## Failure modes

- **Setting SLOs after the fact** (matching to current measured reliability): the budget never bites, the policy never activates, the discipline never forms.
- **No policy attached:** the number becomes a dashboard ornament.
- **SLAs > SLOs:** if your customer SLA is tighter than your internal SLO, you have already failed.
- **Aggregate SLOs only:** an availability SLO that's healthy in aggregate while one tenant is at 95% is a metric serving the wrong audience.

## See also

[[README]] · [[Service Outage Response]] · [[10-toil-reduction]] · [[06-cicd-deployment]]
