title: EU AI Act
summary: Map of Regulation (EU) 2024/1689, the EU AI Act.
parent: index
order: 70
labels: ai-governance, ai-regulation, eu-ai-act, eu-regulation, moc
aliases: EU AI Act Cluster | EU AI Act | AI Act | Regulation 2024/1689 | EU 2024/1689
type: MOC
created: 2026-05-12
updated: 2026-10-09
origin: pillars/eu-ai-act/EU AI Act Cluster.md
reviewed: no
---
> Map of Regulation (EU) 2024/1689 — the EU AI Act. World's first comprehensive AI regulation. Risk-tier obligations (unacceptable / high-risk / limited-risk / minimal-risk) plus separate GPAI tier. Staged applicability from 2 February 2025 through 2 August 2027. Reference cluster for regulatory compliance work serving EU markets, EU-based AI providers, and AI deployers using EU-affecting systems.

## Anchors

- [position](pillars/eu-ai-act/position.md): current view, dated, revisable
- [anchors](pillars/eu-ai-act/anchors.md): primary text, AI Office, national authorities, harmonized standards

## Provenance

- **European Commission proposal** — April 2021.
- **Trilogue negotiations** — 2022-2023.
- **Political agreement** — 8 December 2023.
- **European Parliament adoption** — 13 March 2024.
- **Council of EU adoption** — 21 May 2024.
- **Publication in OJEU** — 12 July 2024.
- **In force** — 1 August 2024 (20 days after OJEU publication).
- **Staged applicability** — 2 February 2025 (prohibited practices), 2 August 2025 (GPAI obligations + governance + penalties), 2 August 2026 (general date of application, incl. Art 50 transparency), 2 December 2027 (Annex III high-risk systems) and 2 August 2028 (Annex I product-embedded high-risk systems), as amended by Regulation (EU) 2026/1744 (Digital Omnibus on AI), OJ L 24.7.2026, in force 27 July 2026.

## What the EU AI Act is, in one paragraph

The EU AI Act is a horizontal regulation establishing harmonized rules for AI systems placed on the EU market, put into service in the EU, or whose output is used in the EU. Applies regardless of where the provider is established. Risk-tiered structure: unacceptable-risk AI prohibited; high-risk AI subject to extensive obligations (risk management, data governance, technical documentation, record-keeping, transparency, human oversight, accuracy and robustness, conformity assessment, CE marking); limited-risk AI subject to transparency obligations; minimal-risk AI subject to voluntary codes. Separate rules for general-purpose AI (GPAI) models including a systemic-risk subtier. Governance via European AI Office (Commission) and national competent authorities. Penalties up to €35M or 7% global annual turnover.

## Risk tiers

| Tier | Treatment | Examples |
|---|---|---|
| Unacceptable | Prohibited | Social scoring by public authorities, real-time remote biometric identification in public for law enforcement (with narrow exceptions), exploitation of vulnerabilities, predictive policing based on profiling alone, untargeted scraping of facial images for biometric databases, emotion recognition in workplace / education (with exceptions) |
| High-risk | Extensive obligations | Annex III list (8 areas) + Annex I products (already regulated for safety, with AI components) |
| Limited-risk | Transparency obligations | Chatbots (inform user of AI interaction), deepfakes (label as AI-generated), AI-generated content in journalistic/scientific use (label) |
| Minimal-risk | Voluntary codes | Most AI systems (spam filters, video game AI, basic recommenders) |

Plus **GPAI tier** (cross-cutting):

- **Baseline GPAI**: technical documentation, training data summary, copyright compliance, downstream provider information.
- **GPAI with systemic risk**: additional obligations including model evaluation, adversarial testing, serious incident reporting, cybersecurity protections.

Detail in [[EU AI Act Risk Tiers]].

## Timeline of applicability

| Date | What applies |
|---|---|
| 2024-08-01 | Regulation in force |
| 2025-02-02 | Prohibited practices ban; AI literacy obligation (Art 4) |
| 2025-08-02 | GPAI obligations; governance bodies and notifying authorities operational; penalties applicable |
| 2026-08-02 | General date of application (incl. Art 50 transparency); Art 102 to 110 from 27 July 2026 |
| 2026-12-02 | Added Art 5 prohibitions (Art 5(1)(ba), (bb), (1a), (1b)); Art 111(4) marking grace ends |
| 2027-12-02 | High-risk obligations for Annex III systems (Art 113(c)(i) as amended by Reg. 2026/1744) |
| 2027-08-02 | Pre-existing GPAI models compliant (Art 111(3)) |
| 2028-08-02 | High-risk systems embedded in regulated products (Annex I; Art 113(c)(ii) as amended) |

Pre-existing GPAI models placed on market before 2 August 2025 have until 2 August 2027 to comply.

Detail in [[EU AI Act Timeline]].

## High-risk system obligations (Annex III)

Annex III lists 8 areas considered high-risk:

1. Biometrics (with exceptions for verification and emotion recognition in narrowly-defined contexts)
2. Critical infrastructure (safety components for water, gas, electricity, traffic management, digital infrastructure)
3. Education and vocational training (admissions, evaluation, assessment of personal traits)
4. Employment, workers management, access to self-employment (recruitment, decision-making about employees, monitoring)
5. Access to and enjoyment of essential private and public services (credit scoring, emergency-response dispatch, public assistance)
6. Law enforcement (with restrictions; some prohibited under Title II)
7. Migration, asylum, border control management
8. Administration of justice and democratic processes (judicial decision-support, election influence)

High-risk obligations include:

- Risk management system across the AI system lifecycle
- Data and data governance (training, validation, testing data quality)
- Technical documentation
- Record-keeping (logs)
- Transparency and information for users
- Human oversight
- Accuracy, robustness, and cybersecurity
- Conformity assessment (internal or third-party Notified Body depending on the area)
- CE marking
- Post-market monitoring
- Reporting of serious incidents

Detail in [[EU AI Act High-Risk Obligations]].

## GPAI obligations

Two tiers:

- **Baseline GPAI**: applies to all GPAI models above a capability threshold. Obligations: technical documentation (template provided), training-data summary (template provided), copyright compliance (especially TDM opt-out respect), downstream-provider information enabling their compliance.
- **GPAI with systemic risk**: applies to models meeting capability threshold (currently defined via training compute: 10^25 FLOP). Additional obligations: model evaluation including adversarial testing, serious incident reporting, cybersecurity protections, additional documentation.

Models meeting the threshold notify the Commission; Commission can also designate models as systemic risk based on capability assessment.

Detail in [[EU AI Act GPAI Obligations]].

## Governance and penalties

- **European AI Office** — within Commission DG CNECT. Established 2024. Operates GPAI oversight, harmonized standards process, codes of practice, EU-wide coordination.
- **AI Board** — Member State representatives. Coordinates national-level implementation.
- **Scientific Panel** — independent experts advising on systemic-risk model identification.
- **Advisory Forum** — stakeholder input.
- **National Competent Authorities** — Member State designated bodies (typically split: notifying authority for conformity assessment + market surveillance authority for enforcement).
- **Notified Bodies** — third-party conformity-assessment bodies designated by Member States for high-risk AI categories requiring third-party assessment.

Penalties (Article 99):

- Prohibited practices: up to €35M or 7% global annual turnover (whichever higher).
- Other obligation violations: up to €15M or 3% global annual turnover.
- Supply of incorrect / incomplete / misleading information to authorities: up to €7.5M or 1% global annual turnover.
- SME / startup cap: limited to the lower of fixed amount or percentage.

Detail in [[EU AI Act Governance]].

## Harmonized standards and ISO 42001

The AI Act envisions harmonized standards (under EU standardization framework) that, when complied with, produce a presumption of conformity for high-risk system obligations.

- **CEN-CENELEC JTC 21** — the EU mirror committee to ISO/IEC JTC 1/SC 42. Working on harmonized standards.
- **ISO/IEC 42001 alignment** — likely candidate for harmonization. Process in progress through 2025-2027.
- **Other harmonized standards** under development for specific high-risk-system areas.

Until harmonization completes, providers need to demonstrate compliance against the AI Act requirements directly. Once harmonized, certified ISO 42001 (and other harmonized standards) produces presumption of conformity.

## Why this matters for SRE and AI-agent work

- **Procurement signal hard-edges over 2026-2027.** Customers in EU jurisdictions will require AI Act compliance evidence as enforcement ramps.
- **Provider vs deployer distinction.** Providers (place AI systems on market) and deployers (use AI systems) have different obligations. Many SRE / AI engineering roles span both depending on context.
- **High-risk classification triggers heavy work.** If a system is high-risk, compliance work is substantial. Knowing whether your system is high-risk is foundational.
- **GPAI obligations affect model-provider relationships.** Vendor due diligence increasingly includes AI Act compliance posture.
- **Transparency obligations for limited-risk systems.** Chatbots, deepfakes, AI-generated content all have transparency requirements applicable broadly.
- **AI literacy obligation (Art 4)** — applies broadly to providers and deployers as of 2 February 2025. Light obligation but real.

## Stefan-context relevance

Stefan does SRE / staff-engineer-track work touching:

- AI features potentially in high-risk categories (depends on client / use case)
- GPAI consumption from multiple model providers
- EU-customer-facing AI features (transparency obligations)
- Client engagements where AI Act compliance is procurement-load-bearing
- German Mittelstand customers approaching AI Act enforcement at staggered dates

Cluster atoms should:

- Stay regulation-grounded with citations to specific articles where load-bearing
- Bridge AI Act obligations to ISO 42001 / NIST AI RMF / OWASP LLM Top 10 implementation work
- Surface deployer obligations (not just provider obligations)
- Track timeline-specific applicability for engagement planning

## Related clusters and atoms

- [[ISO 42001 Cluster|ISO 42001]] — likely harmonized standard for AI Act compliance
- [[NIST AI RMF Cluster|NIST AI RMF]] — voluntary framework with crosswalk to AI Act
- [[OWASP LLM Top 10 Cluster|OWASP LLM Top 10]] — operational threats informing risk management
- [[ISO 27001 Cluster|ISO 27001]] — cybersecurity obligations under AI Act overlap with ISO 27001 controls

## Conventions for this cluster

- Atoms named `EU AI Act <Topic>.md` with consistent structure
- Article references cited explicitly (e.g., "Article 6" not "the high-risk classification article")
- Annex references cited explicitly (e.g., "Annex III" for high-risk areas)
- Timeline references use the formal applicability dates (2 February 2025, etc.)
- Cross-link to ISO 42001 / NIST AI RMF / OWASP for implementation depth

## See also

[[EU AI Act Cluster]] (pillars MOC) · [position](pillars/eu-ai-act/position.md) · [anchors](pillars/eu-ai-act/anchors.md) · [[ISO 42001 Cluster]] · [[NIST AI RMF Cluster]] · [[OWASP LLM Top 10 Cluster]]
