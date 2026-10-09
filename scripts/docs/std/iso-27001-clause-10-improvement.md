title: ISO 27001 Clause 10 Improvement
summary: ISO 27001 Clause 10 Improvement, from the knowledge vault.
parent: iso-27001
order: 100
labels: clause-10, iso-27001, iso-clause
aliases: ISO 27001 Clause 10 | ISO 27001 Improvement | ISO 27001 Nonconformity | ISO 27001 Corrective Action | ISO 27001 Continual Improvement
type: iso-clause
created: 2026-05-12
updated: 2026-06-08
origin: pillars/iso-27001/ISO 27001 Clause 10 Improvement.md
reviewed: no
---
## Sub-clause map

- **10.1** Continual improvement — the org shall continually improve the suitability, adequacy and effectiveness of the ISMS.
- **10.2** Nonconformity and corrective action.


## Key "shall" requirements (verbatim selections from :2022)

- 10.1: "The organization shall continually improve the suitability, adequacy and effectiveness of the information security management system."
- 10.2: "When a nonconformity occurs, the organization shall:
  - a) react to the nonconformity, and as applicable:
    - 1) take action to control and correct it;
    - 2) deal with the consequences;
  - b) evaluate the need for action to eliminate the cause(s) of the nonconformity, in order that it does not recur or occur elsewhere, by:
    - 1) reviewing the nonconformity;
    - 2) determining the causes of the nonconformity;
    - 3) determining if similar nonconformities exist, or could potentially occur;
  - c) implement any action needed;
  - d) review the effectiveness of any corrective action taken;
  - e) make changes to the information security management system, if necessary.
  Corrective actions shall be appropriate to the effects of the nonconformities encountered.
  The organization shall retain documented information as evidence of:
  - the nature of the nonconformities and any subsequent actions taken;
  - the results of any corrective action."

## Changes from :2013

- **Sub-clauses reversed in order** (continual improvement now 10.1, nonconformity now 10.2). Annex SL convention.
- **Wording aligned with Annex SL.** No substantive change in expectation; the 5-step corrective action structure (react, evaluate cause, implement, review effectiveness, change ISMS if needed) is preserved.

## Evidence artefacts an auditor expects

- **Nonconformity register / log** — every nonconformity from internal audits, external audits, incidents, customer complaints, regulator findings, self-identified gaps. Each with status (open / in progress / closed), owner, target date, root cause, corrective action, effectiveness verification.
- **Root-cause analysis records** — for each significant nonconformity. Method (5 Whys, Ishikawa, Bowtie, FMEA) less important than the depth.
- **Corrective action records** — what was done, when, by whom, with effectiveness verification (re-testing, re-auditing, sustained metric improvement) and a date.
- **Continual improvement initiatives** — initiatives that improve effectiveness without being responses to specific nonconformities. Examples: tool consolidation, training rollout, vulnerability scanning maturity uplift, threat modelling adoption.
- **Trend data** — across multiple cycles, showing the management system actually changing. Stable nonconformity counts over years suggest improvement is theoretical.

## Typical audit observations

- **Corrective action = recurrence.** Same nonconformity from prior audit cycle, "corrected" by re-training the same person who failed, recurring 12 months later. Cl 10.2.b root-cause analysis was inadequate.
- **Root cause = "human error" only.** Stops at the proximate cause. Cl 10.2.b expects "causes" (plural) and exploration. The "five whys" of human error usually surface a process, training, design, or staffing issue.
- **Effectiveness review missing.** Action taken, marked closed, no verification that the issue does not recur. Cl 10.2.d finding.
- **No continual improvement beyond nonconformities.** Management system only changes when external auditor finds something. Cl 10.1 expects proactive improvement; the absence is a finding for mature audits.
- **Action backlog growing.** Nonconformity register has 40 open items, 25 overdue. Pattern issue, raises 9.3 management-review effectiveness questions too.

## Common implementation gaps

- **"Corrective" vs "preventive" action conflation.** :2013 had "preventive action" as a separate concept; :2022 (Annex SL) folded preventive thinking into the management system as a whole. Some legacy procedures still distinguish; auditors typically accept either as long as the substance is there.
- **Severity-blind treatment.** Every nonconformity treated as equal regardless of impact. Minor doc-control gap gets the same Gantt-chart treatment as a missing-MFA control. Cl 10.2 corrective action shall be "appropriate to the effects of the nonconformities" — proportional response is required.
- **Incident-to-nonconformity link missing.** Incidents (A.5.24-A.5.28) trigger lessons learned; lessons-learned outputs should feed the nonconformity log under 10.2.b.3 ("similar nonconformities exist or could potentially occur"). Many orgs run incident management and 10.2 corrective action as separate streams.
- **Improvement projects with no metric.** "We're maturing our threat modelling capability" — but no measurement of where it started, where it is now, or where it is targeted. Cl 10.1 wants improvement, which is observable.

## SRE and AI-agent fit notes

- **AI-related nonconformities will be novel categories.** Examples emerging:
  - Agent acted outside documented tool scope (control gap or scope definition gap).
  - Vendor model behavior drift broke a documented control assumption.
  - Audit log for agent action incomplete (missing input context or tool-call output).
  - Prompt-injection succeeded in test or production.
  - Customer PII exfiltrated via model response when controls assumed it could not.
  - System prompt drift between documented version and deployed version.
- **Root cause depth for AI nonconformities.** "The agent did the wrong thing" is the proximate cause. Deeper: model behavior change without monitoring, tool scope too broad, system prompt not version-controlled, no human-in-the-loop on the relevant action class, vendor TOS change not surfaced to the SoA owner. Each implies different corrective action.
- **Continual improvement targets for AI-system work.** Examples: agent action audit-log completeness from 70% to 95% within Q3; prompt-injection test suite coverage of agent endpoints from 40% to 100% within 6 months; tool-scope review cadence reduced from quarterly to monthly for autonomous agents.
- **Vendor-side nonconformity.** When the model provider changes behavior in a way that breaks your control assumption, that is a nonconformity in your ISMS (you assumed something that turned out untrue). Corrective action includes both updating the assumption and reviewing the supplier-controls process that missed the change signal.

## Stefan-context implementation sketch

- Nonconformity log: bd issues tagged with "iso-nonconformity" or similar. Each links to evidence (incident bd, audit finding, self-identified gap).
- Root-cause analysis: lightweight, captured in the bd issue notes field.
- Effectiveness verification: a follow-up bd issue scheduled 30-90 days after closure to verify recurrence has not happened.
- Continual improvement: tracked in vault under SRE/patterns or via management-review atoms; not every improvement needs a formal bd issue, but ones with measurable targets do.
- Severity calibration: critical (impacts client data or vault PII), major (impacts ISMS effectiveness), minor (impacts ISMS efficiency), observation (no current impact but worth tracking).

## See also

- [[ISO 27001 Cluster|cluster MOC]] · [[ISO 27001 Clause 9 Performance Evaluation]]
- [[ISO 27001 Annex A.5 Organizational Controls]] (A.5.24-A.5.28 information security incident management)
- [[ISO 27001 Family and Sector Variants]] (ISO 27035 incident management; ISO 27007 audit guidance)
