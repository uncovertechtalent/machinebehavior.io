title: ISO 27001 position
summary: Current view on what ISO/IEC 27001:2022 is good for, what it is not good for, and where the standard sits relative to actual security work.
parent: iso-27001
order: 5
labels: iso-27001, position
aliases: ISO 27001 Position | ISO 27001 Current View
type: position
created: 2026-05-12
updated: 2026-05-12
origin: pillars/iso-27001/position.md
reviewed: no
---
> Current view on what ISO/IEC 27001:2022 is good for, what it is not good for, and where the standard sits relative to actual security work. Dated, revisable, diff-tracked.

## State of the view as of 2026-05-12

### What ISO 27001:2022 does well

- **Forces management commitment.** Clause 5.1 ("top management shall demonstrate leadership and commitment") and the documented scope of the ISMS make security a board-level artefact, not just an engineering team's side concern. Procurement-readiness benefits flow from this regardless of the security underneath.
- **Risk-based, not control-prescriptive.** Cl 6.1.2 requires a risk-assessment process; Annex A is a reference list. The org picks controls via the Statement of Applicability. Avoids the PCI DSS rigidity problem.
- **Annex SL harmonized structure** shared with ISO 9001 (quality), 14001 (environmental), 22301 (BC), 27701 (privacy). Multi-standard implementations share the management-system layer.
- **Annex A:2022 modernization landed.** Cloud services (A.5.23), threat intelligence (A.5.7), ICT readiness for BC (A.5.30), configuration management (A.8.9), information deletion (A.8.10), data masking (A.8.11), DLP (A.8.12), web filtering (A.8.23), secure coding (A.8.28) close real 2013-era gaps.
- **Internationally recognized.** ISO 27001 certificates are accepted in EU/UK procurement, German Mittelstand RFPs, Asia-Pacific tenders. Single-audit, multi-customer evidence reduces the questionnaire burden materially.
- **Attribute axes in 27002:2022** (control type, CIA, NIST CSF function, operational capability, security domain) allow filtering for risk-driven implementation rather than wholesale adoption.

### What ISO 27001:2022 does poorly

- **Checkbox-compliance failure mode is endemic.** "We have a policy" replaces "the control works." Field experience and breach post-mortems repeatedly show certified orgs failing on the controls they were certified against. Field-trial-style reliability data does not exist for ISO 27001 the way it does for DSM-5; the certification body is the only feedback loop and it is paid by the auditee.
- **Statement of Applicability scope-narrowing.** Orgs draw the ISMS scope around the part of the business they want certified (often just the SaaS production environment, excluding HR, finance, corporate IT) and exclude inconvenient controls as "not applicable." The certificate then over-claims coverage from a buyer's perspective.
- **Auditor variance is high.** Inter-auditor reliability is not measured publicly. Two auditors against the same evidence routinely reach different findings. Auditor-shopping is a documented practice ("we'll get easier auditors next cycle").
- **AI-system fit gaps are unaddressed.** :2022 closed cloud and DLP gaps, then the AI-agent shift arrived. Prompt injection, model-supply-chain compromise, agent-generated audit-log fidelity, autonomous-agent SoD breakdowns, and the model-vendor-as-implicit-data-processor relationship are not covered in current Annex A controls. ISO/IEC 42001:2023 (AI management system) is the partial answer, but the integration story with 27001 is immature.
- **Document-heavy.** Clauses 7.5 (documented information) and 9 (performance evaluation, internal audit, management review) generate large evidence demands. Lean orgs end up either failing or growing a compliance function that does not produce security.
- **Slow update cycle.** :2013 to :2022 took nine years. Threat landscape moves in months. By the time a new control type makes it into Annex A, the threat has matured into specialized standards (e.g., supply-chain attacks → SLSA, agent risks → ISO 42001 / OWASP LLM Top 10).
- **Cost gating.** Certification costs scale with scope and headcount: a small SaaS company typically pays €15-40k for first-time certification (Stage 1 + Stage 2 + first surveillance), plus internal effort of 6-12 person-months for first-pass implementation. Smaller orgs end up doing Cyber Essentials Plus or SOC 2 Type 1 instead and losing on enterprise RFPs.

### Where the evidence currently sits

- **Compliance ≠ security.** Documented in every major breach analysis since the 2013 Target breach (PCI-compliant at time of breach), through 2017 Equifax (was certified, lost 147M records to an unpatched Struts vulnerability), through 2024 Change Healthcare (ISO 27001 certified, RaaS encrypted 25% of all US health claims for weeks). The certificate does not predict breach absence.
- **ISO 27001 + SOC 2 is the de facto enterprise SaaS baseline.** EU buyers favour ISO 27001, US buyers favour SOC 2 Type 2. Most companies selling into both run both. The audit-cycle effort overlaps significantly with good engineering hygiene.
- **AI / ML system coverage is in flux.** ISO/IEC 42001:2023 published December 2023. ISO/IEC 27090 (AI security) and 27091 (AI privacy) in draft. NIST AI RMF (2023) provides outcome-oriented framing. The OWASP LLM Top 10 (2023, updated 2024) is the de facto technical taxonomy. ISO 27001 evidence packages for AI features currently borrow from all of these.
- **NIST CSF 2.0 (February 2024)** added Govern as a sixth function and is increasingly the implementation reference even for ISO 27001 shops. ISO 27002:2022 attribute axis includes NIST CSF mapping explicitly.
- **Privacy regulation pressure is real.** EU GDPR enforcement (Meta €1.2B fine 2023, Amazon €746M 2021, others sustained) pushes orgs toward ISO 27701 PIMS certification on top of 27001. UK Data Protection Act 2018, US state laws (CCPA, CPRA, the various 2024-2025 state laws), and the EU AI Act (Reg 2024/1689) compound the procurement-questionnaire load.
- **Certification-body market is consolidating.** BSI, DNV, TÜV SÜD, LRQA, SGS, BV, Schellman, ISACA-affiliated bodies hold most of the volume. Accreditation under ISO/IEC 17021-1 via UKAS, DAkkS, ANAB, and equivalents is the only consistency mechanism. Bottom-of-market certificates from unaccredited bodies exist and are detectable in buyer due diligence.

## Personal calibration

- **Working assumption for SRE / AI-agent design**: implement the relevant Annex A controls as actual operational behavior first. Treat the SoA as documentation of what exists, not a forward-looking commitment. Reverse audits ("does the control we claim actually work?") catch the drift.
- **Working assumption for procurement readiness**: a credible-looking ISO 27001 cert + a clean SoA + responsive answers to follow-up questionnaire items closes most German Mittelstand and UK enterprise procurement. The cert is necessary, not sufficient.
- **Working assumption for AI-agent compliance**: write the controls that should exist (input validation against prompt injection, audit-log integrity around agent decisions, vendor due diligence on model providers, kill-switch and reversibility on agent actions) and document them as company-specific extensions of A.5.7 (threat intelligence), A.5.23 (cloud), A.8.16 (monitoring), A.8.28 (secure coding). Migrate to ISO/IEC 42001 cert when the buyer signal warrants the second audit cycle.
- **Working assumption for the vault and personal infra**: ISO 27001 is conceptual scaffolding, not an implementation target for a one-person system. Use the clause structure to organize thinking; do not invent the management overhead of certification for personal work.

## What would shift this view

- **Field-trial reliability data on certification audits.** If credible kappa-style data emerged on auditor agreement across the same evidence, the certification signal would either get sharper or visibly collapse.
- **ISO 42001 + ISO 27001 integration guidance.** When the bridge document arrives, AI-system buyers will start asking specifically for both; the time-to-implementation will compress.
- **A widely-publicized breach of an ISO 27001 certified AI-system vendor.** This will move the buyer signal from "has cert" to "has cert plus specific agent-security evidence" within 12-18 months of the event.
- **EU AI Act enforcement** (full applicability 2 August 2026 for general-purpose AI, 2 August 2027 for most high-risk systems). High-risk classification will force documented AI risk management; ISO 27001 + 42001 will be the path of least resistance.

## See also

- [[ISO 27001 Cluster|cluster MOC]] · [[ISO 27001 Controversies]] · [[ISO 27001 Family and Sector Variants]]
- [anchors](pillars/iso-27001/anchors.md)
