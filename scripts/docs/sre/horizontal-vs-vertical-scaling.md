title: Horizontal vs Vertical Scaling
summary: The choice is not "which is better", it is "where does the bottleneck actually live, and which dimension can absorb it." Vertical scaling is bounded by hardware.
parent: scalability
order: 100
labels: capacity-planning, concept, scalability
aliases: Scale Up vs Scale Out | Horizontal Scaling | Vertical Scaling
type: concept
created: 2026-05-04
updated: 2026-05-04
origin: SRE/pillars/02-scalability/Horizontal vs Vertical Scaling.md
reviewed: no
---
> The choice is not "which is better" — it is "where does the bottleneck actually live, and which dimension can absorb it." Vertical scaling is bounded by hardware. Horizontal scaling is bounded by your willingness to engineer for it.

## The two axes

**Vertical (scale up):** bigger box. More CPU, more RAM, faster disk on the same instance. Cheap at small sizes, exponentially expensive at the top end. Caps out at the largest instance type your cloud sells.

**Horizontal (scale out):** more boxes. Linear cost in capacity, no hard ceiling, but every shared resource between the boxes (database, session store, cache) becomes a coordination problem.

The trap: teams scale vertically until the largest instance is exhausted, *then* try to engineer for horizontal scaling under deadline pressure. Sharding a hot database while it's on fire is the classic version.

## When vertical is correct

- Single-writer databases where consistency cost dominates network cost
- Workloads with sub-millisecond inter-component latency requirements (in-memory analytics)
- Stateful systems where the state is too large or too coupled to partition cleanly
- Early-stage products where engineering hours cost more than instance hours

## When horizontal is correct

- Stateless request-handlers (web, API tiers)
- Anything fronted by a load balancer that can do consistent-hash routing
- Read-heavy workloads where read replicas absorb most traffic
- Workloads whose peak is 5x+ their median (autoscaling earns its complexity)
- Anything you cannot afford to take down for a vertical resize

## What actually limits horizontal scaling

It is not "the architecture." It is one of these, almost always:

| Bottleneck | Failure mode |
|---|---|
| Shared database | Connection pool exhaustion, write contention |
| Shared cache | Hot-key thundering herd |
| Sticky sessions | Uneven load, broken failover |
| Centralized config service | Single point of failure for N replicas |
| Cross-replica chatter | Coordination cost grows non-linearly |

Each one is a project to solve. **Horizontal scalability is engineering work paid up-front to buy capacity later.** Vertical scaling is engineering work deferred until the next instance class is impossible.

## The hybrid that wins

Real systems are almost always **N horizontally-scaled stateless tiers in front of a small number of vertically-scaled stateful tiers**. The web tier scales out; the primary database scales up; the read replicas scale out; the analytics warehouse scales up. Knowing which tier is which is the design judgment.

## See also

[[README]] · [[Apple Silicon vs Desktop GPU for Inference]] · [[01-reliability]] · [[07-performance]]
