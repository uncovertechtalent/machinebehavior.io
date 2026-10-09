title: DORA
summary: Map of Regulation (EU) 2022/2554, the Digital Operational Resilience Act.
parent: index
order: 60
labels: dora, eu-regulation, financial-services-regulation, moc
aliases: DORA Cluster | DORA | Digital Operational Resilience Act | Regulation 2022/2554 | EU 2022/2554
type: MOC
created: 2026-05-12
updated: 2026-06-08
origin: pillars/dora/DORA Cluster.md
reviewed: no
---
> Map of Regulation (EU) 2022/2554 — the Digital Operational Resilience Act. EU's comprehensive financial-services ICT resilience regulation. In force since 17 January 2025. Establishes harmonized requirements for ICT risk management, incident reporting, resilience testing, third-party risk management, information sharing for financial entities and their ICT service providers.

## Anchors

- [position](pillars/dora/position.md): current view, dated, revisable
- [anchors](pillars/dora/anchors.md): primary text, ESAs, oversight bodies, RTS publications

## Provenance

- **Commission proposal** — September 2020 (Digital Finance Package).
- **Trilogue negotiations** — 2021-2022.
- **Adopted** — 14 December 2022.
- **OJEU publication** — 27 December 2022.
- **In force** — 16 January 2023.
- **Applicable** — **17 January 2025** (24-month transition).
- **Regulatory Technical Standards (RTS) and Implementing Technical Standards (ITS)** — published 2023-2024 by ESAs.
- **Live enforcement** — from 17 January 2025; supervisory ramp-up ongoing 2025-2026.

## What DORA is, in one paragraph

DORA is the EU's comprehensive financial-services digital operational resilience regulation. Establishes harmonized requirements across the financial sector for: ICT risk management framework, ICT-related incident management and reporting, digital operational resilience testing including threat-led penetration testing (TLPT), management of ICT third-party risk including critical ICT third-party providers (CTPPs), and information-sharing arrangements. Lex specialis for financial sector vs NIS2 — DORA prevails for financial entities. Applicable since 17 January 2025; supervisory and enforcement infrastructure ramping.

## Scope

Applies to financial entities including:

- Credit institutions
- Payment institutions
- Account information service providers
- Electronic money institutions
- Investment firms
- Crypto-asset service providers (CASPs)
- Issuers of asset-referenced tokens (ARTs)
- Central securities depositories
- Central counterparties
- Trading venues
- Trade repositories
- Managers of alternative investment funds
- Management companies
- Data reporting service providers
- Insurance and reinsurance undertakings
- Insurance intermediaries, reinsurance intermediaries, ancillary insurance intermediaries
- Institutions for occupational retirement provision (IORPs)
- Credit rating agencies
- Administrators of critical benchmarks
- Crowdfunding service providers
- Securitisation repositories

Plus ICT third-party service providers (TPPs) — particularly those designated critical (CTPPs).

Some smaller entities (e.g., small institutions) have proportionality provisions.

## Five pillars of DORA

### Pillar 1: ICT risk management framework (Art 5-15)

Financial entity's responsibility:

- **Governance**: management body responsibility, ICT risk strategy, accountability.
- **ICT risk management framework**: integrated framework covering all aspects.
- **Identification**: identify, classify, document all ICT-supported business functions, information assets, ICT assets, dependencies.
- **Protection and prevention**: appropriate ICT security and resilience measures.
- **Detection**: continuous monitoring and detection of anomalies.
- **Response and recovery**: ICT-related incident response, business continuity, disaster recovery.
- **Learning and evolving**: post-incident reviews, lessons learned, continuous improvement.
- **Communication**: internal and external communication protocols.

Detail in [[DORA ICT Risk Management]].

### Pillar 2: ICT-related incident management, classification, reporting (Art 17-23)

- **Incident management process** (Art 17).
- **Classification** (Art 18): based on impact criteria (clients/financial counterparts affected, reputational impact, duration, geographical spread, data losses, economic impact, criticality of affected services).
- **Reporting timelines** (Art 19): initial notification, intermediate report, final report.
- **Harmonized templates and procedures** via RTS/ITS.
- **Voluntary reporting** of significant cyber threats.

Detail in [[DORA Incident Reporting]].

### Pillar 3: Digital operational resilience testing (Art 24-27)

- **Testing programme** required.
- **Basic testing** for all financial entities: vulnerability assessment, scenario-based tests, end-to-end tests, performance/capacity tests, etc.
- **Advanced testing — TLPT (threat-led penetration testing)** for significant entities. Based on TIBER-EU framework. At least every three years. Mandatory for systemically important entities.
- **Testing of ICT third-party providers** included.

Detail in [[DORA Resilience Testing]].

### Pillar 4: ICT third-party risk management (Art 28-44)

- **General principles** (Art 28-29): entity remains fully responsible regardless of outsourcing.
- **Contractual provisions** (Art 30): mandatory clauses in TPP contracts.
- **Register of information** (Art 28(3)): entity-maintained register of all ICT TPP arrangements.
- **Pre-contractual analysis** (Art 28(7)): risk assessment, due diligence before contract.
- **Concentration risk** (Art 29).
- **Critical ICT third-party providers (CTPPs)** (Art 31-44): designated by ESAs; subject to Union-level oversight.

Detail in [[DORA ICT Third-Party Risk]].

### Pillar 5: Information-sharing arrangements (Art 45)

Voluntary mechanisms enabling financial entities to share cyber threat information, intelligence, indicators of compromise, tactics-techniques-procedures.

## DORA vs NIS2

DORA is **lex specialis** for financial sector vs NIS2. Where DORA addresses a topic, DORA prevails; where DORA is silent, NIS2 may apply to financial entities. In practice: financial entities follow DORA primarily; NIS2 obligations limited.

## Governance and oversight

### ESAs — European Supervisory Authorities

- **EBA** (European Banking Authority)
- **ESMA** (European Securities and Markets Authority)
- **EIOPA** (European Insurance and Occupational Pensions Authority)

Jointly develop RTS/ITS, designate CTPPs, conduct CTPP oversight via Joint Oversight Mechanism.

### National competent authorities

Sector-specific supervisors at Member State level (e.g., BaFin in DE, AMF/ACPR in FR).

### Joint Oversight Mechanism / Lead Overseer

For each CTPP, one ESA designated as Lead Overseer. Conducts ongoing oversight, joint examinations, recommendations.

### Penalties

National competent authorities impose penalties per national law. Member State discretion in penalty calibration. Penalties not limited to fines — can include withdrawal of authorization, restrictions, public statements.

Detail in [[DORA Governance and Penalties]].

## Why this matters for SRE and AI-agent work

- **Financial services clients in scope.** Many SRE consultancies serve financial services; DORA applies broadly.
- **ICT TPP status.** Service providers (cloud, SaaS, MSP, AI/ML providers) supplying financial entities are ICT third-party providers under DORA. Contract clauses, register requirements, potential CTPP designation.
- **TLPT requirements.** Advanced testing creates demand for offensive security capability serving financial entities.
- **Incident reporting infrastructure.** Tight timelines force pre-built response.
- **AI-system inclusion.** AI features in financial-entity ICT systems are part of DORA scope.

## Stefan-context relevance

Stefan-relevant if:

- Financial-services clients (direct or via DE Mittelstand financial-services exposure)
- Cloud / AI vendor positioning serving financial customers
- Cross-border financial-entity work

Cluster atoms should:

- Stay regulation-grounded with article references
- Bridge DORA obligations to ISO 27001 / NIS2 implementation
- Surface RTS/ITS specifics where load-bearing
- Track CTPP designation implications

## Related clusters

- [[ISO 27001 Cluster|ISO 27001]] — substantial control overlap
- [[NIS2 Cluster|NIS2]] — overlapping but DORA lex specialis for financial
- [[GDPR Cluster|GDPR]] — personal data co-applies

## Conventions

- Atoms named `DORA <Topic>.md`
- Article references explicit
- RTS/ITS publications cited where load-bearing
- Cross-link to ISO 27001 / NIS2

## See also

[[DORA Cluster]] (pillars MOC) · [position](pillars/dora/position.md) · [anchors](pillars/dora/anchors.md) · [[ISO 27001 Cluster]] · [[NIS2 Cluster]]
