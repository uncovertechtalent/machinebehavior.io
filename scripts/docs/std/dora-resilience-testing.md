title: DORA Resilience Testing
summary: Articles 24-27 establish DORA's third pillar: digital operational resilience testing.
parent: dora
order: 100
labels: dora, regulation-concept
aliases: DORA Resilience Testing | DORA Pillar 3 | DORA Articles 24-27 | DORA TLPT | DORA Threat-Led Penetration Testing
type: regulation-concept
created: 2026-05-12
updated: 2026-10-04
origin: pillars/dora/DORA Resilience Testing.md
reviewed: no
---
> Articles 24-27 establish DORA's third pillar: digital operational resilience testing. Two tiers: basic testing for all financial entities; advanced threat-led penetration testing (TLPT) for entities identified by the competent authority. TLPT based on TIBER-EU framework.

## Testing programme (Article 24)

Financial entity establishes comprehensive digital operational resilience testing programme:

- Risk-based.
- Proportionate to size, business, risk profile.
- Conducted at least annually for basic tests.
- Documented, reviewed, updated.

## Basic testing (Article 25)

Mandatory for all financial entities:

- **Vulnerability assessments and scans**
- **Open source analyses**
- **Network security assessments**
- **Gap analyses**
- **Physical security reviews**
- **Questionnaires and scanning software solutions**
- **Source code reviews where feasible**
- **Scenario-based tests** (simulating real-world attacks)
- **Compatibility testing**
- **Performance / capacity testing**
- **End-to-end tests**

Frequency varies by test type and entity risk profile. Annual minimum for full coverage typically.

## Advanced testing — TLPT (Articles 26-27)

Threat-led penetration testing mandatory for financial entities **identified by the competent authority** under Art 26(8) third subparagraph (impact, financial stability, ICT risk profile), at least every 3 years, on live production systems (Art 26(1)-(2)). "Significant" in the text applies only to credit institutions classified significant under the SSM Regulation, which must use external testers only (Art 26(8) second subparagraph). Checked against the OJ text on EUR-Lex 2026-10-03. Based on TIBER-EU framework.

### Eligible entities

Identified based on:

- Systemic importance
- Specific role in financial system
- Specific risk profile
- Other criteria per RTS

### TLPT framework

- **Threat intelligence-led**: based on realistic threat actors targeting the entity.
- **End-to-end**: covers people, processes, technologies.
- **Live production environment**: tested on live systems (with appropriate safeguards).
- **Conducted by accredited testers**: external or internal teams meeting RTS criteria.
- **Coordinated with regulator**: TLPT Authority / National Competent Authority oversight.
- **Confidentiality**: results highly restricted.
- **Periodicity**: at least every three years.
- **Mutual recognition**: TLPT results may be recognized across Member States (RTS).

### Test phases

Typical TLPT lifecycle:

1. **Preparation**: scoping, threat intelligence collection.
2. **Active testing**: red team operations on production.
3. **Close-down**: documentation, remediation planning.
4. **Remediation**: defensive improvements.
5. **Review**: regulator engagement.

### TIBER-EU foundation

TIBER-EU (Threat Intelligence-Based Ethical Red Teaming) framework established 2018 by ECB. DORA TLPT formalizes and harmonizes TIBER-EU into Union-wide obligation. Current version: TIBER-EU Framework, ECB, February 2025 (65 pages), aligned with DORA TLPT and the TLPT RTS, Commission Delegated Regulation (EU) 2025/1190 of 13 February 2025. The May 2018 PDF is marked outdated by the ECB. Checked 2026-10-03.

## Testing of ICT third-party providers (Article 27)

Tests may include the entity's significant ICT third-party providers. Coordination with TPPs:

- TPP cooperation in testing required.
- Contract clauses (Art 30) include testing rights.
- Multi-customer TPPs may be tested jointly across customers.

## Bridge to existing pen-test practice

For entities with existing penetration testing programmes:

- Basic testing aligns with standard vulnerability management.
- TLPT requires uplift to TIBER-EU-style methodology.
- TLPT requires accredited testers (not all penetration testing firms qualified).
- Coordination with national authorities adds process overhead.

## SRE and AI-agent fit notes

### AI features in resilience testing

AI-feature attack surface in testing scope:

- Prompt injection testing.
- Model behavior manipulation.
- Data exfiltration via AI outputs.
- Tool misuse via agent systems.
- Vendor-side dependencies.

Basic testing typically covers AI features. TLPT may include red-team AI-targeted scenarios.

### Test methodology for AI

- OWASP LLM Top 10 as taxonomy.
- MITRE ATLAS for adversarial AI tactics.
- Specialized AI red-team capability emerging.

## Stefan-context implementation sketch

- For financial-services engagements: TLPT services if accredited capability built.
- For non-TLPT scope: standard pen-testing + AI-specific testing services align with DORA basic testing requirements.

## See also

- [[DORA Cluster|cluster MOC]] · [[DORA ICT Risk Management]] · [[DORA Incident Reporting]] · [[DORA ICT Third-Party Risk]]
- [[OWASP LLM Top 10 Cluster]] (AI-specific testing taxonomy)
