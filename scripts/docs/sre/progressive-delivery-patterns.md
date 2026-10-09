title: Progressive Delivery Patterns
summary: Big-bang deploys treat every release as a coin flip on the entire user base.
parent: cicd-deployment
order: 100
labels: cicd, deployment, pattern, progressive-delivery
aliases: Canary | Blue-Green | Feature Flags | Progressive Delivery
type: pattern
created: 2026-05-04
updated: 2026-05-04
origin: SRE/pillars/06-cicd-deployment/Progressive Delivery Patterns.md
reviewed: no
---
> Big-bang deploys treat every release as a coin flip on the entire user base. Progressive delivery splits the coin flip into many smaller ones with cheap rollback. The right pattern depends on what fails when it fails: a request, a user session, or a database row.

## The four primary patterns

### 1. Blue-green

Two identical environments. Traffic flows to *blue*. Deploy to *green*. Smoke test green. Flip the load balancer. Old version stays warm for instant rollback.

Best for: stateless services, uniform fleets, services with hot caches that must be pre-warmed.
Cost: 2x infrastructure during the deploy window.
Failure mode: stateful changes (DB schema, session storage) break the rollback story.

### 2. Canary

Route N% of traffic to the new version. Watch error rate, latency, and key business metrics. Increase % over a bake period. Roll back at any step if metrics degrade.

Best for: most request-driven services. Default choice unless something rules it out.
Cost: deployment automation that can vary traffic split, observability that can compare canary vs baseline.
Failure mode: low-traffic services don't generate enough signal in the canary window.

### 3. Feature flags

Code ships to all instances. The new behavior is gated by a runtime flag. Roll out by user cohort, geography, or % regardless of deployed version.

Best for: changes whose risk lives in user behavior, not deployment mechanics. A/B tests. Kill-switches for risky integrations.
Cost: flag system as a runtime dependency. Flag-debt: flags that should have been deleted six months ago.
Failure mode: flag explosion. A feature gated by 4 flags is untested in production at the combination level.

### 4. Shadow / dark traffic

New version receives a copy of production traffic. Responses are computed but not returned. Compare new-vs-old responses, latency, error rate.

Best for: high-stakes rewrites, payment systems, anything where the canary's first failure is too expensive.
Cost: traffic-mirroring infrastructure, compute for the shadow tier.
Failure mode: side effects (writes, third-party calls). Shadow only works for read paths or fully-virtualized side effects.

## The decision tree

| Question | If yes |
|---|---|
| Are you changing the database schema? | Blue-green won't save you. Use expand/contract migrations + canary. |
| Is the change behavioral, not mechanical? | Feature flag. |
| Is the cost of the first wrong response unacceptable? | Shadow first, then canary. |
| Are you on Kubernetes with a service mesh? | Canary is cheap; default to it. |
| Do you have <100 RPS at peak? | Canary signal is weak. Use feature flags + slow rollout cohorts. |

## What enables progressive delivery

These are the prerequisites that make any of the above work. Skip one and you have ceremony, not safety:

- **Idempotent deploys.** See [[Idempotence as the IaC Invariant]]. Replays must be safe.
- **Symptom-based alerting** that fires fast on customer impact. See [[Symptoms over Causes for Alerting]].
- **Reliable rollback.** Tested, automated, fast enough that rolling back is the default reflex. See [[Rollback Deployment]].
- **Decoupled DB schema changes.** Expand-then-contract: schema additions backward-compatible with old code, removals only after old code is gone.

## Anti-patterns

- **Canary by deploy environment** ("staging is our canary"). Staging traffic is not production traffic.
- **Manual canary promotion.** Humans gate every step → deploys take days → progressive delivery becomes worse than big-bang.
- **No automatic rollback.** A canary system that requires a human to roll back is a slower big-bang.
- **Flags without expiry.** Every flag needs a removal date. Long-lived flags become permanent forks of behavior.

## See also

[[Rollback Deployment]] · [[Idempotence as the IaC Invariant]] · [[Symptoms over Causes for Alerting]] · [[01-reliability]]
