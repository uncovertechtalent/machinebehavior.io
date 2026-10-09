title: NIST CSF Core Functions
summary: Six functions structure NIST CSF 2.0.
parent: nist-csf
order: 100
labels: framework-concept, nist-csf
aliases: NIST CSF Core Functions | NIST CSF Govern Identify Protect Detect Respond Recover | CSF Functions
type: framework-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/nist-csf/NIST CSF Core Functions.md
reviewed: no
---
> Six functions structure NIST CSF 2.0. Each function has categories and subcategories. Subcategories are outcomes the org should achieve.

## GOVERN (new in 2.0)

Establish, communicate, monitor cybersecurity risk management strategy, expectations, policy.

Categories:

- **Organizational Context (GV.OC)**: organization's mission, expectations of stakeholders, legal / regulatory / contractual requirements, critical dependencies.
- **Risk Management Strategy (GV.RM)**: priorities, constraints, appetite, supply chain.
- **Roles, Responsibilities, Authorities (GV.RR)**: cybersecurity roles, authorities, accountabilities.
- **Policy (GV.PO)**: cybersecurity policy, communication, monitoring.
- **Oversight (GV.OV)**: management commitment, risk management outcomes.
- **Cybersecurity Supply Chain Risk Management (GV.SC)**: supply chain governance.

## IDENTIFY

Understand cybersecurity risks to systems, people, assets, data, capabilities.

Categories:

- **Asset Management (ID.AM)**: inventory of assets.
- **Risk Assessment (ID.RA)**: risk identification and analysis.
- **Improvement (ID.IM)**: improvement processes.

## PROTECT

Implement appropriate safeguards.

Categories:

- **Identity Management, Authentication, Access Control (PR.AA)**.
- **Awareness and Training (PR.AT)**.
- **Data Security (PR.DS)**.
- **Platform Security (PR.PS)**: software development, hardware integrity, configuration management.
- **Technology Infrastructure Resilience (PR.IR)**.

## DETECT

Discover cybersecurity events.

Categories:

- **Continuous Monitoring (DE.CM)**.
- **Adverse Event Analysis (DE.AE)**: events analyzed to characterize them.

## RESPOND

Take action on detected events.

Categories:

- **Incident Management (RS.MA)**.
- **Incident Analysis (RS.AN)**.
- **Incident Response Reporting and Communication (RS.CO)**.
- **Incident Mitigation (RS.MI)**.

## RECOVER

Restore capabilities or services.

Categories:

- **Incident Recovery Plan Execution (RC.RP)**.
- **Incident Recovery Communication (RC.CO)**.

## Subcategory examples

Each category has multiple subcategories (outcome statements). Example subcategories:

- GV.OC-01: organizational mission understood.
- ID.AM-01: hardware inventory.
- PR.AA-01: identities established and credentialed for authorized individuals.
- DE.CM-01: networks monitored to find adverse events.
- RS.MA-01: incident response plan executed.
- RC.RP-01: recovery plan executed during or after incident.

## Implementation tiers

Four tiers:

- **Tier 1: Partial** — ad hoc, reactive.
- **Tier 2: Risk Informed** — risk-aware practices.
- **Tier 3: Repeatable** — formalized, organization-wide.
- **Tier 4: Adaptive** — continuous improvement.

Tier choice depends on org's risk tolerance, threat environment, mission. Higher tier is not universally better.

## Profiles

- **Current Profile**: org's current state per function/category/subcategory.
- **Target Profile**: org's desired state.
- **Gap analysis** drives improvement plans.

## Informative references

NIST publishes mappings from each subcategory to:

- NIST 800-53 controls.
- ISO 27001 / 27002 controls.
- CIS Controls.
- COBIT.
- ATT&CK techniques (where relevant).
- Other frameworks.

Enables cross-framework navigation.

## SRE and AI-agent fit notes

### CSF for AI work

AI features in CSF scope:

- GV.SC supply chain (model providers).
- ID.AM asset inventory (AI features as assets).
- PR.PS platform security (system prompts, tool scopes as configuration).
- DE.CM monitoring (agent behavior).
- RS.AN incident analysis (AI-incident root cause).
- RC.RP recovery (AI feature failover).

NIST AI RMF complements CSF for AI-specific risk.

### Combined CSF + ISO 27001

Function-to-Annex-A mapping straightforward. Single control set serves both.

## Stefan-context implementation sketch

- For US-customer-facing work: CSF vocabulary in stakeholder communication.
- Cross-framework references reduce dual-implementation overhead.

## See also

- [[NIST CSF Cluster|cluster MOC]] · [[NIST CSF vs ISO 27001 and NIST AI RMF]] · [[NIST CSF Controversies]]
- [[ISO 27001 Annex A.5 Organizational Controls]] (function-to-control mapping)
- [[NIST AI RMF Core Functions]] (sibling structure)
