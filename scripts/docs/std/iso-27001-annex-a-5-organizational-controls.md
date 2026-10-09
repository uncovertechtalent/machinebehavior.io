title: ISO 27001 Annex A.5 Organizational Controls
summary: Largest of the four :2022 control themes.
parent: iso-27001
order: 100
labels: annex-a-theme, iso-27001, theme-organizational
aliases: ISO 27001 Annex A.5 | ISO 27001 Organizational Controls | Annex A.5 Controls
type: annex-a-theme
created: 2026-05-12
updated: 2026-06-08
origin: pillars/iso-27001/ISO 27001 Annex A.5 Organizational Controls.md
reviewed: no
---
> Largest of the four :2022 control themes. Thirty-seven controls covering policy, roles, asset management, classification and labelling, access control, supplier relationships, incident management, business continuity, and legal / regulatory compliance. The management-system spine of the control set; A.6 / A.7 / A.8 hang off A.5.

## How to read this atom

Each control listed below has its reference number and title from ISO 27001:2022 Annex A. The accompanying notes cover purpose, typical implementation, common evidence, SRE / AI-agent fit notes where the control has non-obvious shape for those domains. For full normative wording and implementation guidance see ISO/IEC 27002:2022.

New controls in :2022 are tagged **(NEW)**.

## A.5.1 Policies for information security

Top-level information security policy plus topic-specific policies (acceptable use, access control, cryptography, supplier, incident response, ...). Approved, communicated, periodically reviewed. Mirrors Cl 5.2.

Evidence: policy register, current versions, approval records, review schedule, communication evidence.

## A.5.2 Information security roles and responsibilities

Roles defined and assigned. Mirrors Cl 5.3. Typically reflected in a RACI matrix or roles register.

## A.5.3 Segregation of duties

Conflicting duties separated so no single person can perform a sensitive end-to-end action unaudited. Examples: code author ≠ code approver, payment requestor ≠ payment approver, admin-account creator ≠ admin-account user.

AI-agent fit: autonomous-agent operations break classical SoD. An agent that requests, approves, and executes a change in one run is a SoD breach by design. Compensating controls: time-delayed execution with human review window, two-agent design (proposer + approver), strict tool-scope limits, full audit logging.

## A.5.4 Management responsibilities

Management ensures personnel apply infosec per policies and procedures. Mirrors Cl 5.1.

## A.5.5 Contact with authorities

Identified contacts with relevant authorities (regulators, law enforcement, national CERTs, data-protection authorities). When and how to engage.

Evidence: contact register, escalation procedure, evidence of engagement (e.g., GDPR breach notifications, BaFin / Bundesbank reporting for financial-services orgs).

## A.5.6 Contact with special interest groups

Membership in or contact with security forums, professional associations, ISACs / ISAOs, vendor security communities.

## A.5.7 Threat intelligence (NEW)

Collect, analyse, and produce threat intelligence to support the org's risk-management decisions. Three layers:

- **Strategic** — long-term threat-landscape view (ENISA reports, national CERT bulletins, sector-specific ISACs).
- **Tactical** — adversary TTPs (MITRE ATT&CK, MITRE ATLAS for AI).
- **Operational / technical** — IOCs, vulnerability reports, exploit availability.

AI-agent fit: explicit feeds for prompt-injection campaigns, model-supply-chain compromises, jailbreak technique evolution (MITRE ATLAS, OWASP LLM Top 10 update channels, vendor security advisories from Anthropic / OpenAI / etc.).

Evidence: subscriptions / feeds register, periodic threat reports consumed in risk assessment and management review.

## A.5.8 Information security in project management

Infosec integrated into project management for all project types. Threat modelling, security requirements, security testing as project deliverables, not afterthoughts.

## A.5.9 Inventory of information and other associated assets

Asset inventory: information assets, hardware, software, services, identities, premises. Owner identified per asset. The Cl 6.1.2 risk identification depends on this.

AI-agent fit: agents themselves are assets. System prompts, tool definitions, model versions are assets. Vector databases and embedding stores are assets. Training data is an asset. Add to the inventory.

## A.5.10 Acceptable use of information and other associated assets

Rules for the use of information and assets. Often the most-read policy artefact (because every employee signs it on joining).

AI-agent fit: acceptable use of AI tools (employee use of Claude, ChatGPT, Copilot). What can be entered into prompts; what cannot. Most orgs added AUP addenda in 2023-2024.

## A.5.11 Return of assets

Assets returned on termination or change of employment. Includes information assets and access (passwords, MFA tokens, badges, devices).

## A.5.12 Classification of information

Classification scheme (typically Public / Internal / Confidential / Restricted, or equivalent). Each information asset classified per the scheme.

Vault example: `work-kb/` work-shareable; `whiteout-kb/` local-only; `mercedes-kb/` client-specific; `pillars/` personal-knowledge. AGENTS.md hard rule "Never paste vault content into chat platforms or work tickets without explicit per-destination authorization" is the boundary control.

## A.5.13 Labelling of information

Labels applied per the classification scheme. Document headers, footers, watermarks, metadata, frontmatter tags.

Vault example: frontmatter `tags: kb/whiteout-kb` is the label for vault-internal use.

## A.5.14 Information transfer

Transfers of information are controlled — internal transfers, transfers to external parties, electronic transfers (email, file share, API, agent context windows).

AI-agent fit: sending data to a model API is an information transfer. Controls: TLS in transit, vendor-side encryption at rest, data residency, DPA / contractual safeguards, optional vendor opt-outs (training opt-out for OpenAI / Anthropic enterprise tiers).

## A.5.15 Access control

Policy on access control, based on business and infosec requirements.

## A.5.16 Identity management

Full lifecycle: identity establishment, modification, suspension, deletion. Identity proofing, identity proofs of work.

## A.5.17 Authentication information

Allocation, distribution, and management of authentication information (passwords, keys, MFA tokens, biometric templates, API tokens, agent-specific credentials).

AI-agent fit: agent API keys are authentication information under A.5.17. Rotation cadence, scope limitation, vault-or-secret-manager storage all apply. Common gap: developer machines holding long-lived agent API keys with broad scope.

## A.5.18 Access rights

Provisioning, modification, removal, periodic review of access rights. Joiner-mover-leaver process.

## A.5.19 Information security in supplier relationships

Identify and mitigate risks from supplier access to org's information.

## A.5.20 Addressing information security within supplier agreements

Security requirements specified in supplier contracts. DPA, SLA, audit rights, breach notification obligations, sub-processor approval.

AI-agent fit: model vendor agreements. Anthropic enterprise, OpenAI enterprise, Google Cloud Vertex AI, AWS Bedrock all have specific DPAs and data-handling commitments. Track which tier each agent uses; align with A.5.34 PII obligations.

## A.5.21 Managing information security in the ICT supply chain

Supply-chain security: hardware (Apple, Dell, Lenovo, etc.), software (npm / PyPI / Maven dependencies, container images), services (SaaS, IaaS, PaaS), upstream developers (open-source maintainers).

SLSA, SBOM, signed releases, vulnerability scanning of dependencies, container image scanning fall here.

AI-agent fit: model supply chain. Where the weights came from, training data provenance (for open-weights models), prompt-injection-resistance attestation, vendor jailbreak-handling commitments.

## A.5.22 Monitoring, review and change management of supplier services

Ongoing monitoring of supplier service delivery and security. Reviews of supplier performance against agreed metrics. Change management when supplier scope shifts.

## A.5.23 Information security for use of cloud services (NEW)

Cloud-specific control. Selection, use, management, exit. Cloud-shared-responsibility model. CSA Cloud Controls Matrix is the common implementation reference; ISO 27017 expands on this.

AI-agent fit: model-as-a-service is cloud service. Apply A.5.23 to Anthropic API, OpenAI API, Google Vertex, AWS Bedrock relationships. Exit strategy (data deletion on contract termination) is part of this.

## A.5.24 Information security incident management planning and preparation

Incident response plan documented, roles assigned, communications prepared, playbooks built.

## A.5.25 Assessment and decision on information security events

Events triaged: is this an incident? What severity?

## A.5.26 Response to information security incidents

Documented incident response procedure. Containment, eradication, recovery, evidence preservation.

## A.5.27 Learning from information security incidents

Post-incident review (blameless / blame-aware), lessons learned, feeds into risk assessment, control improvements, training updates. Connects to Cl 10.

## A.5.28 Collection of evidence

Evidence collection for legal / regulatory / disciplinary processes. Chain of custody.

## A.5.29 Information security during disruption

Infosec is maintained during business disruption. Different from BC plan: BC restores service; A.5.29 ensures that the restoration does not collapse controls.

## A.5.30 ICT readiness for business continuity (NEW)

ICT capacity to support business continuity. Tested recovery procedures, redundancy, alternative service paths. ISO 27031 expands on this.

## A.5.31 Legal, statutory, regulatory and contractual requirements

Identify, document, keep up to date all applicable legal / regulatory / contractual requirements. Implementation per requirement.

Examples: GDPR, NIS2, DORA, AI Act, sector regulators (BaFin, FCA, Bundesbank, Bundesnetzagentur, state-level DPAs).

## A.5.32 Intellectual property rights

Comply with IP rights. License management, open-source compliance, customer IP separation.

AI-agent fit: training-data IP issues. Code-completion model output and IP attribution. Customer prompt content as customer IP.

## A.5.33 Protection of records

Records protected against loss, destruction, falsification, unauthorized access, unauthorized release. Retention schedules per A.5.31 obligations.

## A.5.34 Privacy and protection of PII

PII identified, classified, handled per applicable law. ISO 27701 PIMS is the natural extension.

AI-agent fit: PII in prompts (employee inputs to AI tools), PII in model outputs, PII in retrieval corpora (RAG sources). Vendor-side PII handling under A.5.20 / A.5.23.

## A.5.35 Independent review of information security

Independent review at planned intervals or when significant changes occur. Internal audit (Cl 9.2) is one form; external certification audit is another; independent technical penetration testing is another.

## A.5.36 Compliance with policies, rules and standards for information security

Verification that infosec is performed in accordance with policies, rules, standards. Often via internal audit, control self-assessments, automated compliance tooling.

## A.5.37 Documented operating procedures

Procedures for operating infosec activities. The how-to companion to the what (policy) and why (objectives). Cl 7.5 controls these.

## SRE and AI-agent quick map (load-bearing A.5 controls)

| Concern | Primary A.5 controls |
|---|---|
| Vault classification & boundary control | A.5.12, A.5.13, A.5.14, A.5.33, A.5.34 |
| Vendor API / model provider management | A.5.19, A.5.20, A.5.21, A.5.22, A.5.23 |
| Agent system prompts and tools as assets | A.5.9, A.5.10, A.5.17 |
| Threat intelligence for AI / agent space | A.5.7 |
| Identity and access for human + agent identities | A.5.15, A.5.16, A.5.17, A.5.18 |
| Incident management for AI-system failures | A.5.24 - A.5.28 |
| Regulatory flow-down (AI Act, GDPR, DORA) | A.5.31, A.5.34 |
| Self-audit / independent review | A.5.35, A.5.36 |

## See also

- [[ISO 27001 Cluster|cluster MOC]]
- [[ISO 27001 Annex A.6 People Controls]] · [[ISO 27001 Annex A.7 Physical Controls]] · [[ISO 27001 Annex A.8 Technological Controls]]
- [[ISO 27001 Clause 6 Planning]] (SoA holds the per-control applicability)
- [[ISO 27001 Family and Sector Variants]] (27002 implementation guidance per control; 27017 cloud; 27018 / 27701 PII / privacy; 27031 BC ICT; 27035 incidents; 27036 supplier)
