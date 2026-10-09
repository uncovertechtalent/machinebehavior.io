title: ISO 27001 Controversies
summary: Contested points and known failure modes of the standard and its certification ecosystem.
parent: iso-27001
order: 100
labels: cross-cutting, iso-27001
aliases: ISO 27001 Controversies | ISO 27001 Critique | ISO 27001 Failure Modes | Compliance Theatre
type: cross-cutting
created: 2026-05-12
updated: 2026-06-08
origin: pillars/iso-27001/ISO 27001 Controversies.md
reviewed: no
---
> Contested points and known failure modes of the standard and its certification ecosystem. The standard is widely used because procurement requires it, not because it is uncontested. Honest implementers and informed buyers should know where the gaps are.

## Compliance ≠ security

The most-cited critique. Documented in every major breach analysis since 2013. Patterns:

- **2013 Target breach** — PCI DSS compliant at time of breach. 40M payment card records exfiltrated via HVAC vendor compromise. PCI compliance did not predict breach absence.
- **2017 Equifax breach** — multiple security certifications. Lost 147M records via an unpatched Apache Struts vulnerability that had been disclosed months earlier. Patch management process existed; was not executed.
- **2017 Maersk / NotPetya** — ISO 27001 certified globally. Lost the entire Active Directory infrastructure in hours to a single accidentally-spread destructive worm. Recovered via a single offline domain controller in a Ghana office (off due to power outage). The certification did not produce the resilience that the recovery did.
- **2020 SolarWinds** — supplier-side compromise affecting tens of thousands of customers including ISO-certified Fortune 500 and government departments. Cl A.15 / A.5.21 supplier-controls coverage proved inadequate against a sophisticated supply-chain attack.
- **2021 Kaseya / REvil** — supply-chain ransomware against managed-service-provider customers. Many compromised customers were ISO 27001 or SOC 2 certified.
- **2024 Change Healthcare / UnitedHealth** — RaaS encrypted 25% of all US health claims for weeks. Multiple certifications across the affected entities.

The conclusion is consistent: the certificate is a procurement signal, not a security signal. The work to produce the certificate has security value; the certificate itself does not.

Bruce Schneier has written for two decades on the gap between security and compliance theatre. The position is now broadly accepted within the security community; less so by procurement organizations who use the certificate as a shortcut.

## Statement of Applicability scope-narrowing

Orgs frequently draw the ISMS scope narrowly to make certification achievable:

- "We are certifying the SaaS product, not corporate IT" — but corporate IT runs the joiner-mover-leaver process and the laptop fleet that has dev access to the product.
- "We are certifying production, not dev" — but dev is the path into production via the build pipeline.
- "We are certifying customer-facing services, not internal services" — but internal services hold the customer data when employees use them.

The SoA exclusions are technically permitted by Cl 6.1.3.d ("the justification for excluding any of the Annex A controls"). What is contested is the buyer-perception gap: a certificate against a narrowly-scoped ISMS may be presented in procurement as if it covered the whole org.

Mature buyers (large enterprises, sophisticated financial services, security-conscious procurement) ask for the SoA and the scope statement explicitly. Less mature buyers accept the certificate at face value.

## Auditor variance and the certification-body market

Inter-auditor reliability data is not published. Practitioner reports consistently describe:

- Same evidence package judged differently by different auditors.
- Same control implementation called "implemented" by one auditor and "partial" by another.
- Wide variance in audit-day rigor between certification bodies and within certification bodies.

The economic structure compounds this: the auditee pays the certification body. Bodies that are "harder" lose business to bodies that are "easier." Accreditation under ISO/IEC 17021-1 is the only external constraint, and accreditation bodies' enforcement is uneven.

Practitioner term: "auditor shopping" — switching certification bodies to find easier audits. Detectable in buyer due diligence (certificate-history visible) but rarely flagged.

The cumulative effect is that certificate equivalence is weaker than the procurement-perceived signal suggests.

## Documentation overhead vs operational reality

The standard requires documented information for the management system (Cl 7.5). Mature audits expect:

- Information security policy
- Topic policies (often 15-25 documents)
- Procedures for ISMS-critical processes (often 30-50 documents)
- SoA (large table)
- Risk methodology, risk register, risk treatment plan
- Asset inventory
- Internal audit programme, plans, reports
- Management review minutes
- Training records, awareness materials, communications
- Supplier registers, supplier-control evidence
- Incident records, post-incident reviews
- Change records, vulnerability scan reports, access reviews
- Configuration baselines

The documentation set is large enough that maintaining it becomes a job, often a compliance-team-shaped job rather than an engineering one. The compliance function then drifts from engineering reality, creating the policy-vs-practice gap that auditors find but that the org has already learned to gloss.

Counter-argument: documentation discipline has security value when the documents are read, used, and updated. The failure mode is documentation as artefact, not documentation as practice.

## Slow update cycle vs fast threat landscape

ISO 27001 revision cycle is 5-10 years. Threat landscape evolution is months to years. By the time a new technique or threat is incorporated:

- Cloud (matured 2010-2015) — explicit A.5.23 control added in :2022.
- Threat intelligence as a discipline (matured 2014-2020) — explicit A.5.7 control added in :2022.
- Supply-chain attacks (SolarWinds 2020, ongoing) — coverage at A.5.21 / A.5.22 level remains policy-only, with operational guidance outside the standard (SLSA, SBOM, signed releases).
- AI-system risks (prompt injection 2022+, agent autonomy 2024+) — no controls in :2022 Annex A. ISO 42001:2023 is the partial answer; integration with 27001 is immature.

For fast-moving threat areas, ISO 27001 is structurally a lagging indicator. Mature implementations bridge this by adding company-specific controls to the SoA, referencing external frameworks (OWASP, MITRE) for operational guidance.

## AI-system fit gaps

A specific subset of the slow-update problem. As of 2026-05-12 the standard does not address:

- **Prompt injection** as a threat class.
- **Autonomous agent action accountability** when no human is in the loop.
- **Model-vendor-as-implicit-data-processor** beyond generic cloud-service controls.
- **System prompt and tool scope as policy artefacts** that need version control, peer review, and SDLC discipline.
- **Agent-generated audit log fidelity** — agents can be unreliable narrators of their own actions.
- **Inference-time model behavior drift** when vendors update models behind a stable API.
- **Training-data IP and consent** flowing through to model behavior.
- **Adversarial robustness** as a system property.

ISO 42001:2023 covers AI management system; the bridge guidance to 27001 is still maturing. The OWASP LLM Top 10 (2023, 2024 revision) is the de facto operational taxonomy. MITRE ATLAS is the threat-modelling reference.

Pragmatic implementation pattern: extend the SoA with company-specific controls anchored to A.5.7, A.5.23, A.8.16, A.8.28; document the rationale; track ISO 42001 alignment for future combined certification.

## The "we passed the audit, then we got breached" pattern

A recurring narrative in breach post-mortems:

- Pre-breach: org is ISO 27001 certified, often for multiple cycles.
- Breach: occurs via a vector the certification did not catch (supply chain, social engineering, configuration drift, insider, novel technique).
- Post-breach analysis: certified controls were technically in place but operationally weak (e.g., MFA enabled but bypass paths existed, training delivered but ineffective, vulnerability scanning run but findings unactioned).

The lesson is not that ISO 27001 is useless. The lesson is that the certificate evidences process maturity, not threat coverage. Process maturity is necessary but not sufficient.

## SoA inflation

Counter-pattern to scope-narrowing: orgs claiming "all 93 controls applicable, all implemented" without operational depth behind each claim. The SoA becomes a checklist of yeses rather than a thoughtful map of risk-to-control.

Mature audits probe randomly: "show me the evidence for A.8.16 implementation" — and the depth of the response reveals whether the SoA reflects practice.

## Certification-body conflicts of interest

Certification bodies sell:

- Pre-certification consulting (where permitted; many bodies separate this into different legal entities or limit cross-billing).
- Certification audit.
- Surveillance and recertification audits.
- Training (auditor training, awareness training, implementation training).

The same body can be involved across multiple commercial lines for the same customer, with separate teams. Accreditation rules under 17021-1 forbid the same individual from auditing what they have consulted on for the same customer. The structural conflict at the firm level persists.

## Cost gating and small-org access

ISO 27001 certification cost (€15-40k+ for small SaaS first-time, plus consultant fees and internal effort) gates smaller orgs out. Effects:

- Small orgs that should have an ISMS skip formal certification, lose enterprise procurement.
- Small orgs that need certification stretch budgets, end up with shallow implementations.
- Mid-market increasingly turns to combined SOC 2 + ISO 27001 to amortize the audit cost.
- "ISO 27001-aligned, not certified" becomes a procurement-acceptable middle ground for some buyers.

The certification-cost gate has improved over the last decade (more certification bodies, more standardization of tooling, more SaaS-based GRC platforms reducing implementation cost) but remains a barrier.

## Counterpoint: what ISO 27001 still does well

The critique is not that the standard should be abandoned. The structural benefits are real:

- **Procurement leverage.** A credible certification reduces RFP friction materially. The signal is imperfect but better than no signal.
- **Internal commitment generation.** Cl 5 leadership obligations move security up the org chart in ways that informal initiatives often fail to.
- **Process discipline.** Cl 9 (internal audit, management review) and Cl 10 (corrective action) install a feedback loop that many orgs lack pre-certification.
- **Common vocabulary.** Practitioners, auditors, and procurement teams share terms drawn from the standard.
- **Annex A as risk-input checklist.** Even when the SoA implementation is shallow, the Annex A enumeration helps identify control gaps that orgs might not otherwise consider.
- **International recognition.** The certificate is accepted globally in a way few alternatives match.

The critique is calibrative: the certificate is one piece of evidence, not proof of security. Treat it accordingly.

## See also

- [[ISO 27001 Cluster|cluster MOC]] · [[ISO 27001 Certification Process]] · [[ISO 27001 Version History]] · [[ISO 27001 Family and Sector Variants]]
- [position](pillars/iso-27001/position.md) (cluster-level position derived from these contested points)
