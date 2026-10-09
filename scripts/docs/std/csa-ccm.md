title: CSA CCM
summary: Cloud Security Alliance (CSA) Cloud Controls Matrix (CCM).
parent: index
order: 210
labels: cloud-security, csa-ccm, moc
aliases: CSA CCM Cluster | Cloud Controls Matrix | CSA CCM v4 | CCM
type: MOC
created: 2026-05-12
updated: 2026-06-08
origin: pillars/csa-ccm/CSA CCM Cluster.md
reviewed: no
---
# CSA Cloud Controls Matrix Cluster

> Cloud Security Alliance (CSA) Cloud Controls Matrix (CCM). Cloud-specific control framework. Maps to multiple frameworks (ISO 27001, NIST CSF, PCI DSS, HIPAA, others). STAR Registry for cloud-provider attestation.

## Anchors

- [position](pillars/csa-ccm/position.md) · [anchors](pillars/csa-ccm/anchors.md)

## Provenance

- **Cloud Security Alliance** — founded 2008. Non-profit cloud-security industry association.
- **CCM v1** (2010).
- **CCM v3.0 / v3.0.1** (2013-2017).
- **CCM v4** (2021).
- Continuous evolution.

## What CCM is

Cloud-specific control framework. ~200 controls across 17 control domains. Designed for:

- Cloud customer evaluation of providers.
- Cloud provider security implementation.
- Mapping to other frameworks (ISO 27001 / 27017, NIST, PCI, HIPAA).

## Control domains (CCM v4)

1. Audit & Assurance (A&A)
2. Application & Interface Security (AIS)
3. Business Continuity Management & Operational Resilience (BCR)
4. Change Control & Configuration Management (CCC)
5. Cryptography, Encryption & Key Management (CEK)
6. Data Security & Privacy Lifecycle Management (DSP)
7. Datacenter Security (DCS)
8. Governance, Risk & Compliance (GRC)
9. Human Resources (HRS)
10. Identity & Access Management (IAM)
11. Interoperability & Portability (IPY)
12. Infrastructure & Virtualization Security (IVS)
13. Logging & Monitoring (LOG)
14. Security Incident Management, E-Discovery & Cloud Forensics (SEF)
15. Supply Chain Management, Transparency & Accountability (STA)
16. Threat & Vulnerability Management (TVM)
17. Universal Endpoint Management (UEM)

Detail in [[CSA CCM Control Domains]].

## STAR Registry

Cloud Security Alliance Security, Trust, Assurance and Risk (STAR) Registry. Three levels:

- **Level 1 STAR Self-Assessment**: cloud providers submit completed CAIQ (Consensus Assessments Initiative Questionnaire — based on CCM) for public registry.
- **Level 2 STAR Certification**: third-party assessment by approved auditor. ISO 27001 + CCM combined.
- **Level 2 STAR Attestation**: SOC 2 + CCM combined.
- **Level 2 STAR C-STAR**: China-specific.

## Why this matters

- **Cloud provider evaluation**: major cloud providers (AWS, Azure, GCP, others) submit STAR.
- **Cross-framework mapping**: cloud customers can use CCM to map cloud provider posture to their own framework (ISO 27001, etc.).
- **CAIQ questionnaire**: common cloud vendor due-diligence input.

## Related clusters

- [[ISO 27001 Cluster|ISO 27001]] — CCM maps to ISO 27001 (also see ISO 27017).
- [[SOC 2 Cluster|SOC 2]] — STAR Attestation combines.

## See also

[[CSA CCM Cluster]] (pillars MOC) · [position](pillars/csa-ccm/position.md) · [anchors](pillars/csa-ccm/anchors.md) · [[ISO 27001 Cluster]] · [[SOC 2 Cluster]]
