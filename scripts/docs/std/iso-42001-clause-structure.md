title: ISO 42001 Clause Structure
summary: Mandatory clauses 4-10 of ISO/IEC 42001:2023.
parent: iso-42001
order: 100
labels: iso-42001, iso-clause
aliases: ISO 42001 Clause Structure | ISO 42001 Clauses | ISO 42001 Cl 4-10 | ISO 42001 Mandatory Clauses
type: iso-clause
created: 2026-05-12
updated: 2026-06-08
origin: pillars/iso-42001/ISO 42001 Clause Structure.md
reviewed: no
---
> Mandatory clauses 4-10 of ISO/IEC 42001:2023. Annex SL aligned — shared structure with ISO 9001, ISO 14001, ISO 27001, ISO 22301, ISO 27701. Most of the clause text mirrors the harmonized Annex SL wording; AI-specific content lives in the supporting Annex A controls and in select clause additions.

## Sub-clause map

Following Annex SL, with AI-specific additions where relevant:

- **Clause 4 — Context of the organization**
  - 4.1 Understanding the organization and its context
  - 4.2 Understanding the needs and expectations of interested parties
  - 4.3 Determining the scope of the AIMS
  - 4.4 AI Management System
- **Clause 5 — Leadership**
  - 5.1 Leadership and commitment
  - 5.2 AI policy
  - 5.3 Organizational roles, responsibilities and authorities
- **Clause 6 — Planning**
  - 6.1 Actions to address risks and opportunities
    - 6.1.1 General
    - 6.1.2 AI risk assessment
    - 6.1.3 AI risk treatment
    - 6.1.4 AI system impact assessment
  - 6.2 AI objectives and planning to achieve them
  - 6.3 Planning of changes
- **Clause 7 — Support**
  - 7.1 Resources
  - 7.2 Competence
  - 7.3 Awareness
  - 7.4 Communication
  - 7.5 Documented information
- **Clause 8 — Operation**
  - 8.1 Operational planning and control
  - 8.2 AI risk assessment
  - 8.3 AI risk treatment
  - 8.4 AI system impact assessment
- **Clause 9 — Performance evaluation**
  - 9.1 Monitoring, measurement, analysis and evaluation
  - 9.2 Internal audit
  - 9.3 Management review
- **Clause 10 — Improvement**
  - 10.1 Continual improvement
  - 10.2 Nonconformity and corrective action

## What is AI-specific in the clause text (vs harmonized Annex SL)

Most clause-level wording mirrors ISO 27001 / ISO 9001 with "AI" substituted for the topic. Distinctive AI-specific clause content:

- **6.1.4 AI system impact assessment** — new sub-clause introducing AI impact assessment as a planning activity. Distinct from risk assessment; covers fairness, robustness, transparency, accountability, environmental, societal impact.
- **8.4 AI system impact assessment** — operational application of 6.1.4; impact assessments at planned intervals and when significant changes occur.
- **5.2 AI policy** — explicit AI policy requirement (not just "information security policy" relabeled). Policy content expected to cover trustworthiness commitments, lifecycle approach, third-party relationships.
- **6.2 AI objectives** — objectives explicitly tied to AI commitments; "be measurable (if practicable)" softer than typical Annex SL wording recognizing AI metrics maturity gap.

The other sub-clause text mirrors Annex SL conventions. Mature ISO 27001 implementations carry most of the structural work; AI-specific content overlays at risk assessment, treatment, impact assessment, and Annex A controls.

## Evidence artefacts an auditor expects

Aligned with ISO 27001 plus AI-specific additions:

- **Context analysis** — including AI-specific external and internal issues (regulatory, ethical, societal, technological).
- **Interested parties register** — including AI-specific stakeholders (data subjects, affected communities, regulators, ethics advisors).
- **AIMS scope statement** — boundaries, AI systems in scope, sites, business processes, interfaces.
- **AI policy** — board-approved, communicated, periodically reviewed.
- **Roles register** — AI-specific roles (AI risk owner, AI ethics lead, AI impact assessment owner, AI system owners).
- **AI risk methodology** — adapted from general risk methodology with AI-specific risk categories.
- **AI risk register** — risks identified, owners, scores, treatment decisions.
- **Statement of Applicability** — Annex A controls, applicability, justification, implementation status.
- **AI system impact assessment records** — for each significant AI system in scope.
- **AI objectives register** — measurable where practicable, with owners and review cadence.
- **Documented information set** — policies, procedures, work instructions, records.
- **Internal audit programme and reports**.
- **Management review minutes**.
- **Nonconformity / corrective action records**.

## Typical audit observations (early audit-practice patterns)

- **AI policy is generic.** "We commit to trustworthy AI" without organization-specific commitments. Auditor probes for substance.
- **Impact assessment as ceremony.** Performed once per system at deployment, never revisited despite significant changes. Cl 8.4 expects ongoing assessment.
- **Risk register vs impact assessment confusion.** Risk and impact treated as the same activity. The standard distinguishes: risk is about uncertainty affecting objectives; impact is about consequences of AI system operation on affected parties.
- **Third-party (model provider) relationships under-evidenced.** SoA cites Annex A control on third-party relationships; evidence package is thin.
- **Lifecycle stage tracking missing.** AI systems not classified by lifecycle stage; controls applied uniformly. The lifecycle-stage-aware control selection is part of the framework intent.
- **AI competence not evidenced.** Cl 7.2 expects competence for AIMS-relevant roles. Generic ML / data-science credentials not always sufficient; AI risk and governance competence is distinct.

## Common implementation gaps

- **Treating ISO 42001 as "ISO 27001 with AI controls bolted on".** The AI risk and impact assessment processes are distinct from infosec risk; conflating them produces shallow coverage.
- **Generative-AI-specific concerns missed.** The framework is AI-general; generative-AI-specific concerns (prompt injection, hallucination, autonomous-agent risks) need to be mapped into the risk register and Annex A controls by the implementer.
- **AI system inventory absent.** Like asset inventory under ISO 27001, AI system inventory is foundational. Often missing or partial.
- **No bridge to NIST AI RMF / OWASP LLM Top 10 / MITRE ATLAS.** ISO 42001 is the management-system layer. The operational threat content lives in NIST / OWASP / MITRE. Mature implementations reference both.

## SRE and AI-agent fit notes

- **Operational AI risks belong in 6.1.2 / 8.2 risk assessment.** Examples (drawing from OWASP LLM Top 10 2025):
  - Prompt injection leading to data exfiltration or tool misuse
  - Sensitive information disclosure via model output
  - Supply chain compromise of model, training data, or dependencies
  - Data and model poisoning
  - Improper output handling allowing downstream injection
  - Excessive agency (overly broad tool scope, missing kill switches)
  - System prompt leakage
  - Vector / embedding weaknesses in RAG architectures
  - Misinformation generation and downstream effect
  - Unbounded consumption (token spend, compute, financial DOS)
- **AI system impact assessment for agent systems.** Specific dimensions:
  - Fairness across user populations
  - Robustness against adversarial inputs
  - Transparency of agent actions and decisions
  - Accountability chain when agent acts autonomously
  - Environmental impact (compute, energy)
  - Societal impact (employment, information ecosystem)
- **AI system lifecycle mapping.** Specific to agent systems:
  - Planning: scope, capabilities, constraints
  - Design and development: system prompt, tool scope, model selection, evaluation harness
  - V&V: prompt-injection testing, output validation, evaluation against acceptance criteria
  - Deployment: gradual rollout, monitoring, audit logging
  - Operation and monitoring: continued evaluation, vendor-side change detection, incident response
  - Re-evaluation: at significant changes (model version, tool scope, vendor behavior)
  - Retirement: deactivation, audit log preservation, knowledge transfer

## Stefan-context implementation sketch

- AI policy: short statement covering vault classification × AI use, vendor authorization, agent action scope, human-in-the-loop policy, kill-switch authority.
- Roles: solo / small-team operator; AI roles concentrate; document the model.
- Risk methodology: lightweight, qualitative; AI risks added as a sub-register linked to main risk register.
- Impact assessment: per significant AI feature / agent; vault atom format.
- Documented information: vault git history covers most; supplement with vendor relationship records, audit log retention proofs, evaluation results.

## See also

- [[ISO 42001 Cluster|cluster MOC]] · [[ISO 42001 Annex A Controls]] · [[ISO 42001 AI System Lifecycle]] · [[ISO 42001 vs ISO 27001 Integration]]
- [[ISO 27001 Clause 4 Context]] · [[ISO 27001 Clause 6 Planning]] (sibling clause structure)
