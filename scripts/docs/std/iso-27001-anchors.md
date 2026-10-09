title: ISO 27001 anchors
summary: Primary documents, related standards, named practitioners, and reference resources for the ISO 27001 cluster.
parent: iso-27001
order: 6
labels: anchors, iso-27001
aliases: ISO 27001 Anchors | ISO 27001 Reading List | ISO 27001 Sources
type: anchors
created: 2026-05-12
updated: 2026-05-12
origin: pillars/iso-27001/anchors.md
reviewed: no
---
> Primary documents, related standards, named practitioners, and reference resources for the ISO 27001 cluster. Curated reading list, not exhaustive.

## Primary normative documents

- **ISO/IEC 27001:2022** — Information security, cybersecurity and privacy protection — Information security management systems — Requirements. Published 25 October 2022. Available from iso.org (CHF 124 / ~€130 single-user PDF) and national standards bodies (BSI for UK, DIN for DE, ANSI for US — typically national-currency equivalent with local annexes).
- **ISO/IEC 27002:2022** — Information security, cybersecurity and privacy protection — Information security controls. Published February 2022. The control implementation handbook. Necessary companion to 27001.
- **ISO/IEC 27000:2018** — Vocabulary. Free download from iso.org/standard/73906.html. Defines terms used across the 27000 family.
- **ISO/IEC 17021-1:2015** — Conformity assessment — Requirements for bodies providing audit and certification of management systems. Governs the certification bodies.
- **ISO/IEC 27006:2015 + amendments** — Requirements specific to ISO 27001 certification bodies.

## Implementation-side standards

- **ISO/IEC 27003:2017** — ISMS implementation guidance.
- **ISO/IEC 27004:2016** — Monitoring, measurement, analysis, and evaluation. Companion to Cl 9.1.
- **ISO/IEC 27005:2022** — Information security risk management. Companion to Cl 6.1.2-6.1.3.
- **ISO/IEC 27007:2020** — Management systems auditing.
- **ISO/IEC 27014:2020** — Governance of information security.

## Sector and topic extensions (27k family)

- **ISO/IEC 27017:2015** — Cloud security controls (cloud service customer and provider).
- **ISO/IEC 27018:2019** — Protection of PII in public clouds acting as PII processors.
- **ISO/IEC 27019:2017** — Energy utility industry.
- **ISO/IEC 27031:2011** — ICT readiness for business continuity (rev in progress).
- **ISO/IEC 27034:2011-2018** — Application security (multi-part).
- **ISO/IEC 27035:2023** — Incident management (multi-part: 1 principles, 2 plan/prepare, 3 ICT incident response, 4 coordination).
- **ISO/IEC 27036:2014-2022** — Supplier relationships (multi-part).
- **ISO/IEC 27037:2012** — Digital evidence identification, collection, acquisition, preservation.
- **ISO/IEC 27040:2024** — Storage security.
- **ISO/IEC 27701:2019** — Privacy information management (PIMS), extends 27001 / 27002 for GDPR / privacy.
- **ISO/IEC 42001:2023** — AI management system (AIMS). Sibling standard to 27001 for AI-system governance.

## Related but non-ISO frameworks

- **NIST Cybersecurity Framework 2.0** (February 2024) — voluntary US framework. Functions: Govern, Identify, Protect, Detect, Respond, Recover. Maps to ISO 27002:2022 via the cyberproperty attribute axis.
- **NIST SP 800-53 Rev. 5** (September 2020 + updates) — federal information system controls; mapping to ISO 27002 published by NIST.
- **NIST AI Risk Management Framework 1.0** (January 2023) + Generative AI Profile (July 2024).
- **CIS Critical Security Controls v8** (2021) — prioritized 18 controls and 153 safeguards. Mapping to ISO 27002 maintained by CIS.
- **AICPA SOC 2 Trust Services Criteria** (2017, revised 2022) — US attestation framework.
- **PCI DSS v4.0** (March 2022, mandatory March 2025) — payment card industry data security.
- **UK Cyber Essentials / Cyber Essentials Plus** (NCSC) — entry-level UK framework.
- **CSA Cloud Controls Matrix v4** — cloud-specific, maps to multiple frameworks.
- **OWASP LLM Top 10** (2023, 2024 revision) — application-security taxonomy for LLM-integrated systems.
- **MITRE ATT&CK / D3FEND** — adversary tactics and defensive countermeasures, useful for risk assessment input under Cl 6.1.2.
- **MITRE ATLAS** — adversarial threat landscape for AI systems.

## Regulatory and procurement-driver context

- **EU GDPR (Reg 2016/679)** — privacy regulation. ISO 27001 + 27701 widely used as defensible technical-and-organisational-measures evidence.
- **EU NIS2 Directive (Dir 2022/2555)** — cybersecurity for essential and important entities. Member-state transposition deadlines 17 October 2024; enforcement ramping through 2025-2026. ISO 27001 alignment is a common path.
- **EU AI Act (Reg 2024/1689)** — general provisions in force August 2024; high-risk system obligations from 2 August 2026 (general-purpose AI) and 2 August 2027 (most high-risk). ISO 42001 + ISO 27001 will be the implementation default.
- **EU DORA (Reg 2022/2554)** — Digital Operational Resilience Act for financial services. In force 17 January 2025. ICT third-party risk management overlaps with ISO 27001 A.5.19-23 / A.8.
- **EU Cyber Resilience Act (Reg 2024/2847)** — product cybersecurity for digital products. Adopted October 2024, applicable late 2027.
- **UK Data Protection Act 2018** + GDPR-equivalent post-Brexit framework.
- **US state privacy laws** — CCPA / CPRA (CA), VCDPA (VA), CPA (CO), CTDPA (CT), UCPA (UT), and the 2024-2025 wave (TX, OR, MT, DE, NH, NJ, MD, others).

## Certification bodies (accredited)

UKAS-accredited (UK) and equivalent national accreditation in DE (DAkkS), US (ANAB), and elsewhere:

- **BSI Group** — UK origin, global. Publisher of BS 7799 lineage. Volume leader in UK / EMEA.
- **DNV** — Norwegian origin, global. Strong in energy, maritime, manufacturing.
- **TÜV SÜD, TÜV Rheinland, TÜV Nord** — German technical inspection bodies, dominant in DE Mittelstand certification.
- **LRQA (formerly Lloyd's Register Quality Assurance)** — global.
- **SGS** — Swiss, global. Largest by volume worldwide.
- **Bureau Veritas (BV)** — French, global.
- **Schellman** — US-origin, growing internationally. Cross-certified for ISO 27001 + SOC 2.
- **A-LIGN** — US-origin, similar combined-audit positioning.
- **Coalfire** — US-origin, security-specialist.
- **ISACA-affiliated bodies** — varying by region.

Accreditation status is checkable via the certification body's listing on UKAS, DAkkS, ANAB, IAS, or the IAF (International Accreditation Forum) member directory.

## Named practitioners and reference voices

### Standards and audit

- **Edward Humphreys** — convenor of the ISO/IEC JTC 1/SC 27/WG 1 (the ISMS working group) for decades; longtime "Mr ISMS." His writing on 27001 evolution is the closest thing to canon.
- **Alan Calder** — IT Governance Ltd founder. Practitioner books on ISO 27001 implementation (UK angle). Useful at the start of an implementation, less so for advanced practice.
- **Steve Watkins** — IT Governance co-author; auditor perspective.

### Risk and threat

- **Jack Jones** — FAIR (Factor Analysis of Information Risk) creator. Quantitative risk model that complements Cl 6.1.2's qualitative default.
- **Daniel Miessler** — practitioner-side commentary on real-world security maturity vs compliance theatre.

### Cloud and modern infrastructure

- **The CSA (Cloud Security Alliance) Star Registry team** — Cloud Controls Matrix maintenance.
- **Erica Toelle, Andrew Plato, others** — practitioner writing on cloud-native security and ISO 27017 alignment.

### AI / agent systems

- **Ram Shankar Siva Kumar** — MITRE ATLAS, AI threat modelling.
- **Andrej Karpathy, Simon Willison** — practitioner writing on LLM security, prompt injection (Willison coined the term).
- **NIST AI Safety Institute team** — ongoing work on the GenAI profile for the AI RMF.

### Critical voices

- **Bruce Schneier** — long-running critique of compliance theatre vs real security. The position atom's "compliance ≠ security" position draws on this lineage.
- **Adam Shostack** — threat modelling discipline; argues for threat-model-driven security over control-list-driven security.

## Reference resources

- **iso.org** — official publisher; CHF-priced PDFs.
- **bsigroup.com** — BSI Knowledge subscription model for UK/EMEA users.
- **NIST CSRC** (csrc.nist.gov) — free NIST publications; mappings to ISO.
- **enisa.europa.eu** — EU agency for cybersecurity; threat-landscape reports useful for Cl 6.1.2 input.
- **iaf.nu** — International Accreditation Forum directory for verifying certification body accreditation.

## See also

- [[ISO 27001 Cluster|cluster MOC]] · [position](pillars/iso-27001/position.md)
