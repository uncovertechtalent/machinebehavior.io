title: FedRAMP and CMMC Mechanics
summary: Per FIPS 199 categorization (confidentiality / integrity /.
parent: fedramp-cmmc
order: 100
labels: fedramp-cmmc, framework-concept
aliases: FedRAMP and CMMC Mechanics | FedRAMP Impact Levels | CMMC Levels | NIST 800-171
type: framework-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/fedramp-cmmc/FedRAMP and CMMC Mechanics.md
reviewed: no
---
## FedRAMP impact levels

Per FIPS 199 categorization (confidentiality / integrity / availability):

- **Low** — limited adverse effect.
- **Moderate** — serious adverse effect.
- **High** — severe or catastrophic adverse effect.

Cloud service authorized at a specific impact level. Federal agency consumes per that level.

## FedRAMP authorization paths

### JAB Provisional ATO (P-ATO)

- Joint Authorization Board (DoD, DHS, GSA) authorizes.
- Most widely-used services.
- Highly competitive process.

### Agency ATO

- Individual federal agency authorizes.
- Specific use case.
- Faster but narrower recognition.

### FedRAMP Tailored

- Lower-impact services.
- Reduced control set.

## FedRAMP process

1. **Readiness assessment** (optional but common).
2. **3PAO engagement** — Third Party Assessment Organization.
3. **Documentation development** — System Security Plan (SSP), policies, procedures.
4. **Assessment** — 3PAO assesses controls.
5. **Authorization decision** — JAB or agency.
6. **Continuous monitoring** — monthly POAM updates, annual assessments, vulnerability scans.

Typical timeline: 12-18 months for first authorization. Continuous monitoring perpetual.

## Cost

FedRAMP authorization costs:

- **3PAO assessment**: $300k-1M+ depending on scope.
- **Internal effort**: significant ongoing.
- **Continuous monitoring**: $200k-500k+ annually.

Cost-justified by federal procurement market access.

## CMMC 2.0 levels

### Level 1 (Foundational)

- 17 NIST 800-171 baseline practices.
- Protects FCI (Federal Contract Information).
- Self-attestation annual.
- Annual senior official affirmation.

### Level 2 (Advanced)

- Full 110 NIST SP 800-171 Rev. 3 controls.
- Protects CUI (Controlled Unclassified Information).
- Two assessment paths:
  - **Self-assess + affirm** — for non-prioritized contracts.
  - **C3PAO assessment** — for prioritized contracts; certificate issued.
- Triennial assessment for C3PAO-assessed.

### Level 3 (Expert)

- NIST 800-171 + additional NIST 800-172 controls (~24 enhanced controls).
- Protects against APTs.
- DIBCAC government assessment.
- 5-year validity with annual affirmations.

## NIST 800-171 controls

Across 14 families:

- Access Control
- Awareness and Training
- Audit and Accountability
- Configuration Management
- Identification and Authentication
- Incident Response
- Maintenance
- Media Protection
- Personnel Security
- Physical Protection
- Risk Assessment
- Security Assessment
- System and Communications Protection
- System and Information Integrity

110 controls in Rev. 3.

## CMMC implementation timeline

- **Final rule (32 CFR Part 170)** published 2024.
- **DFARS contract clause** rollout through 2024-2026.
- **Phased contract inclusion** — proportionally expanding through 2028.
- **All DoD contracts** subject to CMMC by 2028.

## FedRAMP and CMMC overlap

- Both NIST 800-53 / 800-171 based.
- FedRAMP for cloud services to federal agencies.
- CMMC for DoD contractor supply chain.
- Some overlap; some independent application.
- Cloud services serving DoD: typically need both.

## SRE and AI-agent fit notes

For US federal / DoD market:

- FedRAMP for cloud-hosted AI services.
- CMMC for DoD contractor systems (including AI).
- NIST 800-171 controls foundational.

For non-US-federal:

- Limited applicability.

## Stefan-context implementation sketch

- Limited direct relevance.
- For US-federal-adjacent clients: vocabulary familiarity.

## See also

- [[FedRAMP CMMC Cluster|cluster MOC]] · [[FedRAMP and CMMC Controversies]]
- [[NIST CSF Cluster]]
