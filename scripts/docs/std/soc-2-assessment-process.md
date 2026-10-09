title: SOC 2 Assessment Process
summary: End-to-end mechanics for SOC 2 attestation: readiness, gap analysis, control implementation, audit, report.
parent: soc2
order: 100
labels: framework-concept, soc2
aliases: SOC 2 Assessment Process | SOC 2 Audit Process | SOC 2 Engagement Mechanics
type: framework-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/soc2/SOC 2 Assessment Process.md
reviewed: no
---
> End-to-end mechanics for SOC 2 attestation: readiness, gap analysis, control implementation, audit, report. Engagement with CPA firm under SSAE 18.

## Readiness phase

### Gap analysis

Service org assesses current state against TSC:

- Identify TSC categories in scope.
- Map existing controls to TSC criteria.
- Identify gaps.
- Plan remediation.

Often facilitated by consultant or GRC tooling (Drata, Vanta, Secureframe, Tugboat Logic).

### Control implementation

Remediate identified gaps:

- Document policies and procedures.
- Implement technical controls.
- Build evidence collection.
- Train staff.
- Establish operating cadence for ongoing controls.

For Type 2: controls must operate consistently before the audit period.

### Readiness assessment

Optional pre-audit assessment by the CPA firm or another consultant. Identifies remaining issues before formal audit. Common practice.

## Engagement with CPA firm

### CPA firm selection

Criteria:

- AICPA-licensed (required).
- SOC 2 specific experience.
- Industry / sector experience.
- Combined-report capability (SOC 2 + ISO 27001 + others where applicable).
- Geographic reach.
- Cost.

Common firms: Schellman, A-LIGN, Coalfire, BSI Americas, Deloitte, KPMG, PwC, EY, mid-tier firms.

### Engagement letter

Defines:

- TSC categories in scope.
- Type 1 or Type 2.
- Period (Type 2).
- System description scope.
- Subservice organization treatment (carve-out vs inclusive).
- Fee structure.

## Audit conduct

### Type 1

- Kick-off meeting.
- System description review.
- Controls walkthrough (auditor understands control design).
- Inquiry, observation, inspection of relevant evidence.
- Auditor opinion on control design suitability.

Typical duration: 4-8 weeks.

### Type 2

All of Type 1 PLUS:

- Sample testing of control execution over the period.
- Tests of operating effectiveness.
- Issue documentation and resolution.
- Auditor opinion on design + operating effectiveness.

Typical duration: period + 2-4 months for audit + report.

## System description

Service org writes the system description covering:

- Services provided
- Infrastructure
- Software
- People
- Procedures
- Data

The system description is integrated into the SOC 2 report. Drafting is substantive work.

## Subservice organizations

Service orgs typically depend on subservice orgs (AWS, GCP, Azure, others). Treatment:

- **Carve-out method** — subservice org's controls excluded; user entity must consider subservice org's own SOC 2 separately.
- **Inclusive method** — subservice org's controls included in service org's audit (rare; requires substantive subservice org cooperation).

Carve-out is standard; user entities review subservice org SOC 2 reports separately.

## Control activities and complementary user entity controls (CUECs)

CUECs are controls the user entity (customer of the service org) must implement to complete the security picture. Documented in the SOC 2 report.

Example: service org provides MFA capability; user entity must enable and enforce MFA for its users. The "enforce MFA" control is a CUEC.

## Report issuance

### Report structure

- Independent service auditor's report
- Management's assertion
- Description of the system
- Description of tests of controls (Type 2)
- Results of tests (Type 2)
- Other information (optional)

### Report distribution

- Confidential to service org and authorized recipients.
- Typically shared under NDA with customers.
- SOC 3 reports (separate engagement) can be made public.

### Report retention

- Service org retains for prescribed periods.
- Common: indefinite retention; superseded by subsequent reports.

## Annual cycle

After first-year Type 2:

- Annual Type 2 reports (rolling 12-month periods, often calendar year or fiscal year).
- Continuous control execution.
- Continuous evidence collection.
- Periodic bridging letters between annual reports.

## Common pitfalls

- **Insufficient period prior to first Type 2.** Controls must operate consistently; 3-month minimum period assumes 3 months of operating discipline.
- **Subservice org coordination failures.** Inclusive method only practical when subservice cooperates.
- **System description drift.** System description must reflect actual system; updates needed as system evolves.
- **Type 1 used in place of Type 2.** Many enterprise customers require Type 2; Type 1 alone insufficient.
- **Privacy TSC scope expansion** without aligned GDPR / state privacy law work creates duplication.

## SRE and AI-agent fit notes

### Evidence collection for AI features

Type 2 audits require evidence over the period:

- Change logs for system prompts.
- Audit logs for agent actions.
- Vendor relationship records.
- Vulnerability scan results.
- Access review records.
- Training records.

Continuous evidence collection essential.

### AI vendor as subservice org

Model providers (Anthropic, OpenAI, others) are subservice orgs:

- Treated as carve-out.
- User entity (service org) reviews vendor's SOC 2 / ISO 27001 reports.
- CUECs covering vendor relationship management.

## Stefan-context implementation sketch

- For client engagements on SOC 2 readiness: gap analysis + remediation guidance.
- For Type 2 audit support: evidence-collection infrastructure.
- For AI-feature inclusion: documented controls covering AI-specific TSC application.

## See also

- [[SOC 2 Cluster|cluster MOC]] · [[SOC 2 Trust Services Criteria]] · [[SOC 2 Type 1 vs Type 2]] · [[SOC 2 vs ISO 27001]]
- [[ISO 27001 Certification Process]] (sibling certification mechanics)
