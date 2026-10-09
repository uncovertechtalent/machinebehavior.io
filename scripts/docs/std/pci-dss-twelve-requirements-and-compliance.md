title: PCI DSS Twelve Requirements and Compliance
summary: Network segmentation. Firewall / equivalent controls.
parent: pci-dss
order: 100
labels: framework-concept, pci-dss
aliases: PCI DSS Twelve Requirements | PCI DSS v4 Requirements | PCI DSS Compliance Levels | PCI DSS Validation
type: framework-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/pci-dss/PCI DSS Twelve Requirements and Compliance.md
reviewed: no
---
## The twelve requirements (v4.0)

### 1. Install and maintain network security controls

Network segmentation. Firewall / equivalent controls. CHD environment (CDE) isolated.

### 2. Apply secure configurations to all system components

Hardening standards. Default credentials changed. Configuration management.

### 3. Protect stored account data

CHD storage minimization. Encryption / tokenization / truncation. Key management.

### 4. Protect cardholder data with strong cryptography during transmission

TLS-equivalent encryption for CHD in transit. Modern crypto (TLS 1.2+, strong ciphers).

### 5. Protect all systems from malicious software

Anti-malware. Behavior-based detection. Targeted Risk Analysis (TRA) flexibility in v4.

### 6. Develop and maintain secure systems and software

Vulnerability management. Secure development lifecycle. Patch management. Code review.

### 7. Restrict access by business need to know

Role-based access control. Least privilege.

### 8. Identify users and authenticate access

Unique IDs. MFA (substantially expanded in v4 — MFA into CDE).

### 9. Restrict physical access

Physical security for facilities housing CHD. Visitor controls. Media handling.

### 10. Log and monitor all access

Comprehensive logging. Log review. Integrity protection of logs.

### 11. Test security regularly

Vulnerability scanning (quarterly ASV for external). Penetration testing (annual). File integrity monitoring.

### 12. Support information security with organizational policies and programs

Security policy. Risk assessment. Incident response. Security awareness training. Service provider management.

## Each requirement has many sub-requirements

~300 specific sub-requirements across the twelve. Each sub-requirement testable; QSA / ISA validates implementation and operating effectiveness.

## Customized approach (new in v4)

Traditional requirements expressed as defined approach. v4 adds customized approach option:

- Org demonstrates control objective met by alternative implementation.
- Targeted Risk Analysis required.
- Documented and validated approach.

Provides flexibility for cloud-native, modern architectures.

## Compliance validation

### Level 1 merchants / service providers

- Annual on-site assessment by QSA.
- Quarterly external scans by ASV.
- Quarterly internal scans.
- Annual penetration testing.
- Report on Compliance (ROC) + Attestation of Compliance (AOC).

### Level 2 / 3 / 4 merchants

- Annual SAQ (appropriate type per processing model).
- Quarterly ASV scans (where applicable).
- AOC.

### Level 1 service provider

- Annual on-site assessment by QSA.
- ROC + AOC.

### Level 2 service provider

- Annual SAQ-D for Service Providers.

## Scope and CDE

Compliance focuses on cardholder data environment (CDE):

- Systems storing, processing, transmitting CHD or SAD.
- Connected-to systems.
- Security-impacting systems.

Scope reduction common strategy:

- Network segmentation isolates CDE.
- Tokenization removes CHD from systems.
- P2PE eliminates merchant-side CHD exposure.

Smaller CDE = lower compliance burden.

## Cardholder data vs sensitive authentication data

- **CHD (Cardholder Data)**: PAN (Primary Account Number), cardholder name, expiration date, service code. Can be stored if protected.
- **SAD (Sensitive Authentication Data)**: track data, CVV, PIN, PIN block. Cannot be stored post-authorization.

PAN truncation (last 4 digits) reduces scope.

## SaaS provider considerations

SaaS providing services to merchants:

- May be a service provider with own PCI DSS obligations.
- Customers may rely on provider's PCI compliance for shared responsibilities.
- Shared responsibility matrix critical.

## AI feature considerations

AI features touching CHD:

- In PCI DSS scope.
- Same twelve requirements apply.
- Vendor model providers as service providers — need PCI compliance evidence if CHD flows.

Typical pattern: don't put CHD into AI systems. Tokenize before / outside AI processing.

## SRE and AI-agent fit notes

For payment-processing clients:

- PCI DSS substantially overlaps ISO 27001 Annex A.
- Combined ISO 27001 + PCI DSS implementations common.
- Scope reduction via tokenization / P2PE reduces both burdens.

## Stefan-context implementation sketch

- For payment-processing client engagements: PCI DSS vocabulary load-bearing.
- For AI features in payment context: scope reduction (no CHD in AI) preferred.

## See also

- [[PCI DSS Cluster|cluster MOC]] · [[PCI DSS Controversies]]
- [[ISO 27001 Annex A.8 Technological Controls]]
