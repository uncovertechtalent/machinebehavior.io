title: Cyber Resilience Act
summary: Map of Regulation (EU) 2024/2847, the Cyber Resilience Act.
parent: index
order: 80
labels: cyber-resilience-act, eu-regulation, moc, product-cybersecurity
aliases: Cyber Resilience Act Cluster | CRA Cluster | EU CRA | Regulation 2024/2847
type: MOC
created: 2026-05-12
updated: 2026-06-08
origin: pillars/cyber-resilience-act/Cyber Resilience Act Cluster.md
reviewed: no
---
# EU Cyber Resilience Act Cluster

> Map of Regulation (EU) 2024/2847 — the Cyber Resilience Act. EU's product cybersecurity regulation. Adopted October 2024; applicable late 2027 for most obligations. Establishes cybersecurity requirements for products with digital elements (PDE) placed on EU market.

## Anchors

- [position](pillars/cyber-resilience-act/position.md) · [anchors](pillars/cyber-resilience-act/anchors.md)

## Provenance

- **Commission proposal** — September 2022.
- **Political agreement** — December 2023.
- **Adopted** — 23 October 2024.
- **OJEU publication** — 20 November 2024.
- **In force** — 10 December 2024.
- **Applicability**:
  - Some provisions from 11 June 2026 (vulnerability reporting).
  - Main obligations from 11 December 2027.

## What CRA is

CRA regulates cybersecurity of products with digital elements (PDE) placed on EU market. Products = hardware + software. Examples: routers, IoT devices, smartphones, software products (OS, applications, libraries), industrial control systems.

Establishes:

- Essential cybersecurity requirements (Annex I).
- Conformity assessment.
- CE marking with cybersecurity context.
- Vulnerability handling and reporting.
- Support period obligations.
- Market surveillance.

## Scope

- **Hardware products** with digital elements.
- **Software products** (standalone software).
- **Products including their data processing**.

Exclusions:

- Medical devices (covered by MDR).
- Automotive products (covered by UN R155 / R156).
- Civil aviation.
- Marine equipment.
- Pure cloud services (SaaS) — separate landscape.
- Open-source software not commercially supplied (with some carve-outs).

## Risk classification

Default products: standard treatment.

**Important products** (Annex III): higher-risk. Specific conformity assessment requirements. Examples include:

- Password managers
- Network management systems
- Identity management systems
- Browsers
- VPNs
- SIEM, microcontrollers with security functions
- Smart home with security functions

**Critical products**: highest risk. Mandatory third-party certification. Examples may include:

- Smart cards
- Hardware security modules
- Smart meters
- Secure crypto-processors

## Essential cybersecurity requirements (Annex I)

Products must be designed, developed, produced to:

- Be made available without known exploitable vulnerabilities.
- Be made available with a secure-by-default configuration.
- Receive security updates when needed.
- Protect availability of essential functions.
- Process only data necessary for the intended use.
- Protect confidentiality and integrity of stored, transmitted, processed data.
- Protect against unauthorized access.
- Provide security information, logging.

Vulnerability handling requirements (Annex I Part II):

- Identify and document vulnerabilities and components.
- Address vulnerabilities without delay.
- Apply effective and regular tests.
- Once a security update is available, share information about fixed vulnerabilities.
- Establish coordinated vulnerability disclosure (CVD) policy.
- Facilitate sharing of information about potential vulnerabilities.
- Provide security updates.
- Disseminate security updates effectively.

Detail in [[CRA Essential Requirements]].

## Support period

Manufacturer must provide security updates throughout product's lifetime (or expected support period, whichever shorter). Support period communicated to user at purchase. Minimum 5 years for many categories.

## Vulnerability reporting (Article 14)

To ENISA:

- **Actively exploited vulnerability**: within 24 hours of awareness.
- **Severe incident**: within 24 hours; intermediate update within 72 hours.

Cooperation with national CSIRTs.

## Conformity assessment

Self-assessment (default products) or third-party (important / critical products). CE marking applied. Annex VI procedures.

## Why this matters for SRE and AI-agent work

- **Software products in scope.** Including AI-feature software products placed on EU market.
- **SBOM emphasis** in vulnerability requirements.
- **Support period commitments** for software products.
- **Vulnerability disclosure** mandatory.
- **AI products specifically** — AI-feature software products + AI models embedded in hardware. AI Act + CRA co-apply.

## Related clusters

- [[NIS2 Cluster|NIS2]] — operator cybersecurity; CRA is product cybersecurity.
- [[EU AI Act Cluster|EU AI Act]] — co-applies for AI products.
- [[ISO 27001 Cluster|ISO 27001]] — manufacturer cybersecurity practices.
- [[SLSA SBOM Cluster|SLSA + SBOM]] — supply chain integrity supports CRA compliance.

## See also

[[Cyber Resilience Act Cluster]] (pillars MOC) · [position](pillars/cyber-resilience-act/position.md) · [anchors](pillars/cyber-resilience-act/anchors.md) · [[NIS2 Cluster]] · [[EU AI Act Cluster]]
