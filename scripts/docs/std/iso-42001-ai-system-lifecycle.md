title: ISO 42001 AI System Lifecycle
summary: The AI system lifecycle is the operational concept at the heart of ISO 42001.
parent: iso-42001
order: 100
labels: iso-42001, iso-concept
aliases: ISO 42001 Lifecycle | ISO 42001 AI System Lifecycle | AI System Lifecycle | ISO 5338 Lifecycle
type: iso-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/iso-42001/ISO 42001 AI System Lifecycle.md
reviewed: no
---
> The AI system lifecycle is the operational concept at the heart of ISO 42001. Annex A.6 controls structure around it; the lifecycle informs impact assessment, risk treatment, and ongoing operation. ISO/IEC 5338:2023 (AI system life cycle processes) is the companion deep-dive standard.

## Lifecycle stages

ISO 42001 (drawing from ISO 5338) describes seven stages:

1. **Inception** — initial idea, business case, feasibility, high-level scope.
2. **Design and development** — architecture, model selection or training, system prompt, tool scope, evaluation framework, initial implementation.
3. **Verification and validation** — testing against requirements, fairness assessment, robustness testing, evaluation against impact-assessment criteria.
4. **Deployment** — release to production, gradual rollout, user onboarding.
5. **Operation and monitoring** — ongoing service delivery, behavioral monitoring, performance management, audit logging.
6. **Re-evaluation** — periodic review, triggered re-assessment for significant changes (model version, vendor behavior, regulatory change, observed incidents).
7. **Retirement** — deactivation, data handling, audit log preservation, knowledge transfer.

Stages are not strictly sequential. AI systems frequently iterate through design → V&V → deployment → monitoring → re-evaluation → back to design. Retirement may occur from any stage.

## Per-stage activities and controls

### Inception

Activities: business case development, feasibility assessment, initial scope definition, high-level resource estimation, initial risk identification.

Annex A controls active: A.5.2 (impact assessment process — start here), A.2 (policies guide scope decisions), A.10 (third-party identification if vendor AI considered).

Common outputs: feasibility document, initial impact-assessment scope, initial AI system description.

### Design and development

Activities: detailed requirements, architecture, model selection (build vs buy), system prompt engineering, tool scope definition, evaluation harness construction, training (if applicable), initial implementation.

Annex A controls active: A.6.2.2 (requirements), A.6.2.3 (design documentation), A.7 (data for development), A.4 (resources documentation), A.10 (vendor selection and contracts).

Common outputs: AI system architecture, system prompt (versioned), tool definitions, evaluation harness, training records (if applicable), vendor contracts.

For agent systems: the system prompt and tool scope are first-class design artefacts. Version-controlled, peer-reviewed, security-reviewed.

### Verification and validation

Activities: testing against functional requirements, fairness testing, robustness testing (adversarial inputs, prompt injection, jailbreaks), evaluation against impact-assessment criteria, acceptance testing.

Annex A controls active: A.6.2.4 (V&V), A.5.3 (impact assessment documentation), A.7.4 (data quality for testing).

Common outputs: V&V report, evaluation results, fairness assessment, robustness assessment, sign-off for deployment.

For agent systems: prompt-injection test suite results, tool-misuse test results, output validation results.

### Deployment

Activities: production deployment, gradual rollout (canary, percentage-based), monitoring infrastructure activation, user onboarding, communication to interested parties.

Annex A controls active: A.6.2.5 (deployment), A.8 (information for interested parties), A.6.2.8 (event logging activation).

Common outputs: deployment record, rollout plan execution, monitoring dashboard activation, user-facing documentation.

For agent systems: gradual user-cohort enablement, behavioral monitoring on, audit logging on, kill-switch tested.

### Operation and monitoring

Activities: service delivery, behavioral monitoring, performance management, incident response, audit logging, ongoing evaluation, vendor-side change detection.

Annex A controls active: A.6.2.6 (operation and monitoring), A.6.2.8 (event logging ongoing), A.8.4 (incident communication), A.10.3 (supplier monitoring).

Common outputs: monitoring data, performance reports, incident records, vendor-relationship records.

For agent systems: agent action audit logs, anomaly detection alerts, vendor-model-version change tracking, behavioral baseline comparisons.

### Re-evaluation

Activities: periodic review of the AI system, triggered re-assessment for significant changes, updated impact assessment, risk reassessment.

Annex A controls active: A.5 (impact reassessment), A.6.2.4 (re-V&V where appropriate).

Common triggers for re-evaluation:

- Model version change (vendor-side or own-trained)
- Tool scope change for agent systems
- Vendor behavior change observed in monitoring
- Regulatory change (e.g., AI Act applicability shifts)
- Observed incident or near-miss
- Significant change in user population, use case, or business context
- Periodic (at minimum annually)

Common outputs: re-evaluation report, updated impact assessment, updated risk register entries, change decisions (continue / modify / retire).

### Retirement

Activities: deactivation, data handling (deletion or archive per policy), audit log preservation, knowledge transfer, vendor relationship closure.

Annex A controls active: A.6.2 lifecycle as a whole, A.7 (data handling at retirement), A.10 (vendor relationship closure).

Common outputs: retirement record, data disposition record, archive of audit logs (per retention policy), notification to affected parties.

For agent systems: deactivation procedure, vendor API key revocation, audit log archival, post-retirement monitoring of any residual effects.

## Lifecycle vs ML lifecycle / MLOps

ISO 42001's AI system lifecycle largely subsumes the typical MLOps lifecycle (data → train → validate → deploy → monitor → retrain) but extends it:

- **Wider scope**: covers non-ML AI (rule-based, hybrid systems), generative AI, agent systems — not just supervised ML.
- **Lifecycle inception is explicit**: business case and feasibility precede development. MLOps frequently assumes the development decision is already made.
- **Impact assessment is integrated**: not a separate "ethics review" — part of inception and design.
- **Retirement is explicit**: MLOps often handles retirement implicitly. ISO 42001 makes it a controlled process.
- **Vendor AI use is covered**: MLOps typically focuses on org-trained models. ISO 42001 covers model-API consumption as well.

Practical implication: existing MLOps practice maps cleanly into ISO 42001 lifecycle with extensions for inception, impact assessment integration, retirement, and vendor AI handling.

## Lifecycle vs agent-system development

For agent systems (LLM + tools + system prompt + retrieval), the lifecycle stages adapt:

- **Inception**: agent use-case definition, capability requirements, tool scope, autonomy level decision.
- **Design and development**: system prompt engineering, tool definitions, evaluation harness, model selection, retrieval architecture (RAG), guardrails, kill-switches.
- **V&V**: prompt-injection testing, tool-misuse testing, output validation testing, eval suite execution, red-team exercises.
- **Deployment**: limited-cohort rollout, monitoring on, human-in-the-loop initially, transition to lower oversight as confidence grows.
- **Operation and monitoring**: agent action logging, behavioral monitoring, vendor-side change detection, ongoing eval suite execution.
- **Re-evaluation**: triggered by model version updates, vendor TOS changes, incidents, user feedback, periodic.
- **Retirement**: agent deactivation, audit log archival, vendor relationship cleanup.

## Common implementation patterns

- **Lifecycle as project phases**: organizations sometimes implement lifecycle stages as gated project phases (waterfall-style). Works for novel high-stakes systems; over-rigid for iterative AI development.
- **Lifecycle as concurrent activities**: more typical. The org operates the lifecycle as overlapping ongoing activities — V&V continues during operation, re-evaluation feeds back into design.
- **Stage gates**: some orgs introduce decision gates between stages (e.g., V&V exit criteria before deployment). Useful for high-impact systems; ceremonial for low-stakes ones.
- **Per-AI-system lifecycle tracking**: each AI system in the inventory has a lifecycle-stage label. Auditor uses this to sample evidence.

## SRE and AI-agent fit notes

### Lifecycle as SRE planning vocabulary

The seven lifecycle stages bridge AI / ML practice to SRE planning:

- Inception: design review, capacity planning input
- Design and development: production readiness review preparation
- V&V: pre-production testing, load testing, chaos testing for AI components
- Deployment: SRE-coordinated rollout, canary deployment
- Operation and monitoring: SRE-led observability, alerting, on-call coverage
- Re-evaluation: SRE-input post-incident review, error-budget consumption review
- Retirement: SRE-coordinated decommissioning

### Lifecycle as audit-evidence-organization vocabulary

For audit purposes, evidence is more navigable when organized by lifecycle stage:

- One folder per AI system, sub-folders per lifecycle stage, evidence collected as the stage executes.
- Stage-stamped: each evidence item carries its lifecycle stage.
- Cross-stage evidence (e.g., ongoing audit logs) clearly identified.

## Stefan-context implementation sketch

For solo / small-team work building agent systems on top of model APIs:

- Inception: bd issue per significant agent, capturing scope, capability requirements, autonomy level.
- Design and development: system prompt and tool scope in vault under version control; evaluation harness as a code artefact.
- V&V: lightweight prompt-injection and tool-misuse testing before deployment.
- Deployment: gradual personal-use rollout, then client-engagement scoped use, then broader use as confidence grows.
- Operation and monitoring: bd activity captures use; vault git log captures changes; periodic self-review.
- Re-evaluation: triggered by model version changes from Anthropic, OpenCode plugin updates, observed friction.
- Retirement: explicit deactivation, audit log preserved in vault git history.

## See also

- [[ISO 42001 Cluster|cluster MOC]] · [[ISO 42001 Clause Structure]] · [[ISO 42001 Annex A Controls]]
- ISO/IEC 5338:2023 (companion lifecycle deep-dive standard)
- [[OWASP LLM Top 10 Cluster]] (operational threats relevant per lifecycle stage)
