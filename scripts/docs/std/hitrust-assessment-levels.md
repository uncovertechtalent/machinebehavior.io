title: HITRUST Assessment Levels
summary: For each HITRUST control, mappings.
parent: hitrust
order: 100
labels: framework-concept, hitrust
aliases: HITRUST Assessment Levels | HITRUST e1 i1 r2 | HITRUST Certifications
type: framework-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/hitrust/HITRUST Assessment Levels.md
reviewed: no
---
## Three certification levels

### HITRUST e1 (Essentials, 1-year)

- Entry-level certification.
- ~44 controls.
- 1-year validity.
- Designed for foundational cybersecurity.
- Lower cost.
- Common starting point.

### HITRUST i1 (Implemented, 1-year)

- Intermediate certification.
- ~182 controls.
- 1-year validity with annual reassessment.
- Designed for ongoing maturity demonstration.
- Higher rigor than e1.

### HITRUST r2 (Risk-based, 2-year)

- Comprehensive certification.
- Tailored control set per org's risk profile.
- 2-year validity with interim assessment in year 1.
- Highest rigor.
- Substantial scope.

## Choosing level

- **e1**: minimum-credible-security baseline. Procurement signal entry.
- **i1**: ongoing security maturity. Many US healthcare procurement contexts.
- **r2**: comprehensive risk-based. Larger healthcare orgs, complex environments.

## Multi-authority mapping

For each HITRUST control, mappings to:

- HIPAA Security Rule
- NIST CSF / 800-53
- ISO 27001 / 27002
- PCI DSS
- COBIT
- CIS Controls
- State laws (where mapped)
- Others

Single HITRUST assessment can demonstrate compliance with multiple authorities (with caveats — HITRUST assessment is not a substitute for separate certifications, but provides evidence).

## Assessment process

1. **Scope selection** — entity / system / business unit.
2. **MyCSF setup** — HITRUST-hosted platform.
3. **Control selection** — tailored to scope + level.
4. **Implementation** — control implementation.
5. **Validated assessment** — assessor work.
6. **HITRUST QA review** — quality control.
7. **Certification issuance**.

## External Assessor firms

HITRUST Authorized External Assessors:

- Schellman, A-LIGN, Coalfire — largest volume.
- Big Four — Deloitte, KPMG, PwC, EY.
- Regional firms.

Quality control by HITRUST distinguishes from pure auditor-firm-driven attestations.

## HITRUST AI Security Certification (2024+)

Emerging certification:

- AI-specific controls.
- Combined with i1 or r2.
- Aimed at healthcare AI features primarily; broader applicability.

## Cost

HITRUST among most expensive certification paths:

- e1: typically €25-75k+ first-time.
- i1: €50-150k+ first-time.
- r2: €100-300k+ first-time.
- Plus MyCSF subscription.
- Plus external assessor fees.

Cost-justified primarily by US healthcare procurement signal.

## HITRUST vs ISO 27001

| Aspect | HITRUST | ISO 27001 |
|---|---|---|
| Owner | HITRUST Alliance | ISO/IEC |
| Recognition | US healthcare primary | International |
| Multi-framework | Mapped to many | Standalone |
| Cost | Higher | Lower |
| Validity | 1 or 2 years | 3 years |
| Annual reassessment | Yes | Surveillance audits |
| Multi-authority claim | Yes (with caveats) | No |

## SRE and AI-agent fit notes

For US healthcare AI features:

- HITRUST AI Security Certification emerging signal.
- Combined with i1 or r2 base certification.

For non-healthcare:

- Limited applicability.
- ISO 27001 + SOC 2 typically primary.

## Stefan-context implementation sketch

- Limited relevance outside US healthcare.
- For US healthcare client engagements: HITRUST vocabulary load-bearing.

## See also

- [[HITRUST Cluster|cluster MOC]] · [[HITRUST Controversies]]
- [[ISO 27001 Cluster]] · [[SOC 2 Cluster]]
