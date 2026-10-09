title: PCI DSS
summary: Map of PCI DSS v4.0 (March 2022, mandatory March 2025).
parent: index
order: 180
labels: moc, payment-security, pci-dss
aliases: PCI DSS Cluster | PCI DSS | PCI DSS v4.0 | Payment Card Industry Data Security Standard
type: MOC
created: 2026-05-12
updated: 2026-06-08
origin: pillars/pci-dss/PCI DSS Cluster.md
reviewed: no
---
> Map of PCI DSS v4.0 (March 2022, mandatory March 2025). Payment Card Industry Data Security Standard. Operator: PCI Security Standards Council. Mandatory for entities storing, processing, transmitting cardholder data. Prescriptive control requirements.

## Anchors

- [position](pillars/pci-dss/position.md) · [anchors](pillars/pci-dss/anchors.md)

## Provenance

- **2004**: Visa CISP + similar card-scheme programs.
- **2006**: PCI Security Standards Council established by Visa, Mastercard, Amex, Discover, JCB.
- **PCI DSS v1.0** (2004) — first version.
- Multiple revisions.
- **PCI DSS v4.0** (March 2022) — current. Mandatory March 2025 (v3.2.1 retired).
- **v4.0.1** (June 2024) — minor revision.

## What PCI DSS is

Prescriptive control standard for entities handling cardholder data (CHD) or sensitive authentication data (SAD). Twelve top-level requirements; ~300 specific sub-requirements.

## Twelve top-level requirements

Six control objectives, twelve requirements:

### Build and Maintain a Secure Network and Systems

1. Install and maintain network security controls.
2. Apply secure configurations to all system components.

### Protect Account Data

3. Protect stored account data.
4. Protect cardholder data with strong cryptography during transmission.

### Maintain a Vulnerability Management Program

5. Protect all systems from malicious software.
6. Develop and maintain secure systems and software.

### Implement Strong Access Control Measures

7. Restrict access by business need to know.
8. Identify users and authenticate access.
9. Restrict physical access.

### Regularly Monitor and Test Networks

10. Log and monitor all access.
11. Test security regularly.

### Maintain an Information Security Policy

12. Support information security with organizational policies and programs.

## Compliance validation levels

Four merchant levels based on transaction volume:

- **Level 1**: 6M+ transactions/year. Annual on-site QSA assessment.
- **Level 2**: 1M-6M. Annual SAQ + quarterly ASV scan.
- **Level 3**: 20k-1M e-commerce. Annual SAQ + quarterly ASV scan.
- **Level 4**: <20k e-commerce or <1M total. Annual SAQ.

Service provider levels also exist (Level 1, Level 2).

## SAQ types

Self-Assessment Questionnaire variants for small / mid-market merchants:

- SAQ A: card-not-present, fully outsourced.
- SAQ A-EP: e-commerce, partially outsourced.
- SAQ B: dial-up POS terminals or imprint machines.
- SAQ B-IP: standalone IP-connected POS.
- SAQ C-VT: virtual payment terminals.
- SAQ C: payment app on dedicated system.
- SAQ D: catch-all.
- SAQ P2PE: point-to-point-encrypted solutions.

## v4.0 changes from v3.2.1

- **Customized approach** option allowing alternative implementations meeting intent.
- **Continuous compliance** emphasis.
- **Authentication and password requirements** updated (NIST 800-63B-aligned).
- **Multi-factor authentication** broader.
- **Targeted risk analysis** for some flexible requirements.
- **DESV** (Designated Entities Supplemental Validation) for highest-risk entities.
- **Cloud and modern architecture** more directly addressed.

## QSA — Qualified Security Assessor

Council-approved firms conducting Level 1 assessments. ASV (Approved Scanning Vendor) for quarterly external scans.

## Why this matters for SRE work

- **Merchant / payment processor clients** in scope.
- **SaaS handling cardholder data** in scope.
- **Cloud / SaaS providers** to merchants — service provider responsibilities.
- **AI features touching CHD** in scope.

## Related clusters

- [[ISO 27001 Cluster|ISO 27001]] — overlap on most controls.
- [[SOC 2 Cluster|SOC 2]] — common to hold both.

## See also

[[PCI DSS Cluster]] (pillars MOC) · [position](pillars/pci-dss/position.md) · [anchors](pillars/pci-dss/anchors.md) · [[ISO 27001 Cluster]]
