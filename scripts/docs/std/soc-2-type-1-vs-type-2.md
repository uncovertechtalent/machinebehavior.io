title: SOC 2 Type 1 vs Type 2
summary: Two report types differing in scope and rigor.
parent: soc2
order: 100
labels: framework-concept, soc2
aliases: SOC 2 Type 1 vs Type 2 | SOC 2 Types | SOC 2 Type 1 | SOC 2 Type 2
type: framework-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/soc2/SOC 2 Type 1 vs Type 2.md
reviewed: no
---
> Two report types differing in scope and rigor.

## SOC 2 Type 1

### What it covers

Auditor opines on:

- Fairness of management's description of the system.
- Suitability of design of controls to meet applicable TSC at a specific date.

### Time scope

Point-in-time. As of a specific date (e.g., 31 December 2025).

### Effort

- Lower than Type 2.
- Typically 2-3 months from engagement start to report.
- Auditor reviews controls design; does not test operating effectiveness.

### Cost

- For small SaaS: typically €10-25k for Type 1.

### Use case

- First-time SOC 2 engagement.
- Bridge to Type 2 (Type 1 first, then Type 2 covering subsequent period).
- Procurement-readiness when full Type 2 not yet feasible.
- Faster customer satisfaction.

### Limitations

- Does not provide operational-effectiveness evidence.
- Many enterprise customers require Type 2; Type 1 alone insufficient.
- Recently-implemented controls untested for operating reality.

## SOC 2 Type 2

### What it covers

Auditor opines on:

- Fairness of management's description of the system.
- Suitability of design AND operating effectiveness of controls over a period.

### Time scope

Period (review period). Typical periods:

- **3 months** — minimum allowed; bridging period from Type 1.
- **6 months** — interim Type 2.
- **12 months** — standard annual Type 2.

### Effort

- Substantially higher than Type 1.
- Period precedes report — controls must operate before audit.
- Auditor tests samples of control execution over the period.
- Typically 4-8 months elapsed time including period + audit + report.

### Cost

- For small SaaS: typically €15-50k+ for Type 2 first-time.
- Subsequent years often similar or slightly higher.
- Period 1 may cost more than steady state due to first-year discovery.

### Use case

- Procurement-readiness for enterprise customers.
- Annual cycle for ongoing assurance.
- Combined with ISO 27001 for cross-border positioning.

### Operational implications

- Controls must operate consistently over the period.
- Evidence collection ongoing, not just at audit time.
- Control deficiencies during period appear in report.

## Combined Type 1 + Type 2 progression

Typical first-time SOC 2 pattern:

1. **Year 1 H1**: Type 1 report as of mid-year.
2. **Year 1 H2 - Year 2 H1**: Type 2 covering 12-month period.
3. **Year 2+**: annual Type 2 reports.

Or compressed:

1. **Year 1**: Type 1 + bridging Type 2 (3-6 month period).
2. **Year 2+**: annual 12-month Type 2.

## Report contents

### Common contents

- Management assertion
- System description
- Auditor's opinion
- Control descriptions
- Auditor's tests (Type 2 only)
- Results (Type 2 only)
- Other information (optional sections)

### Opinion types

- **Unqualified** — favorable; controls suitably designed (Type 1) or operating effectively (Type 2).
- **Qualified** — favorable with exceptions; specific deficiencies noted.
- **Adverse** — unfavorable; controls insufficient.
- **Disclaimer** — auditor unable to opine.

Procurement-acceptable: unqualified or qualified with minor exceptions.

## Bridging letters

Between annual reports, service orgs sometimes issue bridging letters or interim reports for customers needing assurance for the interim period.

## SRE and AI-agent fit notes

For AI-feature SOC 2 work:

- Type 1 can cover newly-deployed AI features at deployment date.
- Type 2 covers ongoing AI-feature operation over period.
- Period selection affects which AI changes are in scope.

## Stefan-context implementation sketch

- Type 1 first if SOC 2 newly required; Type 2 to follow.
- Typical first-year cost: €15-50k for small/mid-SaaS depending on scope.
- Combined ISO 27001 + SOC 2 engagements reduce per-attestation cost.

## See also

- [[SOC 2 Cluster|cluster MOC]] · [[SOC 2 Trust Services Criteria]] · [[SOC 2 Assessment Process]] · [[SOC 2 vs ISO 27001]]
