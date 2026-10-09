title: NIST CSF
summary: Map of NIST Cybersecurity Framework 2.0 (February 2024).
parent: index
order: 130
labels: cybersecurity-frameworks, moc, nist-csf, voluntary-frameworks
aliases: NIST CSF Cluster | NIST CSF | NIST Cybersecurity Framework | CSF 2.0 | NIST CSF 2.0
type: MOC
created: 2026-05-12
updated: 2026-06-08
origin: pillars/nist-csf/NIST CSF Cluster.md
reviewed: no
---
> Map of NIST Cybersecurity Framework 2.0 (February 2024). Voluntary, outcome-oriented, function-organized US framework. Six core functions: Govern, Identify, Protect, Detect, Respond, Recover. Widely used as implementation reference globally, including by ISO 27001 shops.

## Anchors

- [position](pillars/nist-csf/position.md) · [anchors](pillars/nist-csf/anchors.md)

## Provenance

- **NIST CSF 1.0** (2014) — original. Five functions (Identify, Protect, Detect, Respond, Recover). Following Executive Order 13636 (2013) on critical infrastructure cybersecurity.
- **NIST CSF 1.1** (2018) — minor revision.
- **NIST CSF 2.0** (February 2024) — substantial revision. Added Govern function (6th); broadened scope from critical infrastructure to all org types/sizes; added implementation examples and informative references.
- **NIST AI RMF** (2023) and **NIST Privacy Framework** (2020/2024) — companion frameworks using similar function-based structure.

## What NIST CSF 2.0 is

A voluntary cybersecurity framework. Not certifiable. Outcome-oriented. Helps orgs:

- Understand and assess current cybersecurity posture.
- Communicate cybersecurity expectations.
- Manage and reduce cybersecurity risks.
- Integrate cybersecurity with broader risk management.

## Six core functions

- **GOVERN** (new in 2.0): Establish, communicate, monitor cybersecurity risk management strategy, expectations, policy.
- **IDENTIFY**: Understand cybersecurity risks to systems, people, assets, data, capabilities.
- **PROTECT**: Implement appropriate safeguards.
- **DETECT**: Discover cybersecurity events.
- **RESPOND**: Take action on detected events.
- **RECOVER**: Restore capabilities or services impaired by events.

Each function has categories and subcategories. Subcategories are outcome statements (~100+ across the framework).

Detail in [[NIST CSF Core Functions]].

## Implementation tiers

Four tiers describing cybersecurity risk management practice rigor:

- Tier 1: Partial
- Tier 2: Risk Informed
- Tier 3: Repeatable
- Tier 4: Adaptive

Not a maturity scale per se; framework cautions against treating as one.

## Profiles

Current Profile (current state) vs Target Profile (desired state). Gap analysis drives improvement plans.

Community Profiles (sector-specific) published for:

- Manufacturing
- Smart grid
- Communications
- Maritime
- Election security
- Others

## CSF 2.0 changes from 1.1

- **Govern function added.** Cybersecurity governance as first-class.
- **Scope broadened.** Originally critical infrastructure; now all orgs.
- **Implementation examples added** per subcategory.
- **Informative references** to NIST 800-53, ISO 27001, CIS Controls, ATT&CK, others.
- **Quick-Start Guides** published for specific contexts.

## Why this matters for SRE and AI-agent work

- **De facto US cybersecurity framework**, even for ISO-27001 shops.
- **Cross-framework references** simplify multi-framework implementations.
- **Function structure** maps cleanly to operational practice.
- **NIST AI RMF companion** for AI work.
- **State-government adoption.** Several US state laws reference NIST CSF.

## Related clusters

- [[ISO 27001 Cluster|ISO 27001]] — sibling certifiable; ISO 27002:2022 attribute axis aligns to CSF functions.
- [[NIST AI RMF Cluster|NIST AI RMF]] — sibling for AI risk.
- [[MITRE Cluster|MITRE ATT&CK]] — informative references.

## See also

[[NIST CSF Cluster]] (pillars MOC) · [position](pillars/nist-csf/position.md) · [anchors](pillars/nist-csf/anchors.md) · [[ISO 27001 Cluster]] · [[NIST AI RMF Cluster]]
