title: CSA CCM Control Domains
summary: Audit planning, independence, management, results communication.
parent: csa-ccm
order: 100
labels: csa-ccm, framework-concept
aliases: CSA CCM Control Domains | CCM v4 Domains | CCM 17 Domains | CAIQ
type: framework-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/csa-ccm/CSA CCM Control Domains.md
reviewed: no
---
## 17 control domains (CCM v4)

### A&A — Audit & Assurance

Audit planning, independence, management, results communication.

### AIS — Application & Interface Security

Application security policies, baseline requirements, secure deployment, secure design.

### BCR — Business Continuity Management & Operational Resilience

BC strategy, plans, testing, communication, recovery.

### CCC — Change Control & Configuration Management

Change management, configuration management baselines, change quality testing.

### CEK — Cryptography, Encryption & Key Management

Cryptographic policies, encryption standards, key management.

### DSP — Data Security & Privacy Lifecycle Management

Data classification, ownership, processing, retention, disposal.

### DCS — Datacenter Security

Off-site facility access control, environmental controls.

### GRC — Governance, Risk & Compliance

Governance framework, risk management, compliance management.

### HRS — Human Resources

Background checks, employment terms, training, exit procedures.

### IAM — Identity & Access Management

Authentication, authorization, account management, privileged access.

### IPY — Interoperability & Portability

API documentation, data portability, cloud-to-cloud interoperability.

### IVS — Infrastructure & Virtualization Security

Network security, segmentation, virtualization security, OS hardening.

### LOG — Logging & Monitoring

Log generation, retention, integrity, monitoring, alerting.

### SEF — Security Incident Management, E-Discovery & Cloud Forensics

Incident response, e-discovery, forensics, evidence handling.

### STA — Supply Chain Management, Transparency & Accountability

Supplier risk assessment, supplier security, third-party audit, governance.

### TVM — Threat & Vulnerability Management

Vulnerability identification, anti-malware, threat intelligence, vulnerability disclosure.

### UEM — Universal Endpoint Management

Endpoint security, BYOD, MDM.

## CAIQ — Consensus Assessments Initiative Questionnaire

Standardized questionnaire derived from CCM. Cloud customers ask cloud providers; cloud providers complete + publish to STAR registry.

Each control domain has questions. Cloud provider responses:

- "Yes" — control implemented.
- "No" — not implemented.
- "N/A" — not applicable.
- Plus explanation.

## STAR Registry levels

### Level 1 STAR Self-Assessment

Cloud provider submits completed CAIQ. Free public registry entry. Limited assurance value (self-attested).

### Level 2 STAR Certification

Independent third-party assessment combining ISO 27001 + CCM. Assessor certifies. Higher assurance.

### Level 2 STAR Attestation

Independent third-party attestation combining SOC 2 + CCM. Higher assurance.

### Level 2 STAR C-STAR

China-specific variant.

### Level 3 STAR Continuous

Continuous monitoring + reporting. Limited adoption.

## Cross-framework mappings

CCM published mappings to:

- ISO 27001 / 27002 / 27017 / 27018 / 27036 / 27040
- NIST CSF
- NIST SP 800-53
- PCI DSS
- HIPAA
- HITRUST CSF
- AICPA SOC 2 TSC
- GDPR
- Singapore MAS Outsourcing Guidelines
- Multiple others

Maps enable cloud customers to use CCM as cross-framework lens.

## Cloud provider STAR usage

Major cloud providers:

- **AWS** — STAR Level 1 + Level 2 STAR Certification.
- **Microsoft Azure** — STAR Level 1 + Level 2.
- **Google Cloud Platform** — STAR Level 1 + Level 2.
- **Salesforce** — STAR Level 1 + Level 2.
- **Many SaaS providers** — STAR Level 1.

Customer due diligence: download CAIQ from STAR registry.

## SRE and AI-agent fit notes

For cloud vendor due diligence:

- CAIQ retrieval from STAR.
- Control-by-control review against own requirements.
- Mapping to org's primary framework (ISO 27001, NIST CSF).

For AI vendor due diligence:

- Major AI vendors increasingly submit STAR.
- Anthropic, OpenAI compliance posture documentation overlaps with CCM coverage.

## Stefan-context implementation sketch

- For cloud / AI vendor evaluation: STAR + CAIQ as standardized due-diligence source.
- For client engagements: support client-side cloud vendor assessment.

## See also

- [[CSA CCM Cluster|cluster MOC]] · [[CSA CCM Controversies]]
- [[ISO 27001 Family and Sector Variants]] (ISO 27017 cloud-specific)
