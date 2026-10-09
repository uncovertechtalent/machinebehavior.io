title: 1. Reliability
summary: "Reliability is the most important.
parent: pillars
order: 10
aliases: Reliability Cluster | SRE Reliability Cluster | 01-reliability
created: 2026-04-25
updated: 2026-06-08
origin: SRE/pillars/01-reliability/README.md
reviewed: no
---
> "Reliability is the most important feature."

## What is Reliability?

The ability of a system to perform its intended function under stated conditions for a specified period of time.

## Key Concepts

### Service Level Indicators (SLIs)
Quantitative measures of service behavior:
- **Availability** — % of successful requests
- **Latency** — Response time distribution (p50, p95, p99)
- **Throughput** — Requests per second
- **Error rate** — % of failed requests
- **Freshness** — Data staleness

### Service Level Objectives (SLOs)
Target values for SLIs:
```
Availability SLO: 99.9% of requests successful over 30 days
Latency SLO: p99 < 200ms over 30 days
```

### Service Level Agreements (SLAs)
Contractual commitments with consequences:
- SLA = SLO + Business consequences (refunds, penalties)
- SLAs should be less aggressive than internal SLOs

### Error Budgets
The inverse of reliability — how much failure is allowed:
```
99.9% SLO = 0.1% error budget = 43.2 minutes/month downtime allowed
99.99% SLO = 0.01% error budget = 4.32 minutes/month downtime allowed
```

## Topics

- [ ] Defining meaningful SLIs
- [ ] Setting realistic SLOs
- [ ] Error budget policies
- [ ] Reliability vs. velocity tradeoffs
- [ ] Cascading failures
- [ ] Redundancy and replication
- [ ] Graceful degradation
- [ ] Circuit breakers
- [ ] Retry strategies with backoff
- [ ] Timeouts and deadlines

## Patterns

- N+1 redundancy
- Active-passive failover
- Active-active clustering
- Geographic distribution
- Bulkhead isolation

## Anti-Patterns

- Assuming the network is reliable
- Single points of failure
- Cascading timeouts
- Retry storms
- Unbounded queues

## Tools

| Tool | Purpose |
|------|---------|
| Prometheus | SLI measurement |
| Grafana | SLO dashboards |
| Sloth | SLO generator for Prometheus |
| OpenSLO | Vendor-neutral SLO specification |

## Reading

- Google SRE Book: Chapters 3-4 (Embracing Risk, Service Level Objectives)
- The Site Reliability Workbook: Chapter 2 (Implementing SLOs)

## Regulatory and control mappings

- [[ITIL 4 Practices]] Service Level Management practice.
- [[ISO 27001 Annex A.5 Organizational Controls]] A.5.29-A.5.30 disruption / ICT readiness for BC.
- [[ISO 22301 Clause Structure and Key Concepts]] BIA + RTO + RPO + MBCO discipline.
- [[DORA ICT Risk Management]] Art 11 response and recovery.
- [[NIST CSF Core Functions]] RECOVER function.

## Atoms

- [[Error Budgets as Reliability Currency]]

## People-substrate cross-cluster

Reliability has a people-substrate dual. The leader's regulation under load is an SLI; trauma-substrate adaptations break the same way under-engineered systems break (cascading failure, hero patterns, single points of failure).

- Bridge essay: [[interview-training-psychology-parallels|Interview Training as Applied Clinical Psychology]]
- Psychology: [[pillars/psychology/real-emotional-maturity|Real emotional maturity]] -- the structural reliability property of the operator; performance of maturity is the apparent layer that fails under load
- Psychology: [[pillars/psychology/lack-of-accountability-predicts-relationship-failure|Lack of accountability predicts relationship failure]] -- Gottman empirical anchor; inability to own a mistake is the relational-SLO breach predictor
- Psychology: [[pillars/psychology/nervous-system-regulation-patterns|Nervous-system regulation patterns]] -- dysregulated operator = unreliable response under incident; the regulation layer IS the reliability layer
- Anti-pattern (hero culture): [[pillars/psychology/caretaker-syndrome|Caretaker syndrome]] + [[pillars/psychology/hyper-independence|Hyper-independence]] -- the human SPoF; "I just do it myself" is the same failure pattern as a non-redundant database
- Anti-pattern (SPoF): [[ownership-psychology|Ownership psychology]] over-indexed = the no-redundancy condition the SRE Reliability discipline exists to prevent
