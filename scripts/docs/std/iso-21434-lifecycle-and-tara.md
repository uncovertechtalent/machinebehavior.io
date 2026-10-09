title: ISO 21434 Lifecycle and TARA
summary: Organizational level..
parent: iso-21434
order: 100
labels: framework-concept, iso-21434
aliases: ISO 21434 Lifecycle | ISO 21434 TARA | Vehicle Cybersecurity Lifecycle | Threat Analysis and Risk Assessment
type: framework-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/iso-21434/ISO 21434 Lifecycle and TARA.md
reviewed: no
---
## CSMS — Cybersecurity Management System

Organizational level. Includes:

- Cybersecurity policy and processes.
- Roles and responsibilities.
- Resources and competence.
- Distributed cybersecurity activities across product lifecycle.
- Continuous cybersecurity activities (post-deployment).
- Audit and management review.

OEMs and suppliers maintain CSMS supporting product cybersecurity engineering.

## Product lifecycle phases

### Concept phase

- **Item definition** — what is being developed; assumptions; boundaries.
- **Cybersecurity goals** — high-level outcomes.
- **TARA** — threat analysis and risk assessment.
- **Cybersecurity concept** — initial cybersecurity strategy.

### Product development phase

- **Cybersecurity requirements** derived from cybersecurity goals.
- **Cybersecurity design** — architecture, components, interfaces.
- **Integration and verification** — assemble, test cybersecurity.
- **Validation** — validate cybersecurity goals achieved.
- **Release for production**.

### Post-development phases

- **Production** — secure manufacturing process.
- **Operations and maintenance** — incident management, vulnerability management, security updates.
- **Decommissioning** — secure decommissioning.

## TARA — Threat Analysis and Risk Assessment

### Asset identification

Identify cybersecurity-relevant assets:

- Components, interfaces.
- Data (user data, vehicle data, control data).
- Functions.

### Damage scenarios

For each asset, what damage could occur:

- Financial impact.
- Operational impact.
- Safety impact.
- Privacy impact.

### Threat scenarios

For each damage scenario, threat agents and methods:

- Attacker profiles.
- Attack paths.

### Attack path analysis

How could threat scenarios manifest:

- Entry points.
- Vulnerabilities to exploit.
- Steps to achieve threat scenario.

### Risk determination

Combine attack feasibility + impact:

- Likelihood.
- Severity.
- Risk level.

### Risk treatment

For each significant risk:

- Avoid, transfer, mitigate, accept.
- Document treatment decisions.

## Cybersecurity engineering activities

Throughout lifecycle:

- **Requirements engineering** — derived from cybersecurity goals.
- **Design** — secure by design principles.
- **Implementation** — secure coding, secure configuration.
- **Verification** — code review, static analysis, dynamic testing, penetration testing.
- **Validation** — does the product achieve cybersecurity goals?

## Distributed cybersecurity activities

OEM + tier-N supplier coordination:

- Cybersecurity requirements flow-down.
- Supplier-side cybersecurity activities.
- Cybersecurity interface agreement.
- Joint TARA for shared interfaces.

## Continuous cybersecurity activities (post-deployment)

- **Cybersecurity monitoring** — production fleet monitoring.
- **Cybersecurity incident response** — detect, contain, recover.
- **Vulnerability management** — identify, assess, address.
- **Security updates** — develop, distribute, install.

Aligns with UN R156 SUMS for software update management.

## Cybersecurity interface agreements

Between OEMs and suppliers:

- Define cybersecurity responsibilities.
- Define cybersecurity requirements at interface.
- Define information exchange (vulnerabilities, incidents).
- Define joint activities (TARA, audits).

## AI-feature considerations

For AI features (ADAS, autonomous driving):

- TARA includes AI-specific threats (adversarial inputs, model poisoning, prompt injection for LLM-based features).
- Cybersecurity goals address AI-related impact.
- ATLAS-aware threat analysis.
- ISO/PAS 21448 SOTIF complements for AI safety.

## SRE and AI-agent fit notes

Vehicle-specific work; less directly relevant to typical SRE engagements unless serving automotive clients.

For automotive client engagements:

- Vocabulary alignment with ISO 21434 phases.
- TARA methodology familiarity.
- AI feature threat modeling using ATLAS + automotive specifics.

## Stefan-context implementation sketch

- For automotive client engagements: ISO 21434 + TISAX + UN R155 combined framing.
- Limited direct applicability for general SRE / AI work outside automotive sector.

## See also

- [[ISO 21434 Cluster|cluster MOC]] · [[ISO 21434 Controversies]]
- [[UN R155 R156 Cluster]] · [[TISAX Cluster]] · [[ASPICE Cluster]]
