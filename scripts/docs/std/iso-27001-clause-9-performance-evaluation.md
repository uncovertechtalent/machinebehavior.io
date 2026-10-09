title: ISO 27001 Clause 9 Performance Evaluation
summary: Requirements: ISO/IEC 27001:2022 clause 9, Performance evaluation; text at https://www.iso.org/standard/27001 (licensed, not reproduced here).
parent: iso-27001
order: 100
labels: clause-9, iso-27001, iso-clause
aliases: ISO 27001 Clause 9 | ISO 27001 Performance Evaluation | ISO 27001 Monitoring | ISO 27001 Internal Audit | ISO 27001 Management Review
type: iso-clause
created: 2026-05-12
updated: 2026-10-09
origin: pillars/iso-27001/ISO 27001 Clause 9 Performance Evaluation.md
reviewed: no
---
## Sub-clause map

- **9.1** Monitoring, measurement, analysis and evaluation — what to monitor and measure, methods, when, by whom, when results analysed, retain documented information.
- **9.2** Internal audit
  - **9.2.1** General — internal audits at planned intervals to verify the ISMS conforms to the org's own requirements and to ISO 27001 and is effectively implemented and maintained.
  - **9.2.2** Internal audit programme — plan, establish, implement and maintain audit programmes; define audit criteria and scope per audit; select auditors and conduct audits objectively and impartially; report results; retain documented information of programmes and audit results.
- **9.3** Management review
  - **9.3.1** General — top management shall review the ISMS at planned intervals.
  - **9.3.2** Management review inputs — eight required input categories.
  - **9.3.3** Management review results — decisions related to continual improvement and any need for changes to the ISMS; retain documented information.

## Requirements (reference)

Requirements: ISO/IEC 27001:2022 clause 9, Performance evaluation; text at https://www.iso.org/standard/27001 (licensed, not reproduced here).

## Changes from :2013

- **9.3.2 wording aligned with Annex SL.** Sub-items renumbered and slightly expanded (changes in interested-party needs as explicit input added at (c)).
- **9.2 split into 9.2.1 (general) and 9.2.2 (programme).** Annex SL alignment.
- **9.1 substantively unchanged.**

## Evidence artefacts an auditor expects

- **Monitoring and measurement plan / register** — a table listing each metric: what is measured, why, method, frequency, owner, target, current value, trend, action triggers.
- **Metrics dashboards / reports** — actual results, with history. Examples: patch SLA compliance %, phishing click rate, MFA coverage %, vulnerability scan critical findings, mean time to detect, mean time to respond, training completion rate.
- **Internal audit programme document** — multi-year plan covering the full ISMS scope across the cycle (typically all clauses and all Annex A controls within three years), with risk-weighted audit frequency.
- **Internal audit plans per audit** — scope, criteria, auditor name, dates, sampling approach.
- **Internal audit reports** — findings categorized (major nonconformity / minor nonconformity / observation / opportunity for improvement), with evidence references.
- **Auditor independence evidence** — auditor did not audit their own work; external internal auditor used where in-house auditors lack scope independence.
- **Management review schedule and minutes** — annual minimum, ideally semi-annual. Minutes capture the nine input categories explicitly and the resulting decisions.
- **Management review decision tracking** — actions assigned, owner, target date, status. Closure tracked back to next review.

## Typical audit observations

- **Metrics that nobody reads.** Dashboard exists but no evidence anyone uses the data to make decisions. Cl 9.1.f finding.
- **Metrics that measure activity, not effectiveness.** "We ran 12 phishing exercises" — but trend in click rate not tracked. Cl 9.1.b finding.
- **Internal audit scope incomplete over the cycle.** Three-year programme covers most clauses but skips Annex A.7 (physical) because "everyone is remote." Auditor probes: are remote endpoints in scope of A.7? If yes, finding.
- **Internal auditor not independent.** Engineering manager audits their own team. Cl 9.2.2.c finding.
- **External internal auditor without skills.** Contracted internal-audit firm sends junior auditors with no AI-system context. Audit reports are surface-level; certification auditor probes the depth.
- **Management review is a status meeting.** Minutes show project updates, no engagement with the nine required inputs. Cl 9.3.2 finding.
- **Action items from prior reviews not closed.** Same items appearing across three management reviews. Cl 9.3.3 + Cl 10.2 (corrective action effectiveness) findings.

## Common implementation gaps

- **Measurement plan ≠ security telemetry.** Operational telemetry (CPU, latency, error rate) is not the same as ISMS metrics (MFA coverage, training completion, control effectiveness). Both useful; both needed. Cl 9.1 expects the latter explicitly.
- **Internal audit as compliance ceremony.** Pre-cert internal audit run by the cert prep consultant who finds nothing — and the cert auditor finds plenty. Independence and competence in the internal auditor are load-bearing.
- **Management review timed for the audit.** Held annually one month before recertification audit. Cl 9.3.1 requires "planned intervals" — typically interpreted as at minimum annually; semi-annual or quarterly is better practice for fast-moving environments.
- **Decisions, not just discussions.** Cl 9.3.3 requires decisions captured. Minutes that summarize discussion without listing decisions fail this.

## SRE and AI-agent fit notes

- **Metrics for AI-system control effectiveness.** Examples:
  - Agent action audit log completeness (% of agent decisions with full input + output captured).
  - Prompt-injection test coverage (% of agent endpoints subjected to recent injection tests).
  - Tool-scope review cadence (% of agents with tool scope reviewed in last 90 days).
  - Vendor TOS version currency (model providers using TOS version matching SoA reference).
  - Model version drift (% of production endpoints on the SoA-referenced model version).
  - Human-in-the-loop override rate (frequency of human reversal of agent decisions, with trend).
- **Internal audit for AI controls.** Until ISO 42001 audit competence matures, internal audit teams typically lack the technical depth to substantively audit AI-system controls. Options: train an internal auditor on AI-system security; bring in a specialist external internal auditor on a project basis; explicitly note the gap in management review and accept the residual risk.
- **Management review inputs from AI operations.** Add:
  - Trend in agent incidents and near-misses.
  - Trend in vendor-side model behavior changes.
  - Status of AI risk register (alongside main risk register).
  - Status of ISO 42001 alignment work if relevant.
  - Threat intelligence specific to AI / agent ecosystem.
- **Management review cadence pressure.** AI ecosystem changes faster than the typical annual / semi-annual ISMS review. Either accept the lag and document the residual risk, or run a more frequent technical review feeding summarised input into the formal management review.

## Stefan-context implementation sketch

- Metrics: small, focused set. Examples: vault PII boundary violations (target zero), vendor API key age (target <90 days), agent audit-log retention (target 12 months, current value tracked monthly), federation peer trust attestation freshness, vault staleness percentage from `KNOWLEDGE-FRAMEWORK.md` thresholds.
- Internal audit: self-audit cycle for personal infra (lightweight); client-engagement audit triggered by contract.
- Management review: quarterly self-review at minimum, captured as a vault atom with the nine input categories.
- Independence concern: solo work has no internal-independence; treat client-side review or pre-certification consultant audit as the impartial third party.

## See also

- [[ISO 27001 Cluster|cluster MOC]] · [[ISO 27001 Clause 8 Operation]] · [[ISO 27001 Clause 10 Improvement]]
- [[ISO 27001 Family and Sector Variants]] (ISO 27004 measurement; ISO 27007 management systems auditing; ISO 27008 controls assessment)
