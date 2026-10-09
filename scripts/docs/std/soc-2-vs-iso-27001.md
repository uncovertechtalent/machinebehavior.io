title: SOC 2 vs ISO 27001
summary: SOC 2 (US, AICPA attestation, TSC) and ISO 27001 (international, ISO certification, Annex A) are sibling third-party assurance frameworks with substantial overlap.
parent: soc2
order: 100
labels: cross-cutting, iso-27001, soc2
aliases: SOC 2 vs ISO 27001 | ISO 27001 vs SOC 2 | SOC 2 ISO 27001 Comparison
type: cross-cutting
created: 2026-05-12
updated: 2026-06-08
origin: pillars/soc2/SOC 2 vs ISO 27001.md
reviewed: no
---
> SOC 2 (US, AICPA attestation, TSC) and ISO 27001 (international, ISO certification, Annex A) are sibling third-party assurance frameworks with substantial overlap. Many SaaS organizations hold both for cross-border procurement.

## Side-by-side mechanics

| Aspect | SOC 2 | ISO 27001 |
|---|---|---|
| Type | Attestation | Certification |
| Owner | AICPA (US) | ISO/IEC |
| Auditor | CPA firm | Accredited certification body |
| Audit standard | SSAE 18 | ISO/IEC 17021-1 |
| Recognition | US-dominant | International |
| Output | Report (not public) + opinion | Public certificate |
| Validity | Annual report (no certificate) | 3-year certificate, annual surveillance |
| Period | Point-in-time (Type 1) or period (Type 2) | Continuous |
| Scope | Org-defined system | Org-defined ISMS (SoA) |
| Controls | TSC + supplemental | Annex A + SoA controls |
| Mandatory controls | Security CC | Cl 4-10 + applicable Annex A |
| Customer access | NDA-restricted | Certificate public |
| Cost (small SaaS first-time) | €15-50k+ Type 2 | €15-40k+ first-time |
| Recurring | Annual ~€15-40k Type 2 | Annual surveillance ~€5-12k + recertification |

## Content overlap

Substantial overlap between SOC 2 TSC and ISO 27001 Annex A:

| SOC 2 TSC area | ISO 27001 Annex A |
|---|---|
| CC1 Control Environment | Cl 5 Leadership |
| CC2 Communication | Cl 7.4 + Cl 5.2 |
| CC3 Risk Assessment | Cl 6.1.2 + A.5.7 |
| CC4 Monitoring | Cl 9 + A.8.16 |
| CC5 Control Activities | Various A.5-A.8 |
| CC6 Logical/Physical Access | A.5.15-A.5.18 + A.7 + A.8.5 |
| CC7 System Operations | A.5.24-A.5.28 + A.8 |
| CC8 Change Management | A.8.32 |
| CC9 Risk Mitigation (vendor) | A.5.19-A.5.23 |
| Availability TSC | A.5.30 + ISO 22301 |
| Processing Integrity TSC | A.8.25-A.8.29 |
| Confidentiality TSC | A.5.12-A.5.14 + A.8.24 |
| Privacy TSC | A.5.34 + ISO 27701 |

Coverage estimate: 70-85% control overlap.

## Combined implementation patterns

### Pattern 1: ISO 27001 first, SOC 2 added

Common for EU-origin orgs expanding to US:

1. ISO 27001 in place.
2. Map ISO 27001 implementation to SOC 2 TSC.
3. Identify SOC 2-specific gaps (typically minor).
4. Engage CPA firm for SOC 2 audit.

Time savings: 60-75% of SOC 2 implementation already done.

### Pattern 2: SOC 2 first, ISO 27001 added

Common for US-origin orgs expanding to EU:

1. SOC 2 Type 2 in place.
2. Extend management system to ISO 27001 Cl 4-10.
3. Build SoA covering ISO 27001 Annex A.
4. Engage certification body.

Time savings: 50-70%.

### Pattern 3: Both simultaneously

Greenfield implementations choosing both:

- Single management system covering both standards.
- Combined audits (Schellman, A-LIGN, BSI Americas, Coalfire offer this).
- Cost reduction 20-30% vs separate audits.

## Combined audit infrastructure

Major firms offering combined ISO 27001 + SOC 2 audits:

- **Schellman** — major volume.
- **A-LIGN** — similar.
- **Coalfire** — security-specialist.
- **BSI Americas** — global reach.
- **Big Four** — Deloitte, KPMG, PwC, EY combined practices.

For these firms, ISO 27001 ANAB-accredited certification body status + AICPA CPA firm status both required.

## Why hold both

- **EU procurement**: ISO 27001 preferred.
- **US procurement**: SOC 2 preferred.
- **Combined positioning**: Both signals for cross-border SaaS.
- **Customer questionnaire optimization**: Single response often satisfies both regimes.
- **Vendor due diligence**: Customers may request either or both.

## Recommendation patterns

### Strong recommendation for both

- SaaS serving both US and EU enterprise customers.
- Cross-border AI / data processing.
- Scale where combined-audit cost is justified.

### One or the other

- US-only customer base: SOC 2 sufficient.
- EU-only customer base: ISO 27001 sufficient.
- Cost-constrained: pick by primary customer base.

## What SOC 2 covers that ISO 27001 does not

- **US procurement signal** stronger.
- **Privacy TSC** for US privacy-law (GDPR-comparable, US-state-laws-aligned) audit.
- **Type 1 option** for faster initial assurance.
- **Customer-specific reports** common (customer can request specific TSC categories).

## What ISO 27001 covers that SOC 2 does not

- **Public certificate** usable for marketing.
- **International recognition** broader.
- **3-year cycle** vs annual reports.
- **Standardized SoA** vs flexible TSC scope.
- **Annex A** comprehensive control catalog.
- **Management system framework** more structured.

## Bridging considerations

- **Different reporting cycles**: ISO 27001 annual surveillance + 3-year recertification; SOC 2 annual reports.
- **Different evidence formats**: ISO 27001 audit-trail-driven; SOC 2 system-description + control-test-driven.
- **Audit firm capability**: not all auditors handle both well.
- **Documentation overhead**: managing two sets of evidence; some orgs unify under combined GRC platform.

## SRE and AI-agent fit notes

### Combined evidence for AI features

For an AI feature, evidence supporting both:

- Risk register entries → ISO 27001 risk treatment + SOC 2 CC3.
- Audit logs → ISO 27001 A.8.15 + SOC 2 CC4.1, CC7.2.
- Change records → ISO 27001 A.8.32 + SOC 2 CC8.1.
- Vendor records → ISO 27001 A.5.19-A.5.23 + SOC 2 CC9.

Single evidence package serves both audits.

### AI vendor reports

When evaluating model providers:

- Provider's SOC 2 Type 2 report — request under NDA.
- Provider's ISO 27001 certificate — verify online.
- Provider's ISO 42001 status — emerging.
- Combined evidence package informs vendor due diligence.

## Stefan-context implementation sketch

- Cross-border AI / SaaS work: combined positioning where engagement scale justifies.
- ISO 27001 alignment first (international recognition); SOC 2 layered when US enterprise customer mass warrants.

## See also

- [[SOC 2 Cluster|cluster MOC]] · [[SOC 2 Trust Services Criteria]] · [[SOC 2 Assessment Process]]
- [[ISO 27001 Cluster|ISO 27001]]
