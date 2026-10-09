title: ISO 27001 Family and Sector Variants
summary: The wider ISO/IEC 27000 family and adjacent ISO standards that extend, refine, or run parallel to 27001.
parent: iso-27001
order: 100
labels: cross-cutting, iso-27001
aliases: ISO 27001 Family | ISO 27000 Family | ISO 27001 Sector Variants | ISO 27001 Adjacent Standards
type: cross-cutting
created: 2026-05-12
updated: 2026-06-08
origin: pillars/iso-27001/ISO 27001 Family and Sector Variants.md
reviewed: no
---
> The wider ISO/IEC 27000 family and adjacent ISO standards that extend, refine, or run parallel to 27001. Plus the non-ISO frameworks that overlap heavily (NIST CSF, SOC 2, PCI DSS, Cyber Essentials, CSA Cloud Controls Matrix). When 27001 is the spine, the family is the rib cage.

## The ISO/IEC 27000 series

### Core / foundational

- **ISO/IEC 27000:2018** — Overview and vocabulary. Free from iso.org. Definitions used across the family.
- **ISO/IEC 27001:2022** — ISMS requirements. The certifiable standard.
- **ISO/IEC 27002:2022** — Information security controls (implementation guidance). The companion handbook to Annex A.

### Implementation and operations

- **ISO/IEC 27003:2017** — ISMS implementation guidance.
- **ISO/IEC 27004:2016** — Monitoring, measurement, analysis and evaluation.
- **ISO/IEC 27005:2022** — Information security risk management. Recommended companion to Cl 6.1.2-6.1.3.
- **ISO/IEC 27007:2020** — Management systems auditing guidelines.
- **ISO/IEC 27008:2019** — Assessment of information security controls.
- **ISO/IEC 27014:2020** — Governance of information security.

### Certification bodies and competence

- **ISO/IEC 27006:2015** + amendments — Requirements for ISO 27001 certification bodies.
- **ISO/IEC 27021:2017** — Competence requirements for ISMS professionals.

### Sector and topic extensions

- **ISO/IEC 27010:2015** — Inter-sector and inter-organizational communications.
- **ISO/IEC 27011:2016** — Telecommunications.
- **ISO/IEC 27017:2015** — Cloud-services controls. Customer-side and provider-side extensions of 27002.
- **ISO/IEC 27018:2019** — PII protection in public clouds acting as PII processors. Complements GDPR Article 28 processor obligations.
- **ISO/IEC 27019:2017** — Energy utility industry process control systems.
- **ISO 27799:2016** — Health informatics.

### Business continuity and resilience

- **ISO/IEC 27031:2011** — ICT readiness for business continuity. Revision in progress.
- **ISO 22301:2019** — Business continuity management systems (sibling to 27001 under Annex SL).

### Incident management and forensics

- **ISO/IEC 27035:2023** (multi-part) — Information security incident management. Part 1 principles, Part 2 plan/prepare, Part 3 ICT incident response, Part 4 coordination.
- **ISO/IEC 27037:2012** — Digital evidence: identification, collection, acquisition, preservation.
- **ISO/IEC 27038:2014** — Redaction of digital information.
- **ISO/IEC 27041:2015** — Investigation suitability assurance.
- **ISO/IEC 27042:2015** — Investigation analysis and interpretation.
- **ISO/IEC 27043:2015** — Investigation principles and processes.

### Storage, networking, application security

- **ISO/IEC 27033** (multi-part) — Network security.
- **ISO/IEC 27034** (multi-part) — Application security.
- **ISO/IEC 27040:2024** — Storage security.

### Supplier relationships

- **ISO/IEC 27036** (multi-part) — Supplier relationships. Part 1 overview, Part 2 requirements, Part 3 ICT supply chain, Part 4 cloud-specific.

### Privacy

- **ISO/IEC 27701:2019** — Privacy Information Management System (PIMS). Extends 27001 / 27002 with privacy-specific requirements. GDPR-aligned.
- **ISO/IEC 29100:2024** — Privacy framework.
- **ISO/IEC 29151:2017** — Code of practice for PII protection.

### AI security and privacy

- **ISO/IEC 42001:2023** — AI management system (AIMS). The 27001-equivalent for AI governance. Certifiable.
- **ISO/IEC 23894:2023** — AI risk management guidance.
- **ISO/IEC 27090** (in development, draft 2025) — AI security.
- **ISO/IEC 27091** (in development, draft 2025) — AI privacy.

## Adjacent non-ISO frameworks

### US-origin

- **NIST Cybersecurity Framework 2.0** (February 2024) — voluntary outcome-oriented framework. Functions: Govern (new in 2.0), Identify, Protect, Detect, Respond, Recover. Maps to ISO 27002:2022 via cyberproperty attribute axis. Non-certifiable. Widely adopted as the implementation reference even in ISO 27001 shops.
- **NIST SP 800-53 Rev. 5** (September 2020 + updates) — federal information systems controls catalogue. Mapping to ISO 27001 / 27002 published by NIST.
- **NIST SP 800-171 Rev. 3** (2024) — protecting CUI in non-federal systems. Required for DoD contractors via CMMC.
- **NIST AI Risk Management Framework 1.0** (January 2023) + Generative AI Profile (July 2024).
- **CMMC 2.0** — Cybersecurity Maturity Model Certification, three levels. US DoD supply chain.
- **SOC 2** (AICPA) — attestation framework with Trust Services Criteria (security, availability, processing integrity, confidentiality, privacy). Type 1 (point-in-time) vs Type 2 (period coverage, typically 6-12 months). US procurement default.
- **HITRUST CSF** — healthcare-origin, broadened. Combines HIPAA, NIST, ISO 27001, PCI DSS, others. US healthcare procurement.
- **FedRAMP** — US federal cloud authorization. Three impact levels.
- **CIS Critical Security Controls v8** (2021) — 18 controls, 153 safeguards. Prescriptive technical baseline. Mapping to ISO 27002 maintained.

### UK / EU origin

- **UK Cyber Essentials / Cyber Essentials Plus** — NCSC. Five technical control areas (firewalls, secure configuration, user access control, malware protection, security update management). Self-assessed (Cyber Essentials) or externally audited (Plus). Common UK government supplier requirement.
- **UK NIS Regulations** (2018) / EU NIS2 Directive (2022/2555) — operators of essential services. Member-state transposition completed late 2024 / early 2025. Enforcement ramping.
- **EU GDPR** (2016/679) — privacy. ISO 27001 + 27701 are common technical-and-organisational measures evidence.
- **EU DORA** (2022/2554) — Digital Operational Resilience Act for financial services. Applicable since 17 January 2025.
- **EU AI Act** (2024/1689) — risk-tiered AI regulation. General-purpose AI obligations from 2 August 2026; high-risk system obligations from 2 August 2027. ISO 42001 alignment likely.
- **EU Cyber Resilience Act** (2024/2847) — digital products cybersecurity, mandatory from late 2027.
- **TISAX** — Trusted Information Security Assessment Exchange. Automotive-sector adaptation of ISO 27001, German-origin (VDA). Required by major German automakers.

### Industry-specific

- **PCI DSS v4.0** (March 2022, mandatory March 2025) — payment card industry. Prescriptive.
- **CSA Cloud Controls Matrix v4** — Cloud Security Alliance. Maps to multiple frameworks. STAR Registry for cloud-provider attestation (3 levels).
- **HIPAA Security Rule** (US healthcare) — administrative, physical, technical safeguards for ePHI.
- **FFIEC** (US financial) — federal regulator cybersecurity guidance.
- **NYDFS 23 NYCRR 500** (NY financial services) — explicit cyber requirements.

### Application / development security

- **OWASP Top 10** — web application security risks.
- **OWASP API Security Top 10** — API-specific risks.
- **OWASP LLM Top 10** (2023, 2024 revision) — LLM-integrated application risks. De facto AI-app-security taxonomy.
- **OWASP ASVS** — application security verification standard.
- **OWASP SAMM** — software assurance maturity model.
- **BSIMM** — Building Security In Maturity Model.
- **MITRE ATT&CK** — adversary tactics and techniques.
- **MITRE D3FEND** — defensive countermeasures.
- **MITRE ATLAS** — adversarial threat landscape for AI systems.
- **SLSA** — Supply-chain Levels for Software Artifacts.

## Mapping crosswalks

Common combinations and where to find mappings:

- **ISO 27001 ↔ NIST CSF 2.0** — ISO/IEC 27002:2022 attribute axis includes NIST CSF function alignment; NIST publishes a crosswalk.
- **ISO 27001 ↔ SOC 2** — published mapping (e.g., AICPA's TSC mapping document, Schellman / A-LIGN combined-audit documentation).
- **ISO 27001 ↔ PCI DSS v4** — PCI Council publishes mappings.
- **ISO 27001 ↔ CIS CSC v8** — CIS-maintained mapping.
- **ISO 27001 ↔ HIPAA** — HITRUST CSF effectively bridges; direct mapping documents exist.
- **ISO 27001 ↔ ISO 42001** — bridge guidance maturing; ISO/IEC JTC 1/SC 42 publishing aligned implementation notes.

Buyer-facing implication: a single set of controls implementation can satisfy multiple frameworks. The audits remain separate; the underlying work overlaps 70-90%. Combined-audit certification bodies (Schellman, A-LIGN, BSI, others) offer single-engagement multi-cert paths.

## Common implementation stacks

Three patterns common in practice:

- **EU SaaS pattern:** ISO 27001 + ISO 27701 + (optional) ISO 27017 + (optional) ISO 27018. GDPR-aligned.
- **US SaaS pattern:** SOC 2 Type 2 + (optional) ISO 27001 + (optional) HIPAA / FedRAMP / state-specific.
- **AI-native pattern (emerging):** ISO 27001 + ISO 42001 + (optional) ISO 27701. AI Act 2026-2027 ramp will accelerate adoption.

## SRE and AI-agent fit notes

- **ISO 42001** is the most relevant adjacent standard for AI-system operators. Sibling structure to 27001 (Annex SL), with AI-specific controls. Combined certification path emerging through 2025-2026.
- **ISO 27017** for cloud-customer responsibilities, especially when relying on cloud-hosted model APIs.
- **ISO 27018** for cloud-PII-processor relationships. Applicable when the org acts as a controller using a vendor as processor.
- **ISO 27036-3** for ICT supply chain — relevant to AI-coding-tool, model-vendor, vector-DB-vendor selection and oversight.
- **MITRE ATLAS** and **OWASP LLM Top 10** as the operational threat taxonomies that flow into ISO 27001 Cl 6.1.2 risk inputs and A.5.7 threat intelligence.

## See also

- [[ISO 27001 Cluster|cluster MOC]] · [[ISO 27001 Certification Process]] · [[ISO 27001 Version History]] · [[ISO 27001 Controversies]]
- [anchors](pillars/iso-27001/anchors.md)
