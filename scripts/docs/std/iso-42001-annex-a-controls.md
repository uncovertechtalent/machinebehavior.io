title: ISO 42001 Annex A Controls
summary: Reference control set for ISO/IEC 42001:2023 Annex A.
parent: iso-42001
order: 100
labels: annex-a, iso-42001
aliases: ISO 42001 Annex A | ISO 42001 Controls | ISO 42001 Annex A Controls
type: annex-a
created: 2026-05-12
updated: 2026-06-08
origin: pillars/iso-42001/ISO 42001 Annex A Controls.md
reviewed: no
---
> Reference control set for ISO/IEC 42001:2023 Annex A. Approximately 38 controls organized into 10 control-objective areas. The Statement of Applicability (SoA, required by Cl 6.1.3.d equivalent) records which controls apply, with implementation status and justification for any exclusions. Annex B provides implementation guidance per control.

## How to read this atom

Each section below corresponds to one Annex A control objective area. The headline controls within are listed with brief notes covering purpose, typical implementation, and SRE / AI-agent fit notes. For the full normative wording, refer to ISO/IEC 42001:2023 itself.

## A.2 Policies related to AI

Two controls:

- **A.2.2 AI policy** — establish, communicate, review the AI policy.
- **A.2.3 Alignment with other organizational policies** — AI policy aligns with broader org policies (info security, privacy, ethics, code of conduct, procurement).

## A.3 Internal organization

Two controls:

- **A.3.2 AI roles and responsibilities** — roles assigned and communicated.
- **A.3.3 Reporting of concerns** — channels for raising AI-related concerns (whistleblower-style accessibility, anonymous option).

## A.4 Resources for AI systems

Five controls covering the assets and inputs needed for AI systems:

- **A.4.2 Resource documentation** — document the resources used by AI systems.
- **A.4.3 Data resources** — data used by AI systems documented and managed.
- **A.4.4 Tooling resources** — tools (training, evaluation, deployment, monitoring) documented and managed.
- **A.4.5 System and computing resources** — infrastructure (cloud, hardware, networking) documented and managed.
- **A.4.6 Human resources** — competencies for AI work documented and managed.

SRE fit: maps to ITIL Asset Management and ISO 27001 A.5.9 (inventory of information and assets). For AI work specifically: data, models, prompts, tool definitions, evaluation harnesses, vector DBs all enter the asset register.

## A.5 Assessing impacts of AI systems

Four controls. AI system impact assessment is the load-bearing process at the heart of ISO 42001:

- **A.5.2 AI system impact assessment process** — process for conducting impact assessments.
- **A.5.3 Documentation of AI system impact assessments** — records of completed assessments.
- **A.5.4 Assessing AI system impact on individuals or groups** — fairness, discrimination, privacy, human dignity considerations.
- **A.5.5 Assessing societal impacts of AI systems** — broader social, economic, environmental impacts.

The impact assessment is required by Cl 6.1.4 and Cl 8.4; the controls operationalize it.

## A.6 AI system lifecycle

Seven controls covering the AI system lifecycle, the framework's core operational concept:

- **A.6.1.2 Objectives for responsible development of AI systems** — clear objectives for responsible development.
- **A.6.1.3 Processes for responsible AI system design and development** — defined processes.
- **A.6.2.2 AI system requirements and specification** — requirements documented.
- **A.6.2.3 Documentation of AI system design and development** — design records.
- **A.6.2.4 AI system verification and validation** — V&V activities.
- **A.6.2.5 AI system deployment** — deployment procedures.
- **A.6.2.6 AI system operation and monitoring** — ongoing monitoring and management.
- **A.6.2.7 Technical documentation** — technical documentation for AI systems.
- **A.6.2.8 AI system recording of event logs** — event logging requirements.

The lifecycle stages described in the controls: planning, design and development, verification and validation, deployment, operation and monitoring, re-evaluation, retirement.

SRE fit: maps to MLOps lifecycle, ITIL Service Design / Transition / Operation activities. For agent systems: system prompt design, tool scope definition, evaluation harness construction, deployment with gradual rollout, ongoing behavioral monitoring, retirement procedures.

## A.7 Data for AI systems

Four controls on data handling:

- **A.7.2 Data for development and enhancement of AI systems** — data quality, provenance, lineage for development data.
- **A.7.3 Acquisition of data** — data acquisition processes.
- **A.7.4 Quality of data for AI systems** — data quality controls.
- **A.7.5 Data provenance** — provenance documentation.
- **A.7.6 Data preparation** — data preparation processes.

SRE fit: maps to ISO 27001 A.5.12 (classification), A.5.13 (labelling), A.5.14 (information transfer), A.8.10 (information deletion), A.8.11 (data masking). For AI specifically: training-data provenance, RAG-corpus management, evaluation-dataset versioning.

## A.8 Information for interested parties of AI systems

Five controls on transparency to affected parties:

- **A.8.2 System documentation and information for users** — documentation provided to users.
- **A.8.3 External reporting** — external transparency mechanisms.
- **A.8.4 Communication of incidents** — incident communication to affected parties.
- **A.8.5 Information for interested parties** — relevant information made available.

Connects to EU AI Act transparency obligations and to NIST AI RMF Govern function.

SRE fit: for agent systems serving customers, user-facing documentation explains what the agent does, what data it touches, what limits apply, how to escalate. Incident communication includes AI-related incidents.

## A.9 Use of AI systems

Two controls on using AI systems (the org as AI user, distinct from AI developer):

- **A.9.2 Processes for responsible use of AI systems** — processes for using AI systems responsibly.
- **A.9.3 Objectives for responsible use of AI systems** — clear objectives for use.
- **A.9.4 Intended use of AI system** — define and document intended use.

These controls apply when the org uses AI systems built by others (e.g., consuming model APIs from Anthropic / OpenAI / Google rather than developing models in-house). Apply alongside the third-party relationship controls.

## A.10 Third-party and customer relationships

Three controls on supplier and customer relationships:

- **A.10.2 Allocating responsibilities** — clear allocation of responsibilities between parties.
- **A.10.3 Suppliers** — supplier-side AI considerations.
- **A.10.4 Customers** — customer-side AI considerations.

SRE fit: load-bearing for model-vendor relationships. Anthropic, OpenAI, Google, Cohere, vector DB SaaS providers, agent framework SaaS providers all sit here. Combined with ISO 27001 A.5.19-A.5.23 supplier controls.

## Annex B implementation guidance

ISO/IEC 42001:2023 includes Annex B providing implementation guidance per Annex A control. Non-normative; aimed at helping implementers understand intent and example evidence. Useful starting point for SoA development; not sufficient for deep implementation in mature programs.

## Statement of Applicability (SoA)

Required by Cl 6.1.3 equivalent. Records:

- Each Annex A control
- Applicable (yes / no)
- Justification (if not applicable: why; if applicable: rationale and link to risk treatment)
- Implementation status
- Reference to implementing policy, procedure, or evidence

The SoA also captures org-specific controls beyond Annex A. For AI work, expect to add controls covering: generative-AI-specific concerns (prompt injection, hallucination), agent autonomy controls (tool scope, kill-switches), model-vendor-specific arrangements, evaluation harness governance, vector / RAG-specific concerns.

## Common implementation patterns

- **Risk-driven SoA**: control selection driven by AI risk register entries. Each risk → one or more controls selected for treatment. Cleanest mapping.
- **Coverage-driven SoA**: assume all Annex A controls apply; justify any exclusions. Simpler to defend but can over-implement.
- **Phased SoA**: initial scope covers core (A.2 policies, A.3 organization, A.5 impact assessment, A.6 lifecycle, A.7 data, A.10 third-party); subsequent cycles expand to A.4 resources, A.8 information, A.9 use.

## SRE and AI-agent fit summary

| Concern | Primary Annex A controls |
|---|---|
| AI policy and roles | A.2.2, A.2.3, A.3.2, A.3.3 |
| AI asset inventory (data, models, prompts, tools) | A.4.2-A.4.6 |
| AI impact assessment | A.5.2-A.5.5 |
| AI system lifecycle (incl agent systems) | A.6.1.2-A.6.2.8 |
| Data handling (training, RAG, evaluation) | A.7.2-A.7.6 |
| Transparency to users / affected parties | A.8.2-A.8.5 |
| Use of vendor AI (model APIs as services) | A.9.2-A.9.4 |
| Model-vendor relationships | A.10.2-A.10.4 |

## See also

- [[ISO 42001 Cluster|cluster MOC]] · [[ISO 42001 Clause Structure]] · [[ISO 42001 AI System Lifecycle]] · [[ISO 42001 vs ISO 27001 Integration]]
- [[ISO 27001 Annex A.5 Organizational Controls]] · [[ISO 27001 Annex A.8 Technological Controls]] (sibling control sets; substantial overlap)
- [[OWASP LLM Top 10 Cluster]] (operational threats feeding into risk register)
