title: TISAX Assessment Levels
summary: Three levels (AL1, AL2, AL3) determining audit depth and evidence requirements per TISAX assessment.
parent: tisax
order: 100
labels: tisax, tisax-mechanism
aliases: TISAX Assessment Levels | TISAX AL1 AL2 AL3 | TISAX AL Levels
type: tisax-mechanism
created: 2026-05-12
updated: 2026-06-08
origin: pillars/tisax/TISAX Assessment Levels.md
reviewed: no
---
> Three levels (AL1, AL2, AL3) determining audit depth and evidence requirements per TISAX assessment. The OEM specifies the required level per supplier per label. Choice of level drives audit cost, time, and rigour.

## AL1 — Self-assessment only

Lowest level. Supplier completes the VDA-ISA self-assessment. No external audit. Result published as a label in the ENX portal with the explicit annotation that it is AL1 (self-attested).

### When AL1 is used

- Rarely required by OEMs in practice. Most OEM contracts specify AL2 or AL3.
- Internal-pilot use when an org wants to enter the ENX system before completing the work for full audit.
- Some non-critical assessments where the OEM accepts self-attestation.

### Evidence requirements

Workbook completed honestly. No external evidence verification. Self-declaration of maturity-level scores per control.

### Output

Label in registry tagged AL1. Validity 3 years.

### Limitations

The AL1 label carries the lowest assurance weight. Procurement organizations and OEM-side teams treat it as a starting point, not a sufficient signal. Most TISAX activity skips AL1.

## AL2 — Self-assessment + plausibility check

Mid-tier level. Supplier completes self-assessment; audit provider conducts a plausibility check via remote interview and document review.

### When AL2 is used

- Common for tier-2 and tier-3 suppliers with non-critical access.
- Standard for Information Security with High protection requirement label when prototype-protection scope is absent or limited.
- Some Data Protection labels (standard, non-special-category).

### Audit conduct

- **Remote audit** — typical. Audit provider reviews supplier workbook, conducts video conference interviews with named control owners, requests document samples (policies, training records, access reviews, incident reports).
- **Duration** — typically 1-3 days of audit-provider effort over 2-4 elapsed weeks. Supplier-side effort heavier (preparation, interview attendance, document retrieval).
- **Sample size** — auditor selects sample of controls, typically 30-60% coverage with risk-weighted selection.
- **Evidence types** — policy documents, training completion records, audit log samples, change records, incident reports, supplier security records, vulnerability scan summaries, access-review records.

### Findings categorization

- **Major** — control significantly below target maturity; blocks label issuance until remediated.
- **Minor** — control marginally below target or evidence weak; conditional label allowed in some cases.
- **Observations** — improvement opportunities not blocking.

### Output

Label in registry tagged AL2. Audit report shared between supplier and audit provider; not published. ENX portal carries the label and validity period only.

## AL3 — Self-assessment + on-site audit

Highest level. Supplier completes self-assessment; audit provider conducts a full on-site audit.

### When AL3 is used

- Tier-1 suppliers with broad OEM access
- Development partners working on pre-series components or vehicles
- Information Security with Very High protection requirement label
- Any Prototype Protection label (almost always requires AL3)
- Special-category Data Protection label

### Audit conduct

- **On-site visit** — required. Audit provider attends supplier premises. Hybrid (one on-site + remote follow-up) accepted by some providers.
- **Multi-site scope** — large suppliers may have multiple sites in scope; auditor visits sample or full set depending on risk.
- **Duration** — typically 3-5 days on-site for single-site, longer for multi-site. Total elapsed time 4-8 weeks including preparation, audit, findings remediation, label issuance.
- **Sample size** — auditor selects deeper sample of controls than AL2, typically 60-90% coverage. Walk-throughs of critical processes (incident response, change management, access provisioning, prototype handling).
- **Physical inspection** — for Prototype Protection scope: visit to restricted-access rooms, observation of physical controls, review of badge / access logs, walk-through of physical perimeter and entry controls.
- **Evidence types** — same as AL2 plus on-site observation, physical-control inspection, deeper sampling, possibly random employee interviews.

### Findings categorization

Same major / minor / observation taxonomy as AL2. Major findings have shorter remediation windows in some cases due to the depth of the underlying gap.

### Output

Label in registry tagged AL3. Audit report shared between supplier and audit provider; not published.

## Selection criteria (how the OEM chooses)

OEM-side rules for assessment-level specification typically follow:

- **AL1** — rarely specified. Reserved for low-risk relationships or transitional cases.
- **AL2** — most non-development-partner relationships. Suppliers with confidential business information access but no prototype involvement.
- **AL3** — development partners, prototype-handling suppliers, suppliers with very-high-protection access (e.g., engineering simulation data, source code).

OEMs publish supplier-classification guides specifying which class of relationship triggers which assessment level. Tier-1s typically apply a similar classification to their own suppliers (cascading flow-down).

## Cost and time orientation

Indicative ranges for a typical mid-size supplier:

| Aspect | AL1 | AL2 | AL3 |
|---|---|---|---|
| Audit provider cost (€) | 0 (no audit) | 3-8k | 8-25k |
| Audit duration (days) | n/a | 1-3 | 3-5+ |
| Elapsed time | weeks | 2-4 weeks | 4-8 weeks |
| Supplier internal effort | self-paced | 2-4 person-weeks prep | 3-8 person-weeks prep |
| Validity | 3 years | 3 years | 3 years |

Multi-site assessments multiply cost and duration roughly linearly per additional site, with some shared overhead.

ENX participation fee separate (€1-5k annually, scales with org size).

## Common patterns by supplier tier

- **OEMs** — AL3 against full catalogue, multi-site.
- **Tier-1 suppliers** — AL3 + Info Sec Very High + often Prototype Protection. Multi-site for large tier-1s.
- **Tier-2 suppliers** — AL2 + Info Sec High most common; AL3 if specific contract requires.
- **Tier-3 and beyond** — AL2 + Info Sec High; sometimes AL1 for very small or non-critical suppliers.
- **Service providers (IT services, consultancies, MSPs serving auto)** — AL2 + Info Sec High typically; AL3 if accessing prototype data or strategic information.
- **Sub-processors of personal data** — Data Protection module added at AL2 or AL3 per OEM specification.

## Re-assessment and renewal

Labels are valid 3 years. Renewal assessment runs against the then-current VDA-ISA version. Supplier can begin renewal up to 6 months before expiry; common practice is starting 4-6 months before to ensure label continuity. Lapsed labels disappear from the portal; suppliers with lapsed labels lose OEM-side visibility until renewal completes.

## Findings remediation windows

- **AL2 minor findings** — typically 60-90 days to remediate; verification via document submission to audit provider.
- **AL2 major findings** — typically 60-90 days; verification often requires follow-up interview or document review.
- **AL3 minor findings** — similar window; verification by audit provider review.
- **AL3 major findings** — same window; may require follow-up site visit for critical physical or prototype-protection gaps.

Failure to remediate within the window can result in label withholding; the supplier then re-enters the assessment process.

## SRE and AI-agent fit notes

- **AL2 evidence for AI controls** — likely review of:
  - System prompt version control and review records
  - Tool-scope documentation and approval records
  - Agent action audit log retention and sample reviews
  - Vendor (model provider) due diligence records, including DPA and data-handling commitments
  - Cloud-service authorization and configuration evidence
- **AL3 evidence for AI controls** — same plus:
  - On-site interview with AI / ML engineering lead
  - Walk-through of agent-system deployment process
  - Observation of incident-response capability for agent-related incidents
  - Verification of physical and logical separation between AI tooling and prototype-data environments

## Stefan-context implementation sketch

- For solo / small-team consulting, formal TISAX is rare. When required, AL2 against Info Sec High is the realistic minimum; AL3 if engagement involves prototype data.
- Pre-engagement: confirm OEM-specified level and labels via client contract review.
- Internal preparation: self-assessment against current VDA-ISA workbook 6-12 weeks before audit; remediate gaps; collect evidence into structured folder.
- Audit-provider selection: confirm TISAX accreditation via ENX portal; check sector experience.

## See also

- [[TISAX Cluster|cluster MOC]] · [[TISAX VDA-ISA Catalogue]] · [[TISAX Labels and Scopes]] · [[TISAX Assessment Process]]
