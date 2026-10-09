title: 3. Observability
summary: "You can't fix what you can't.
parent: pillars
order: 30
aliases: Observability Cluster | SRE Observability Cluster | 03-observability
created: 2026-04-25
updated: 2026-06-08
origin: SRE/pillars/03-observability/README.md
reviewed: no
---
> "You can't fix what you can't see."

## What is Observability?

The ability to understand a system's internal state by examining its external outputs — without deploying new code.

## Three Pillars

### 1. Metrics
Numeric measurements over time:
- **Counters** — Cumulative values (requests_total)
- **Gauges** — Current values (temperature, queue_size)
- **Histograms** — Distribution of values (latency_bucket)
- **Summaries** — Quantiles (p50, p95, p99)

### 2. Logs
Discrete events with context:
- Structured (JSON) > Unstructured
- Include: timestamp, level, service, trace_id, message, context
- Sampling for high-volume services

### 3. Traces
Request flow across services:
- Trace = collection of spans
- Span = single operation with timing
- Propagate context (trace_id, span_id) across services

## Key Concepts

### RED Method (Request-driven)
- **Rate** — Requests per second
- **Errors** — Failed requests per second
- **Duration** — Latency distribution

### USE Method (Resource-driven)
- **Utilization** — % time resource is busy
- **Saturation** — Work queued waiting
- **Errors** — Error count

### Four Golden Signals
1. Latency
2. Traffic
3. Errors
4. Saturation

## Topics

- [ ] Metric naming conventions
- [ ] Cardinality management
- [ ] Log aggregation pipelines
- [ ] Distributed tracing implementation
- [ ] Correlation (metrics ↔ logs ↔ traces)
- [ ] Alerting strategies
- [ ] Dashboard design
- [ ] Runbook integration
- [ ] Cost of observability
- [ ] Sampling strategies

## Alerting

### Good Alerts
- Actionable — Someone needs to do something
- Urgent — It can't wait
- Symptom-based — Users are affected
- Documented — Runbook linked

### Bad Alerts
- Noisy — Fires too often, gets ignored
- Cause-based — CPU high but no user impact
- Ambiguous — What should I do?

### Alert Hierarchy
```
Page (wake someone up)
  → Ticket (fix during business hours)
    → Log (investigate when time permits)
```

## Tools

| Category | Tools |
|----------|-------|
| Metrics | Prometheus, Datadog, CloudWatch |
| Logs | ELK, Loki, Splunk |
| Traces | Jaeger, Tempo, Zipkin, X-Ray |
| Visualization | Grafana, Kibana |
| Alerting | Alertmanager, PagerDuty, Opsgenie |

## Anti-Patterns

- Alert fatigue (too many alerts)
- Vanity metrics (dashboards no one uses)
- High cardinality labels
- Missing context in logs
- No correlation between signals

## Reading

- Google SRE Book: Chapters 6, 10 (Monitoring, Alerting)
- Distributed Systems Observability (O'Reilly)

## Regulatory and control mappings

- [[ISO 27001 Annex A.8 Technological Controls]] A.8.15 Logging. A.8.16 Monitoring activities. A.8.17 Clock synchronization.
- [[NIS2 Security Measures]] Art 21(b) incident handling (detection + logging foundation).
- [[DORA ICT Risk Management]] Art 10 detection.
- [[NIST CSF Core Functions]] DETECT function — continuous monitoring + adverse event analysis.
- [[ITIL 4 Practices]] Monitoring and Event Management.

## People-substrate cross-cluster

Observability has a people-substrate dual: reading what's actually happening in the team (and in yourself) is the same skill as reading what's happening in a system. The three SRE pillars (metrics, logs, traces) map to substrate / apparent / assigned in the developmental-position frame. The trauma filter is the observability bias the operator has to debias against.

- Bridge essay: [[interview-training-psychology-parallels|Interview Training as Applied Clinical Psychology]] -- Item 5 (cognitive distortions = observability bias) + Item 11 (post-interview capture = session-note discipline)
- Developmental-position: [[pillars/developmental-position/Three-Layer Position Model|Three-Layer Position Model]] -- substrate / apparent / assigned is the observability stack for humans; most "observation" stays on apparent
- Developmental-position: [[pillars/developmental-position/The Trauma Filter|The Trauma Filter]] -- the observability bias every operator carries; rubrics + structural defenses are the procedural counter
- Competency: [[self-awareness|Self-Awareness dimension]] -- the operator's own observability stack; without it, all incident signals get filtered through ego-protection
- Psychology: [[pillars/psychology/cognition-and-influence|Cognition and influence]] -- DMN identity decoupling; default-mode network produces noise that masquerades as signal
- Psychology: [[pillars/psychology/amygdala-as-smoke-detector|Amygdala as smoke detector]] -- the legacy alerting layer that fires on pattern-match, not on actual threat; analogous to alert-fatigue mechanism in monitoring

## Atoms

- [[CPU Cache Hierarchy and Speculative Execution]]
- [[Symptoms over Causes for Alerting]]
