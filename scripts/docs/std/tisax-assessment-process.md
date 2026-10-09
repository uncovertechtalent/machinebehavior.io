title: TISAX Assessment Process
summary: End-to-end mechanics for a TISAX assessment.
parent: tisax
order: 100
labels: tisax, tisax-mechanism
aliases: TISAX Assessment Process | TISAX Audit Process | TISAX Registration
type: tisax-mechanism
created: 2026-05-12
updated: 2026-06-08
origin: pillars/tisax/TISAX Assessment Process.md
reviewed: no
---
> End-to-end mechanics for a TISAX assessment. From OEM contract trigger, through ENX registration, self-assessment, audit-provider selection, audit conduct, findings remediation, label issuance, and ongoing maintenance.

## Trigger

The process begins when:

- **An OEM contract clause requires TISAX** — supplier reviews flow-down clauses, identifies required labels and assessment levels, plans implementation.
- **A tier-1 customer flows down a TISAX requirement** — sub-tier supplier responds similarly.
- **Voluntary positioning** — supplier obtains TISAX proactively to access automotive procurement opportunities without specific contractual driver. Less common.

## Step 1: ENX registration

Supplier registers as a TISAX participant with ENX Association via enx.com. Registration includes:

- Legal-entity identification
- Site information (locations to be in scope)
- Primary contacts (typically: business contact, technical / security contact)
- Annual participation fee payment

Registration validity is open-ended (renews annually with fee payment). The supplier becomes a participant in the ENX system and gains portal access.

Cost: ENX participation fees vary by organization size; typical range €1k-5k annually.

## Step 2: Define assessment scope

Supplier defines:

- **Labels** required (per OEM contract or strategic choice)
- **Assessment level** per label (AL1 / AL2 / AL3, per OEM specification)
- **Sites** in scope
- **Audit timing** target

This scope is registered with ENX before audit-provider engagement.

## Step 3: Self-assessment

Supplier completes the VDA-ISA workbook for the in-scope module(s):

- Information Security module (almost always)
- Prototype Protection module (if applicable)
- Data Protection module (if applicable)

For each control:

- Identify target maturity level (per OEM-specified protection requirement)
- Honestly assess current maturity level
- Document evidence
- Note any gaps and remediation plans

Self-assessment serves three functions:

- Internal gap analysis driving remediation work
- Input to audit-provider engagement (the auditor reviews the self-assessment)
- Audit-provider evidence baseline (a credible self-assessment shortens audit time; a sloppy one extends it)

Typical effort: 4-12 person-weeks for first-time self-assessment depending on maturity start point.

## Step 4: Remediation

Gaps identified in self-assessment are remediated before audit:

- Missing documents created
- Process gaps closed
- Training rolled out
- Technical controls implemented or upgraded
- Evidence collection systematized

Common remediation duration: 2-6 months for organizations starting from low maturity, shorter for organizations with existing ISO 27001 implementation.

Remediation done before audit reduces findings and shortens label-issuance timeline.

## Step 5: Audit-provider selection

Supplier selects an ENX-accredited audit provider. Selection criteria:

- **Accreditation confirmation** — check ENX portal for current accreditation status
- **Sector experience** — auto-supplier vs IT-services-supplier vs OEM-internal audit experience varies
- **Geographical fit** — German auditors common; some international audit providers have TISAX accreditation
- **Module coverage** — auditor accreditation may cover Info Sec only, or include Prototype Protection and Data Protection
- **Capacity / scheduling** — peak periods (autumn / spring) can have multi-month waiting lists
- **Cost** — quotes vary across providers; obtain 2-3 quotes for comparison

Common audit providers: TÜV SÜD, TÜV Rheinland, TÜV Nord, DEKRA, DQS, KPMG, Deloitte, PwC, EY, BSI Group, and several specialist firms.

The supplier signs an engagement contract with the audit provider. The audit-provider relationship is independent of ENX (ENX accredits providers; suppliers contract with providers directly).

## Step 6: Audit conduct

Audit conduct depends on assessment level:

### For AL2 (plausibility check)

- **Kick-off meeting** — confirm scope, schedule, evidence-submission process. Typically remote.
- **Document review** — supplier submits documents via secure channel; auditor reviews ahead of interviews.
- **Interview phase** — video conferences with control owners (CISO / ISMS manager, HR for screening / training, IT for technical controls, business-process owners). Typically 1-3 days of interviews.
- **Auditor analysis** — auditor scores controls based on evidence and interviews, reconciles with supplier self-scores, drafts findings.

### For AL3 (full on-site audit)

- **Kick-off meeting** — typically on-site, opening session with management.
- **Document review** — pre-visit and during visit.
- **Interview phase** — on-site interviews with same role coverage as AL2 plus additional interviews and observations.
- **Physical inspection** — for Prototype Protection scope: tour of restricted-access rooms, observation of physical controls, review of badge / access logs. For Info Sec scope: tour of data-centre or server-room areas if applicable, observation of physical security generally.
- **Walk-throughs** — auditor walks through critical processes: incident response (often via tabletop exercise or recent-incident review), change management (sample change tickets), access provisioning (sample joiner-mover-leaver records), prototype handling if in scope.
- **Auditor analysis** — same as AL2 with deeper sampling.

### Closing meeting

- Auditor presents preliminary findings: major nonconformities, minor nonconformities, observations.
- Supplier acknowledges and clarifies.
- Remediation timeline agreed for blocking findings.

## Step 7: Findings remediation

Major findings must be remediated for label issuance. Mechanics:

- **Remediation plan** — supplier submits to audit provider within an agreed window (typically 30 days).
- **Remediation execution** — supplier implements the corrective action.
- **Evidence submission** — supplier submits remediation evidence (updated documents, training records, screenshot evidence, third-party verification where applicable).
- **Auditor verification** — auditor reviews evidence; may require additional interview or, in critical cases, follow-up visit.
- **Window** — typical 60-90 days from audit completion to remediation closure.

Minor findings have similar mechanics but lower urgency; some auditors allow them to be addressed within the validity period rather than pre-issuance.

Observations are informational; not blocking.

## Step 8: Label issuance

After successful audit completion and findings closure, the audit provider issues label(s) to ENX. The portal records:

- Label(s) awarded
- Assessment level per label
- Site coverage
- Validity start and end dates (3 years from issuance)
- Audit-provider identity
- Catalogue version against which assessed

The supplier receives notification of label issuance and confirms via the portal.

## Step 9: Ongoing maintenance

During the 3-year validity:

- **No surveillance audits required** (unlike ISO 27001, which has annual surveillance audits).
- **Internal maintenance** — supplier maintains controls, updates documentation, runs internal audits to verify continued effectiveness.
- **Scope changes** — adding sites or business processes mid-cycle requires an in-cycle re-assessment. Removing scope is allowed via portal update.
- **Major changes** — significant organizational changes (M&A, major restructure, major incident) may trigger OEM requests for early reassessment.
- **Customer authorization** — supplier authorizes new OEM customers to view labels as procurement relationships develop.

## Step 10: Renewal

3-year validity approaching expiry:

- **Begin renewal 4-6 months before expiry**.
- **Repeat process** from Step 3 (self-assessment) against the current catalogue version.
- **Audit-provider continuity** — supplier may use the same provider or switch; switching is not unusual and not penalized.
- **Catalogue version** — renewal assessment runs against the catalogue version current at audit start. Major catalogue revisions may extend the prep period.

## Common operational timing

Realistic timeline for a first-time TISAX assessment:

| Phase | Duration |
|---|---|
| ENX registration | 1-2 weeks |
| Self-assessment + initial remediation planning | 4-8 weeks |
| Remediation work | 2-6 months |
| Audit-provider selection and scheduling | 1-3 months (depending on auditor capacity) |
| Audit conduct | AL2: 2-4 weeks elapsed; AL3: 4-8 weeks elapsed |
| Findings remediation (if needed) | 30-90 days |
| Label issuance | 1-2 weeks after remediation closure |
| **Total** | **6-12 months typical** |

Aggressive timeline (existing strong ISO 27001 implementation, dedicated PM): 3-6 months. Stretch (low maturity, distributed responsibility): 12-18 months.

## Common pitfalls

- **Underestimating self-assessment effort.** The workbook is detailed; thorough self-assessment requires significant subject-matter time across the org. Not just a security-team exercise.
- **Engaging audit provider before remediation.** Auditor schedules months out; engaging too early means audit lands before remediation completes, generating findings that could have been avoided.
- **Confusing TISAX with ISO 27001 mechanics.** They share controls but mechanics differ. SoA-equivalent freedom does not apply; OEM-specified labels constrain scope.
- **Site-scope drift.** Adding a site post-issuance triggers re-assessment for that site. Scope decisions at the start of the process matter.
- **Audit-provider confusion on Prototype Protection.** Not all audit providers have deep Prototype Protection capability. Confirm capability for the specific module before engagement.
- **OEM addenda missed.** Some OEMs publish security requirements beyond TISAX baseline. Suppliers focusing only on TISAX miss these and fail OEM-side reviews despite holding the label.

## SRE and AI-agent fit notes

- **Self-assessment evidence for AI controls** — system prompt version control, tool-scope review records, agent action audit logs, vendor due-diligence records, cloud-service authorization evidence, configuration baselines.
- **Audit-provider AI-control depth** — varies. AL2 audits typically light on AI-specific probing as of 2026; AL3 audits increasingly include questions on AI-tool use, particularly for suppliers with prototype-data access.
- **Remediation around AI handling** — common findings (anticipated, as catalogue and audit practice catch up): missing or weak version control on system prompts; missing tool-scope documentation; weak vendor due diligence for model providers; inadequate audit log retention for agent actions; missing data-handling commitments from model providers (zero-retention, no training data use).

## Stefan-context implementation sketch

For solo / small-team operation against automotive client:

- Prep: VDA-ISA workbook self-assessment ahead of audit need
- Audit-provider selection: smaller German specialist firms or mid-tier (TÜV Hessen, DQS, regional specialists) more cost-effective than Big Four for small-supplier scope
- Audit conduct: AL2 remote is the realistic minimum; AL3 only if engagement specifically requires
- Evidence base: vault git history covers most documentation; supplement with audit-log retention records, training evidence (continuous-learning records), vendor-relationship documentation

## See also

- [[TISAX Cluster|cluster MOC]] · [[TISAX VDA-ISA Catalogue]] · [[TISAX Assessment Levels]] · [[TISAX Labels and Scopes]]
- [[ISO 27001 Certification Process]] (sibling process for ISO 27001 — different mechanics, useful contrast)
