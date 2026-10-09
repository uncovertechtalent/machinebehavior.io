title: SOC 2
summary: Map of AICPA SOC 2 attestation framework.
parent: index
order: 100
labels: moc, security-compliance, soc2, us-attestation
aliases: SOC 2 Cluster | SOC 2 | SOC2 | AICPA SOC 2 | Service Organization Controls 2
type: MOC
created: 2026-05-12
updated: 2026-06-08
origin: pillars/soc2/SOC 2 Cluster.md
reviewed: no
---
> Map of AICPA SOC 2 attestation framework. US-origin third-party attestation under SSAE 18 (AT-C section 105). Trust Services Criteria (TSC) covering security, availability, processing integrity, confidentiality, privacy. US enterprise SaaS procurement default. Type 1 (point-in-time) vs Type 2 (period coverage). Reference cluster for US-customer-facing SaaS work and cross-border ISO 27001 + SOC 2 dual implementations.

## Anchors

- [position](pillars/soc2/position.md) · [anchors](pillars/soc2/anchors.md)

## Provenance

- **AICPA** (American Institute of Certified Public Accountants) — US professional accounting body. Develops attestation standards.
- **SAS 70 (1992)** — original third-party assurance standard. Deprecated 2011.
- **SSAE 16 (2011)** + **SOC 1/SOC 2/SOC 3** — restructure. SOC 1 financial reporting; SOC 2 security/operations; SOC 3 public summary version.
- **SSAE 18 (2017)** — current attestation standard.
- **2017 Trust Services Criteria** — current TSC. Revised 2022 with editorial changes.
- **AICPA Auditing Standards Board** — maintains.

## SOC 2 vs SOC 1 vs SOC 3

- **SOC 1**: financial-reporting controls (relevant when service org affects user-entity financial statements).
- **SOC 2**: security / operations controls (TSC categories). Most relevant for SaaS.
- **SOC 3**: public-facing version of SOC 2 (summary, no full controls detail). For marketing.

This cluster focuses on SOC 2.

## Trust Services Criteria (TSC)

Five categories. Security is mandatory; others optional based on org choice.

### Security (Common Criteria, CC)

Mandatory. Nine CC criteria sub-categories:

- CC1: Control Environment
- CC2: Communication and Information
- CC3: Risk Assessment
- CC4: Monitoring Activities
- CC5: Control Activities
- CC6: Logical and Physical Access Controls
- CC7: System Operations
- CC8: Change Management
- CC9: Risk Mitigation

### Availability

Optional. System availability for operation and use as committed or agreed.

### Processing Integrity

Optional. System processing is complete, valid, accurate, timely, authorized.

### Confidentiality

Optional. Information designated as confidential is protected.

### Privacy

Optional. Personal information collected, used, retained, disclosed, disposed in conformity with commitments.

Detail in [[SOC 2 Trust Services Criteria]].

## Type 1 vs Type 2

### Type 1

- Point-in-time attestation.
- Auditor opines on whether controls are suitably designed as of a specific date.
- Faster, less expensive.
- Often first SOC 2 engagement.

### Type 2

- Period attestation (typically 6 or 12 months).
- Auditor opines on whether controls are suitably designed AND operating effectively over the period.
- Substantially more rigorous.
- Procurement-preferred — provides operational-effectiveness evidence.

Detail in [[SOC 2 Type 1 vs Type 2]].

## Engagement mechanics

- Auditor: CPA firm with SOC 2 capability.
- Engagement letter scope: TSC categories, system description, period.
- System description: org's description of services, controls.
- Auditor testing: review controls design (Type 1) + operating effectiveness (Type 2).
- Report contents: management's assertion, system description, auditor opinion.

Detail in [[SOC 2 Assessment Process]].

## SOC 2 vs ISO 27001

| Aspect | SOC 2 | ISO 27001 |
|---|---|---|
| Type | Attestation | Certification |
| Owner | AICPA | ISO/IEC |
| Recognition | US-dominant | International |
| Period | Point-in-time (Type 1) or period (Type 2) | 3-year certificate with annual surveillance |
| Scope | Org-defined system | Org-defined ISMS (SoA) |
| Controls | TSC + supplemental | Annex A + SoA |
| Audit output | Report (not public) + opinion | Public certificate |
| Cost (small SaaS) | €15-50k+ Type 2 first-time | €15-40k+ first-time |
| Renewal | Annual report | 3-year recertification |

Many SaaS companies hold both. Detail in [[SOC 2 vs ISO 27001]].

## Why this matters for SRE and AI-agent work

- **US procurement default.** US enterprise customers commonly require SOC 2 Type 2.
- **AI feature inclusion.** AI features in SOC 2 scope; same TSC criteria apply.
- **Combined audits.** Common combined ISO 27001 + SOC 2 engagements (Schellman, A-LIGN, BSI Americas, others).
- **Vendor due diligence.** SaaS vendors' SOC 2 reports are key vendor-evaluation inputs.

## Related clusters

- [[ISO 27001 Cluster|ISO 27001]] — sibling standard
- [[GDPR Cluster|GDPR]] — Privacy TSC overlap
- [[NIST CSF Cluster|NIST CSF]] — common reference

## See also

[[SOC 2 Cluster]] (pillars MOC) · [position](pillars/soc2/position.md) · [anchors](pillars/soc2/anchors.md) · [[ISO 27001 Cluster]]
