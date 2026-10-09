title: ISO 42001 Certification Process
summary: End-to-end mechanics for ISO/IEC 42001:2023 certification.
parent: iso-42001
order: 100
labels: cross-cutting, iso-42001
aliases: ISO 42001 Certification | ISO 42001 Audit Process | AIMS Certification
type: cross-cutting
created: 2026-05-12
updated: 2026-06-08
origin: pillars/iso-42001/ISO 42001 Certification Process.md
reviewed: no
---
> End-to-end mechanics for ISO/IEC 42001:2023 certification. Same Annex SL mechanics as ISO 27001 — Stage 1 + Stage 2 audits, annual surveillance, three-year recertification. Audit-practice maturity is still early (certification bodies started offering audits late 2024 / early 2025), so this atom emphasizes current state and emerging conventions rather than settled practice.

## Implementation timeline (first-time certification)

For an org without prior ISO management-system certification:

- **Months 0-2**: scope decision, gap analysis against ISO 42001:2023, methodology selection.
- **Months 2-6**: AI policy development, AI risk methodology, AI system inventory, role assignment, impact assessment process design, control implementation work.
- **Months 6-9**: initial AI risk assessment, AI system impact assessments, SoA production, control implementation completion, training rollout, evidence base buildup.
- **Months 9-10**: internal audit dry run.
- **Month 10**: management review.
- **Months 10-11**: Stage 1 audit.
- **Months 11-13**: Stage 2 audit. Certification decision.

For an org already certified to ISO 27001:

- Implementation overlap reduces timeline by 30-50%.
- Combined audit option compresses external-audit timeline.

Realistic ranges: 6-12 months for ISO 27001-mature orgs adding ISO 42001, 12-18 months for orgs implementing both simultaneously without prior certifications.

## The four-audit cycle

Identical to ISO 27001:

- **Year 1**: Stage 1 + Stage 2 = initial certification.
- **Year 2**: Surveillance audit 1.
- **Year 3**: Surveillance audit 2.
- **Year 4**: Recertification audit.

Findings categorized as major nonconformity (blocks certification), minor nonconformity (must be addressed within agreed window), observation / opportunity (non-binding feedback).

## Stage 1 audit

Documentation and readiness review. Auditor checks:

- AIMS scope documented.
- AI policy in place.
- AI risk methodology defined.
- AI risk register populated.
- SoA produced with Annex A coverage.
- AI system inventory in place.
- AI system impact assessments performed for in-scope systems.
- Internal audit programme planned.
- At least one management review held.
- Basic control implementations evidenced.

Outcome: ready for Stage 2 or recommendations for further work.

## Stage 2 audit

Full implementation audit:

- Document review (continued).
- Interviews with top management, AI leadership, AI system owners, AI risk owners, control owners, sampled staff.
- Evidence sampling: AI policy communication evidence, training records, impact assessment records, risk treatment records, vendor management records, audit logs, incident records.
- Walkthroughs of critical processes: impact assessment process, risk treatment process, change management for AI systems, incident response for AI-related incidents.
- AI system reviews: sample of in-scope AI systems with full lifecycle evidence.

Outcome: certification decision. Major nonconformities block certification until remediated.

## Audit-practice maturity (current state, 2026)

Certification bodies started offering ISO 42001 audits in late 2024 / early 2025. Current maturity:

- **First-year auditors**: trained in ISO 42001 fundamentals and Annex A. Variable AI-domain experience.
- **AI-domain depth**: variable. Auditors with prior ML / data-science / AI-engineering background bring depth; others rely on the framework structure.
- **Common findings**: AI policy generic, impact assessment treated as one-shot, AI system inventory incomplete, vendor relationship evidence thin, lifecycle-stage tracking missing.
- **Combined audits**: ISO 27001 + ISO 42001 combined audits common; auditors handle both standards in single engagement.
- **Inter-auditor variance**: high in early state. Expected to converge as audit-practice matures through 2025-2027.

Implication for buyers: an ISO 42001 certificate issued in 2025-2026 carries less convergent meaning than a mature ISO 27001 certificate. Buyers asking for the SoA and the audit report (where supplier willing to share bilaterally) get more substance than the certificate alone.

Implication for implementers: choosing a certification body with strong AI-domain auditing capability matters more in early state than it will in 2028+ when audit practice has matured.

## Accreditation chain

Standard ISO mechanics:

- **IAF** coordinator.
- **Accreditation bodies** (UKAS, DAkkS, ANAB, others) accredit certification bodies under ISO/IEC 17021-1.
- **ISO/IEC 42006** (in development) — will formalize the AIMS-specific certification body requirements. Until 42006 publishes, accreditation under 17021-1 is the baseline.

Buyer-side verification: certificate names the certification body; accreditation status verifiable via the accreditation body. Unaccredited certificates exist and are detectable in buyer due diligence.

## Certification body selection

Selection criteria for ISO 42001 specifically:

- **Accreditation confirmation** for the AIMS scope. Confirm via accreditation body website.
- **AI-domain audit experience**: ask about auditor backgrounds. Senior auditors with ML / data-science / AI-engineering background are scarce; firms with AI-domain leads in their audit practice carry depth.
- **Combined-cert capability**: ISO 27001 + ISO 42001 combined audits reduce overhead. Some bodies also offer ISO 27701 combined for three-way.
- **Sector experience**: AI-feature SaaS, regulated industries, AI-product companies all have specific concerns; ask about prior similar customers.
- **EU AI Act preparation**: certification bodies tracking the AI Act harmonization process closely will be positioned to handle the harmonized-standard auditing once formal.

Common bodies with early ISO 42001 capability:

- **BSI Group** — UK origin; published ISO 42001 readiness content early.
- **DNV** — strong in maritime, energy; AIMS capability building.
- **TÜV Süd** — German technical inspection; combined offerings with ISO 27001.
- **LRQA** — global; combined offerings.
- **Schellman** — US-origin; combined SOC 2 + ISO 27001 + ISO 42001 positioning.
- **A-LIGN** — US-origin; similar combined.
- **PECB** — emerging.

## Cost orientation

For a 50-300 person AI-feature SaaS company:

- **First-time ISO 42001 alone**: €10-25k for Stage 1 + Stage 2 + first surveillance. Plus consultant support if used. Plus 4-8 person-months of internal effort.
- **Combined ISO 27001 + ISO 42001 first-time**: €25-50k vs ~€30-65k separate. Combined-audit savings real.
- **Annual surveillance ISO 42001**: €4-8k each.
- **Recertification ISO 42001**: €10-20k.

Costs likely to rise as audit-practice matures and demand outpaces auditor supply through 2026-2027.

## Common procedural pitfalls

- **Treating ISO 42001 as ISO 27001 plus Annex A bolt-on.** Impact assessment, lifecycle, vendor relationships need genuine treatment.
- **AI system inventory underestimated.** Often missed early; foundational to risk and impact work.
- **Generic AI policy.** Boilerplate "trustworthy AI" language without org-specific commitments.
- **Impact assessment as one-shot.** Cl 8.4 expects ongoing impact assessment, especially at significant changes.
- **Vendor evidence thin.** A.10 third-party controls expect substantive due diligence and ongoing monitoring of model providers.
- **Selecting auditor without AI-domain capability check.** Early-stage auditor variance produces uneven audit experiences. Worth asking about auditor backgrounds.
- **EU AI Act timing misalignment.** Some orgs pursuing ISO 42001 before AI Act enforcement applies to them; useful procurement signal but may not directly satisfy AI Act compliance until harmonization completes.

## Path for small / solo operations

Same considerations as ISO 27001 cost-gating:

- **Small AI-product companies** may struggle with ISO 42001 cost. Cyber Essentials Plus equivalent for AI doesn't exist yet.
- **NIST AI RMF alignment** (voluntary, non-certified) is the lighter alternative for orgs not yet warranting cert.
- **Combined cert when revenue justifies** — typically when AI-feature procurement signal exceeds cert cost with margin.
- **For solo / small-team consulting**: cert not warranted. Implement aligned to ISO 42001 structure, maintain evidence, present client-by-client when engagement requires.

## SRE and AI-agent fit summary

The certification process is largely standard ISO mechanics; the AI-specific concerns are in implementation and evidence content rather than process mechanics. SRE / AI-agent specific concerns:

- AI system inventory must include agents, models, prompts, tool definitions, retrieval corpora.
- Impact assessment must address agent-specific impacts.
- Lifecycle tracking must accommodate the iteration speed of agent development.
- Vendor monitoring must include detection of model-behavior changes from providers.

## Stefan-context implementation sketch

- Solo / small-team operation: certification not currently warranted.
- For client engagements: implement aligned to ISO 42001 structure, document evidence in vault.
- Track EU AI Act harmonization progress; certification timing benefits from harmonization completion.
- For procurement-readiness: combined ISO 27001 + ISO 42001 alignment is the positioning to maintain.

## See also

- [[ISO 42001 Cluster|cluster MOC]] · [[ISO 42001 vs ISO 27001 Integration]]
- [[ISO 27001 Certification Process]] (sibling certification mechanics)
- [[EU AI Act Cluster]] (regulatory driver)
