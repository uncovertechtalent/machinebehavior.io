title: ISO 27001 Certification Process
summary: End-to-end mechanics of getting and keeping an ISO/IEC 27001:2022 certificate.
parent: iso-27001
order: 100
labels: cross-cutting, iso-27001
aliases: ISO 27001 Certification | ISO 27001 Audit Process | ISO 27001 Stage 1 Stage 2 | ISO 27001 Surveillance | ISO 27001 Recertification
type: cross-cutting
created: 2026-05-12
updated: 2026-06-08
origin: pillars/iso-27001/ISO 27001 Certification Process.md
reviewed: no
---
> End-to-end mechanics of getting and keeping an ISO/IEC 27001:2022 certificate. Implementation timeline, the four-audit cycle (Stage 1, Stage 2, two surveillances, recertification), accreditation chain, certification-body selection, cost structure, common procedural pitfalls.

## Implementation timeline (first-time certification)

Typical timeline for a 50-300 person SaaS company doing it well, with executive support and existing security maturity:

- **Months 0-2:** scope decision, gap analysis against ISO 27001:2022 + Annex A. Selection of methodology, project plan.
- **Months 2-6:** policy and procedure authoring, risk methodology implementation, control implementation work for identified gaps.
- **Months 6-9:** initial risk assessment, SoA production, control implementation completion, training rollout, evidence base buildup.
- **Months 9-10:** internal audit dry run. Findings remediated.
- **Month 10:** management review. ISMS at minimum-viable maturity.
- **Months 10-11:** Stage 1 audit (documentation review, readiness check).
- **Months 11-13:** Stage 2 audit (full ISMS implementation audit). Certification decision.

Aggressive timeline (existing strong security culture, dedicated project manager, consultant support): 6-9 months. Realistic for most: 9-15 months. Stretch (low maturity start, distributed responsibility): 18-24 months.

## The four-audit cycle

Once certified, the cycle runs three years from initial certification:

- **Year 1:** Initial certification = Stage 1 + Stage 2.
- **Year 2:** Surveillance audit 1 (smaller scope, typically 30-50% of the org's ISMS sampled).
- **Year 3:** Surveillance audit 2 (similar scope to Y2, different controls sampled).
- **Year 4:** Recertification audit (full scope, similar to Stage 2 effort).

Then the cycle repeats.

Each audit produces a report with findings classified as:

- **Major nonconformity** — must be addressed before certification is granted / maintained. Common triggers: a "shall" requirement not met, evidence of systemic control failure, scope drift not addressed in the SoA.
- **Minor nonconformity** — must be addressed within an agreed timeframe (typically 60-90 days) and verified at next audit.
- **Observation / opportunity for improvement** — non-binding feedback; not addressing it is not a finding but pattern over multiple cycles may become one.

## Stage 1 audit

Documentation and readiness review. Auditor checks:

- Is the ISMS scope documented and reasonable?
- Are the management-system documents (policies, procedures, methodologies, SoA) in place and consistent?
- Is the risk assessment and treatment work substantively complete?
- Is the internal audit programme planned and at least partially executed?
- Has at least one management review occurred?
- Are the basic control implementations evidenced?

Outcome: either "ready for Stage 2" or "not yet ready; address X, Y, Z first." Stage 1 is meant to catch obvious gaps before the more expensive Stage 2.

## Stage 2 audit

Full implementation audit. Multi-day on-site / remote sessions, sampling-based, covering all clauses and Annex A controls within the SoA. Typical scope:

- Document review (continued from Stage 1).
- Interviews with top management, the ISMS manager, control owners, sampled staff.
- Evidence sampling: training records, audit logs, change tickets, incident reports, supplier records, vulnerability scans, access reviews.
- Walkthroughs of critical processes (incident response, change management, access provisioning, vendor onboarding).
- Site visits where applicable.

Outcome: certification decision. Findings categorized. Major nonconformities block certification until addressed and verified.

## Surveillance audits

Smaller-scope checks, typically 1-2 days. Cover:

- A risk-weighted subset of controls (auditor decides; orgs cannot pre-negotiate exclusion).
- Significant changes since the last audit (new vendors, new products, organizational changes).
- Status of any open nonconformities from prior audits.
- Management review and internal audit cycle continuity.
- A sample of recurrent processes (some incidents, some access reviews, some training records).

Cumulatively over the three-year cycle, the auditor sees most of the ISMS. They are never expected to see all of it every year; the org is.

## Recertification audit

Reset of the cycle. Similar effort to Stage 2. Confirms ISMS continues to meet requirements and is effective. New certificate issued (valid three years).

If the org has changed substantially (acquisition, new business lines, major scope expansion), recertification can effectively re-run a Stage 1 + Stage 2.

## Accreditation chain

Three layers:

- **IAF** (International Accreditation Forum) — mutual recognition arrangement coordinator. The "accreditation of accreditors" body.
- **Accreditation bodies** — UKAS (UK), DAkkS (DE), ANAB (US), JAS-ANZ (AU/NZ), and equivalents per country. They accredit certification bodies.
- **Certification bodies** — BSI, DNV, TÜV SÜD, LRQA, SGS, Bureau Veritas, Schellman, etc. They certify organizations.

A "real" ISO 27001 certificate is issued by a certification body accredited under ISO/IEC 17021-1 by a recognized accreditation body. Certificates from unaccredited issuers exist; they carry no weight in procurement due diligence.

Buyer-side verification: the certificate names the certification body, which can be looked up on the accreditation body's website to confirm accreditation scope and status. The IAF maintains a directory of accreditation bodies.

## Certification body selection

Practical criteria:

- **Accreditation scope match.** Some bodies accredit for ISO 27001 in some countries / sectors but not others. Confirm before signing.
- **Sector experience.** SaaS auditors, financial-services auditors, manufacturing auditors all exist. Asking "have you certified comparable orgs" is reasonable.
- **AI / cloud capability.** As of 2026, ask explicitly about Annex A.5.7, A.5.23, A.8.9, A.8.16, A.8.28 audit depth. Auditor variance on these controls is high.
- **Combined certification.** If pursuing 27001 + 27701 (privacy), 27001 + 27017 (cloud), 27001 + 22301 (BC), 27001 + 42001 (AI), confirm the body can audit the combination.
- **Geography.** Local body for local certification often eases procurement; recognized international bodies offer broader recognition.
- **Cost.** Quotes vary 30-50% across bodies for the same scope. Bottom-of-market quotes often signal accreditation gaps or under-resourced auditing.

Common bodies (non-exhaustive, no endorsement implied):

- **UK / EMEA emphasis:** BSI Group, LRQA, BV, DNV, SGS.
- **DE Mittelstand emphasis:** TÜV SÜD, TÜV Rheinland, TÜV Nord, DEKRA.
- **US emphasis:** Schellman, A-LIGN, Coalfire, BSI Americas.
- **Global volume leaders:** SGS, BSI, BV.

## Cost structure (orientation)

For a 50-300 person SaaS, ranges as of 2026 (euro equivalents, ballpark):

- **First-time certification:** €15-40k for Stage 1 + Stage 2 + first surveillance. Plus €20-60k for consultant support if used. Plus €0-100k of internal staff time depending on starting maturity (6-12 person-months commonly).
- **Per surveillance audit (years 2, 3):** €5-12k each.
- **Recertification (year 4):** €15-30k.
- **Internal effort steady-state:** ~10-20% of one FTE for ISMS maintenance once mature, plus periodic spikes (audit prep, scope changes).

For a 1000+ person enterprise, multiply by 3-5x for audit costs and proportionally more for internal effort. For a 1-10 person startup, smaller orgs sometimes get away with €8-15k all-in plus more lightweight implementation.

## Common procedural pitfalls

- **Selecting a certification body without checking accreditation.** A certificate from an unaccredited body is procurement-worthless and discovers itself in the first enterprise RFP that takes due diligence seriously.
- **Consultant-as-auditor conflict.** The consultant who helped you implement should not be the internal auditor. Cl 9.2.2.c independence finding waiting to happen.
- **Treating Stage 1 as ceremonial.** Auditor recommendations at Stage 1 are first-class warnings; not addressing them tanks Stage 2.
- **Auditor-shopping perception.** Switching certification bodies repeatedly looking for easier audits is detectable in buyer due diligence (certificate history visible).
- **Scope drift between audits.** Org grows, adds new product, expands geographically, and lets the SoA fall behind. Major nonconformity at next surveillance or recertification.
- **Transition deadline missed.** Orgs certified under :2013 had until 31 October 2025 to transition to :2022. As of 2026-05-12 the window has closed; certificates against :2013 are no longer valid.

## Path for small / solo operations

ISO 27001 certification is overhead-heavy for solo or very small operations. Common patterns:

- **Cyber Essentials Plus (UK)** — much narrower; ~£1k-3k all-in; sufficient for many UK government tenders and entry-level enterprise.
- **SOC 2 Type 1 / Type 2** — US-aligned; lighter implementation overhead than 27001; common for early-stage SaaS.
- **ISO 27001 alignment without certification** — implement the standard, document the work, present evidence to customers on request, without paying for certification. Loses the third-party-attested signal; saves the cost. Works for buyers who accept it; does not work for buyers who require a certificate.
- **Certification when revenue justifies.** Common threshold: when ARR is large enough that one enterprise deal requiring certification covers the certification cost with margin to spare, or when a specific deal makes the certificate a path-clearer.

## Stefan-context implementation sketch

- Solo / small-team consulting: certification is not currently warranted. Implement aligned to :2022 structure, maintain evidence in vault, present client-by-client when engagement requires.
- For [employer]-class client work: client may carry ISO 27001 certification; supplier flow-down obligations apply. Document compliance with the relevant clauses without seeking own certification unless a buyer specifically requires it.
- Re-evaluate certification when: a buyer mandates it for procurement, when client portfolio reaches a scale where multiple buyers each save individual due-diligence effort, or when ISO 42001 ecosystem matures enough that combined-cert positioning is commercially significant.

## See also

- [[ISO 27001 Cluster|cluster MOC]] · [[ISO 27001 Family and Sector Variants]] · [[ISO 27001 Version History]] · [[ISO 27001 Controversies]]
- [[ISO 27001 Clause 9 Performance Evaluation]] (internal audit, the precursor to external audit)
- [anchors](pillars/iso-27001/anchors.md) (certification body listings)
