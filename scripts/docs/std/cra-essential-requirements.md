title: CRA Essential Requirements
summary: Annex I of the CRA establishes essential cybersecurity requirements (Part I) and vulnerability handling requirements (Part II) applicable to products with digital elements.
parent: cyber-resilience-act
order: 100
labels: cyber-resilience-act, regulation-concept
aliases: CRA Essential Requirements | CRA Annex I | CRA Cybersecurity Requirements | CRA Vulnerability Handling
type: regulation-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/cyber-resilience-act/CRA Essential Requirements.md
reviewed: no
---
> Annex I of the CRA establishes essential cybersecurity requirements (Part I) and vulnerability handling requirements (Part II) applicable to products with digital elements.

## Part I: Cybersecurity requirements

### Properties (security by design / default)

- **No known exploitable vulnerabilities** at time of placing on market.
- **Secure default configuration.**
- **Mechanism to recover or reset** in case of incident.
- **Confidentiality protection** for stored, transmitted, processed data.
- **Integrity protection** for stored, transmitted, processed data and configurations.
- **Authentication and identity management** appropriate to risk.
- **Authorization controls** appropriate to risk.
- **Minimize attack surface**.
- **Reduce impact of incidents** including mitigation.
- **Provide security-related information** to user.
- **Log security-relevant events**.
- **Protect against unauthorized access**.
- **Provide security updates**.

Requirements are risk-based and proportional.

### Documentation

Manufacturer maintains technical documentation demonstrating compliance per Annex VII.

## Part II: Vulnerability handling requirements

Throughout product support lifetime:

- **Identify and document** vulnerabilities and components (SBOM).
- **Address vulnerabilities** without delay; security updates as appropriate.
- **Apply effective and regular tests** and reviews.
- **Disclose information** about fixed vulnerabilities once security update available.
- **Have coordinated vulnerability disclosure policy.**
- **Share information** about potential vulnerabilities.
- **Disseminate security updates** effectively.

### SBOM emphasis

Vulnerability identification includes identifying components. Software Bill of Materials (SBOM) is the practical mechanism. Standards (SPDX, CycloneDX) widely used.

### CVD policy

Coordinated vulnerability disclosure policy required:

- Disclosure channel (typically security@ or vendor-specific).
- Acknowledgement timing.
- Remediation timeline.
- Public disclosure approach.

### Support period

Manufacturer commits to support period. Updates provided during support period. Communicated at purchase.

## Conformity assessment procedures

### Default products

Self-assessment (Module A internal control). Manufacturer's declaration of conformity.

### Important products (Annex III)

- Module B (EU-type examination) + Module C (conformity to type) — Annex VI procedures.
- Or full quality assurance Module H — third-party assessment.

### Critical products

Mandatory third-party certification through European cybersecurity certification scheme.

### CE marking

Affixed after successful conformity assessment.

## Reporting obligations (Article 14)

To ENISA:

- **Actively exploited vulnerability**: notification within 24 hours of becoming aware.
- **Severe incident**: notification within 24 hours; further updates per ENISA-specified intervals.

To users:

- Notify users about security updates, especially when actively exploited vulnerability addressed.

To national CSIRTs:

- Cooperation expected.

## Manufacturer obligations

- Cybersecurity requirements compliance.
- Technical documentation maintenance.
- Conformity assessment.
- Declaration of conformity + CE marking.
- Vulnerability handling.
- Support throughout support period.
- Information to user.
- Cooperation with authorities.

## Importer / distributor obligations

- Verify manufacturer compliance.
- Cooperate with market surveillance.
- Cease distribution of non-conforming products.

## Open source carve-out

Open source software not commercially supplied is generally outside CRA scope. Commercial supply pulls in scope. Detailed scoping in regulation:

- Open source contributors not in scope when contributing.
- Commercial entities monetizing open source can be in scope.
- "Open source stewards" (organizations supporting open source) have narrow obligations.

Implementation of open source carve-out is complex; guidance maturing.

## SRE and AI-agent fit notes

### AI-feature software products

AI features integrated into products are part of the product. CRA requirements apply to the integrated whole:

- AI feature vulnerabilities are product vulnerabilities.
- AI feature security updates flow through product support.
- SBOM should identify AI feature components (model versions, libraries).

### AI-specific vulnerabilities

CRA-relevant AI vulnerabilities:

- Prompt injection susceptibility.
- Output handling vulnerabilities.
- Model supply chain compromise.
- Inadequate input validation.

Same content as OWASP LLM Top 10 / ATLAS, integrated into product security context.

## Stefan-context implementation sketch

- For software products: CRA applies if placed on EU market.
- For SRE / consultancy services: out of CRA scope (services not products).
- For clients producing software products: support CRA compliance work.

## See also

- [[Cyber Resilience Act Cluster|cluster MOC]] · [[CRA Controversies]]
- [[NIS2 Cluster]] (operator-side) · [[SLSA SBOM Cluster]] (supply chain)
