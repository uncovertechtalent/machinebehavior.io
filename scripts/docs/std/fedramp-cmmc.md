title: FedRAMP CMMC
summary: Two US federal cybersecurity compliance programs.
parent: index
order: 200
labels: fedramp-cmmc, moc, security-compliance, us-federal
aliases: FedRAMP CMMC Cluster | FedRAMP | CMMC | US Federal Cybersecurity Compliance
type: MOC
created: 2026-05-12
updated: 2026-06-08
origin: pillars/fedramp-cmmc/FedRAMP CMMC Cluster.md
reviewed: no
---
# FedRAMP and CMMC Cluster

> Two US federal cybersecurity compliance programs. FedRAMP (Federal Risk and Authorization Management Program) — federal cloud authorization. CMMC (Cybersecurity Maturity Model Certification) — Department of Defense supply chain. Both NIST 800-53 / 800-171-based.

## Anchors

- [position](pillars/fedramp-cmmc/position.md) · [anchors](pillars/fedramp-cmmc/anchors.md)

## Provenance

### FedRAMP

- **Established 2011** by OMB.
- **Joint Authorization Board (JAB)** authorizes high-impact services.
- **Agency Authorizations (A-ATO)** — individual agency authorizations.

### CMMC

- **CMMC 1.0** (2020) — original.
- **CMMC 2.0** (2021) — restructured.
- **DFARS clause** requires CMMC for DoD contractors.
- **Implementation** ramping 2024-2026.

## FedRAMP

### Three impact levels

- **Low** — minor impact.
- **Moderate** — most federal services.
- **High** — sensitive federal services.

### Authorization paths

- **JAB Authorization** — for widely-used services.
- **Agency Authorization (A-ATO)** — agency-specific.

### Process

- 3PAO (Third Party Assessment Organization) assesses.
- Authorization based on NIST 800-53 controls per impact level.
- Continuous monitoring throughout authorization.

### FedRAMP for AI

FedRAMP authorizations apply to AI services. Major cloud AI services obtaining FedRAMP authorization.

## CMMC 2.0

### Three levels

- **Level 1 (Foundational)** — Basic safeguarding of FCI (Federal Contract Information). 17 NIST 800-171 baseline practices. Self-attested.
- **Level 2 (Advanced)** — Protect CUI (Controlled Unclassified Information). NIST 800-171 full ~110 controls. Third-party (C3PAO) assessment for prioritized; self-assess for some.
- **Level 3 (Expert)** — Protect against advanced persistent threats. Additional NIST 800-172 controls. DIBCAC government assessment.

### Implementation

- DFARS 252.204-7012 (existing) + new DFARS 252.204-7021 (CMMC clause).
- CMMC Accreditation Body (CyberAB) administers.
- C3PAO firms conduct Level 2 assessments.
- 5-year validity.

Detail in [[FedRAMP and CMMC Mechanics]].

## Why this matters

- **US federal contracts** require FedRAMP for cloud services.
- **DoD contracts** require CMMC.
- **Procurement-load-bearing** for US federal market.
- **NIST 800-53 / 800-171** technical basis.

## Related clusters

- [[NIST CSF Cluster|NIST CSF]] — related NIST family.
- [[ISO 27001 Cluster|ISO 27001]] — related international.

## See also

[[FedRAMP CMMC Cluster]] (pillars MOC) · [position](pillars/fedramp-cmmc/position.md) · [anchors](pillars/fedramp-cmmc/anchors.md) · [[NIST CSF Cluster]]
