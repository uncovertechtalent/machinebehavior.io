title: ISO 27001 Clause 6 Planning
summary: The SoA is the most-cited single artefact in an ISO 27001 audit.
parent: iso-27001
order: 100
labels: clause-6, iso-27001, iso-clause
aliases: ISO 27001 Clause 6 | ISO 27001 Planning | ISO 27001 Risk Assessment | ISO 27001 Risk Treatment | ISO 27001 SoA | Statement of Applicability
type: iso-clause
created: 2026-05-12
updated: 2026-06-08
origin: pillars/iso-27001/ISO 27001 Clause 6 Planning.md
reviewed: no
---
## Sub-clause map

- **6.1** Actions to address risks and opportunities
  - **6.1.1** General — actions to address risks and opportunities considered when planning the ISMS.
  - **6.1.2** Information security risk assessment — define and apply a process.
  - **6.1.3** Information security risk treatment — define and apply a process, produce a Statement of Applicability, get risk-owner approval of the treatment plan and acceptance of residual risk.
- **6.2** Information security objectives and planning to achieve them.
- **6.3** Planning of changes — **new in :2022.**

## Key "shall" requirements (verbatim selections from :2022)

- 6.1.2: the org "shall define and apply an information security risk assessment process that:
  - a) establishes and maintains information security risk criteria that include:
    - 1) the risk acceptance criteria;
    - 2) criteria for performing information security risk assessments;
  - b) ensures that repeated information security risk assessments produce consistent, valid and comparable results;
  - c) identifies the information security risks: ... apply the risk assessment process to identify risks associated with the loss of confidentiality, integrity and availability for information within the scope of the information security management system; identify the risk owners;
  - d) analyses the information security risks: ... assess the potential consequences ... assess the realistic likelihood ... determine the levels of risk;
  - e) evaluates the information security risks: ... compare the results of risk analysis with the risk criteria ... prioritize the analysed risks for risk treatment."
- 6.1.3: the org "shall define and apply an information security risk treatment process to:
  - a) select appropriate ... risk treatment options ...
  - b) determine all controls that are necessary to implement the information security risk treatment option(s) chosen;
  - c) compare the controls determined in 6.1.3 b) above with those in Annex A and verify that no necessary controls have been omitted;
  - d) produce a Statement of Applicability that contains:
    - the necessary controls ... and justification for their inclusion;
    - whether the necessary controls are implemented or not;
    - the justification for excluding any of the Annex A controls;
  - e) formulate an information security risk treatment plan;
  - f) obtain risk owners' approval of the information security risk treatment plan and acceptance of the residual information security risks."
- 6.2: objectives shall "be consistent with the information security policy; be measurable (if practicable); take into account applicable information security requirements, and results from risk assessment and risk treatment; be monitored; be communicated; be updated as appropriate; be available as documented information."
- 6.3: "When the organization determines the need for changes to the information security management system, the changes shall be carried out in a planned manner."

## Changes from :2013

- **6.3 Planning of changes is new.** Previously planning of ISMS changes was implicit in 8.1 operational planning. :2022 surfaces it as a standalone clause, aligned with Annex SL update.
- **6.1.3.c wording tightened** — "compare the controls determined ... with those in Annex A and verify that no necessary controls have been omitted." :2013 wording was "compare the controls determined in 6.1.3 b) above with those in Annex A and verify that no necessary controls have been omitted."  Substance the same; auditor expectation unchanged.
- **6.2 added** subitems "be monitored" and "be available as documented information" (Annex SL alignment).

## The Statement of Applicability (SoA)

The SoA is the most-cited single artefact in an ISO 27001 audit. It is a table with one row per Annex A control (all 93 in :2022) listing:

- Control reference and title.
- Applicable (yes/no).
- Justification (if applicable: why; if not applicable: why not).
- Implementation status (implemented / partially / not yet).
- Reference to the implementing policy, procedure, or evidence.

The SoA is the bridge between the risk treatment plan (what the org will do) and the Annex A reference list (the recognized control catalog). Excluding controls is permitted; the justification must withstand auditor probing. "We do not handle physical assets" is a valid exclusion for a fully remote SaaS company. "We do not need monitoring" is not.

The SoA also extends beyond Annex A: if 6.1.3.b identifies necessary controls not in Annex A (e.g., AI-system specific controls), those are added to the SoA. Annex A is a floor reference, not a ceiling.

## Evidence artefacts an auditor expects

- **Risk assessment methodology document** — defines criteria, scales (likelihood, impact), thresholds, and the repeatable process. Cl 6.1.2.b ("consistent, valid and comparable results") is checked by re-running the process and seeing matching outputs.
- **Risk register** — actual risks identified, owners assigned, scored, with treatment decisions.
- **Risk treatment plan** — for each treated risk: chosen treatment (mitigate / accept / avoid / transfer), controls selected, target date, responsible role.
- **Statement of Applicability** — current version, dated, owner identified, including the new :2022 controls.
- **Risk owner approvals** — signed or otherwise auditable acceptance of residual risk.
- **Objectives register** — measurable security objectives with target values, current values, owner, review cadence. Examples: "phishing simulation click rate < 5% in 12 months," "patch SLA met for 95% of critical CVEs within 7 days," "100% of new agents have documented threat models before production deployment."
- **Change-planning records** (new for :2022) — evidence the change is planned (not just executed): change management tickets, architectural review records, security review sign-off.

## Typical audit observations

- **Risk register is a control list, not a risk list.** Each row reads "lack of MFA," "lack of patching," "lack of training." These are control gaps, not risks. A risk has a threat agent, an asset, a vulnerability, and a consequence. Major nonconformity if pervasive.
- **Risk scoring not repeatable.** Two assessors against the same asset arrive at different scores because the criteria are vague. Cl 6.1.2.b finding.
- **SoA exclusions thin.** "A.7.4 Physical security monitoring — not applicable, we are remote." Auditor probes: do remote employees have CCTV / smart cameras / door sensors in home offices the company has authorized? The exclusion may need narrowing.
- **SoA out of date.** Still on :2013 numbering; A.18.1.4 cited instead of A.5.34 (PII protection). Major nonconformity post-transition-deadline (31 October 2025).
- **Objectives are activities, not outcomes.** "Run a phishing exercise" is an activity. "Achieve < 5% click rate" is an outcome. Cl 6.2 expects measurable objectives — outcomes are measurable in the relevant sense.
- **Change planning not visible.** A new agent system deployed to production with no documented change record. Cl 6.3 nonconformity.

## Common implementation gaps

- **Asset register absent.** Risks reference "the production database" without a clear asset list. Cl 6.1.2.c risk identification depends on knowing the assets in scope. Often a Cl 8 or A.5.9 finding feeding back to 6.
- **Risk treatment plan = SoA copy.** The treatment plan should be richer than the SoA: it has time-boxed actions, not just controls.
- **Residual risk acceptance is a rubber stamp.** Risk owner signs without seeing the residual-after-treatment score. Cl 6.1.3.f expects informed acceptance.
- **Objectives align to certification, not security.** "Achieve and maintain ISO 27001 certification" is meta and circular as an objective. Useful objectives speak to risk reduction or capability improvement.

## SRE and AI-agent fit notes

- **AI / agent risks belong in the risk register.** Examples:
  - Prompt injection causing autonomous agent to exfiltrate data.
  - Model vendor outage cascading into customer-facing service.
  - Agent-generated audit logs being incomplete or tamperable.
  - Tool-use scope creep (an agent given file-read access misused for file-write).
  - Federated workspace synchronization integrity (bd federation between machines).
  - Vendor SaaS API key compromise via developer machine.
- **Risk owners for AI controls.** Often unclear. Default to the engineering lead for the system; escalate to CISO / management representative for cross-system concerns.
- **New Annex A :2022 controls especially relevant for AI work:**
  - **A.5.7 Threat intelligence** — covers feeds about AI-specific threats, prompt-injection campaigns, model-supply-chain news.
  - **A.5.23 Information security for use of cloud services** — covers model-as-a-service vendor relationships.
  - **A.8.9 Configuration management** — covers model versions, system prompts, agent tool scopes.
  - **A.8.10 Information deletion** — covers training-data and vendor-side retention.
  - **A.8.11 Data masking** — relevant when shipping data to model APIs.
  - **A.8.12 Data leakage prevention** — relevant for AI feature responses and tool-use boundaries.
  - **A.8.16 Monitoring activities** — covers agent action logging.
  - **A.8.28 Secure coding** — extended to "secure prompting" and tool-scope definitions.
- **SoA extensions for AI.** Add company-specific controls referencing OWASP LLM Top 10, NIST AI RMF profile, or ISO 42001 alignment. Document them as additions to A.5.7, A.8.16, A.8.28 with a clear rationale.

## Stefan-context implementation sketch

- Risk methodology: lightweight, qualitative, with named scoring criteria (low / medium / high on impact and likelihood with explicit definitions per criteria). FAIR-quantitative reserved for high-stakes client risks.
- Risk register: maintained as a bd query / markdown atom. Linked to vault classification (`whiteout-kb/` vs `work-kb/` vs client data).
- SoA: built once against :2022 Annex A; updated when scope, vendor list, or threat model shifts.
- Objectives: e.g., "vault PII never leaves whiteout-kb classification boundary," "vendor SaaS API keys rotated within 90 days," "agent audit logs retained 12 months and tamper-evident."
- Change planning: bd issue per significant ISMS change (new vendor, new agent, scope shift, federation peer add).

## See also

- [[ISO 27001 Cluster|cluster MOC]] · [[ISO 27001 Clause 5 Leadership]] · [[ISO 27001 Clause 7 Support]] · [[ISO 27001 Clause 8 Operation]]
- [[ISO 27001 Annex A.5 Organizational Controls]] (A.5.7 threat intelligence, A.5.9 inventory of information and other associated assets, A.5.12 classification, A.5.23 cloud)
- [[ISO 27001 Family and Sector Variants]] (ISO 27005 risk management methodology)
