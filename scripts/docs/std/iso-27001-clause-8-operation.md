title: ISO 27001 Clause 8 Operation
summary: ISO 27001 Clause 8 Operation, from the knowledge vault.
parent: iso-27001
order: 100
labels: clause-8, iso-27001, iso-clause
aliases: ISO 27001 Clause 8 | ISO 27001 Operation | ISO 27001 Operational Planning
type: iso-clause
created: 2026-05-12
updated: 2026-06-08
origin: pillars/iso-27001/ISO 27001 Clause 8 Operation.md
reviewed: no
---
## Sub-clause map

- **8.1** Operational planning and control — plan, implement and control the processes needed to meet ISMS requirements and to implement actions determined in Cl 6.
- **8.2** Information security risk assessment — perform risk assessments at planned intervals or when significant changes are proposed or occur.
- **8.3** Information security risk treatment — implement the risk treatment plan; retain documented information of the results.

## Changes from :2013

- **8.1 final sentence on externally provided processes was added** in :2022. ":2013" structure had this implicit through Annex A controls only. :2022 makes the operational-control obligation explicit for outsourced processes — this includes cloud services and managed-service-provider relationships.
- **8.2 and 8.3 effectively unchanged.**

## Evidence artefacts an auditor expects

- **Operating procedures** for ISMS-critical processes: change management, incident response, vulnerability management, identity and access management, backup and restore, business continuity testing, supplier onboarding and offboarding, asset disposal.
- **Process criteria documentation** — for each ISMS-critical process, the criteria that define a properly-executed instance (e.g., "all changes to production must have peer review, security approval where applicable, and rollback plan").
- **Process execution records** — change tickets, incident records, vulnerability scan reports, access reviews, restoration test results.
- **Outsourced-process control evidence** — supplier security questionnaires, third-party audit reports (SOC 2 Type 2, ISO 27001 cert, ISAE 3402), DPAs, contractual security clauses, monitoring of supplier performance against agreed metrics.
- **Risk reassessment cadence proof** — annual full reassessment, plus triggered reassessments for significant changes (new product, new technology, new regulation, post-incident).
- **Risk-treatment-plan execution proof** — Gantt or ticket history showing planned treatments moving to closure.

## Typical audit observations

- **Procedure-to-practice drift.** Procedure says "all production access requires MFA" but the auditor finds a service account using static credentials. Either the procedure is wrong (then update it) or the practice is wrong (then fix it). The drift itself is the finding.
- **Risk reassessment cadence missed.** "We do it annually" — last one was 14 months ago. Minor nonconformity.
- **No reassessment after significant change.** New cloud provider onboarded six months ago, no triggered risk assessment. Cl 8.2 finding.
- **Supplier controls weak.** Vendor onboarding tick-box exercise, no ongoing monitoring. Cl 8.1 final-sentence finding.
- **Process-criteria absent.** Procedures describe steps but not what makes execution acceptable (e.g., approval thresholds, SLA targets, deviation handling). Cl 8.1.a finding.
- **Risk treatment plan execution stalled.** Plan says "implement MFA company-wide by Q2 2025" — Q1 2026 audit finds rollout 60% complete with no revised plan. Cl 8.3 finding; cascades to Cl 10.2 (corrective action).

## Common implementation gaps

- **Outsourced-process scope underestimated.** SaaS apps, payroll providers, ITSM platforms, monitoring tools, contract developers, hosted CI / CD — all are externally provided processes for ISMS purposes. Treating only cloud infrastructure providers as "outsourced" misses the rest.
- **Change management is for product changes only.** ISMS changes (new policy, new control implementation, vendor swap) are not run through the change-management process. Cl 8.1 expects criteria-based control of all processes — including the management system itself.
- **Risk reassessment is a desk exercise.** Annual reassessment that rubber-stamps last year's register without testing whether risks changed. Auditor probes by comparing year-over-year deltas vs known business / threat changes.
- **Treatment plan is a wish list.** Items without owner, date, or budget. Cl 8.3 expects implementation, which expects executability.

## SRE and AI-agent fit notes

- **Externally provided processes for AI work** include: model APIs (Anthropic, OpenAI, Google, Cohere), embedding APIs, vector DB SaaS, model hosting platforms, agent framework SaaS (LangSmith, others), CI / CD with AI-feature builds, security scanning SaaS that touches code with AI-feature implementations. Each is an Cl 8.1 final-sentence supplier; each gets supplier-controls evidence.
- **Risk reassessment triggers in AI work.** New trigger types specific to AI:
  - Model version change (provider-side) — agent behavior may shift.
  - Tool-scope change — new capability added to an agent.
  - New data source connected to retrieval / RAG — new threat surface.
  - Vendor TOS / DPA change — data handling commitments shift.
  - Public incident at a model provider — reassess vendor risk.
- **Operating procedures for autonomous-agent work.** Need procedures for: deploying new agents, scoping agent tool access, monitoring agent behavior, handling agent-induced incidents, rolling back agent decisions, retiring an agent. Most orgs lack these as of 2026.
- **Documented results of risk-treatment execution.** Especially important for AI controls because the controls themselves are new (post-:2022 + post-AI-shift) and audit-precedent is thin.

## Stefan-context implementation sketch

- Process inventory: vault sync, agent deployment, vendor API authorization, federation peer onboarding, incident response, backup / restore (Dolt for bd, git for vault).
- Process criteria: documented in atom-level conventions (e.g., AGENTS.md hard rules), bd workflow rules.
- Outsourced processes: model providers (Anthropic, OpenAI), Cloudflare, AWS (headscale), Apple iCloud (selective), hardware vendors, payment processors.
- Risk reassessment triggers: vendor TOS changes (monitored manually), model version major releases, new client engagement onboarding, new federation peer or machine, new vault corpus added.
- Treatment-plan execution: tracked as bd issues with priority and target dates.

## See also

- [[ISO 27001 Cluster|cluster MOC]] · [[ISO 27001 Clause 6 Planning]] · [[ISO 27001 Clause 9 Performance Evaluation]]
- [[ISO 27001 Annex A.5 Organizational Controls]] (A.5.19-A.5.23 supplier relationships, ICT services, cloud services)
- [[ISO 27001 Annex A.8 Technological Controls]] (A.8.9 configuration management, A.8.32 change management)
- [[SRE/runbooks/Service Outage Response]] (operational evidence example)
