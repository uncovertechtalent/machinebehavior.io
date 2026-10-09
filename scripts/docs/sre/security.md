title: 8. Security
summary: "Security is a process, not a.
parent: pillars
order: 80
aliases: SRE Security Cluster | Security Cluster | 08-security
created: 2026-04-25
updated: 2026-06-08
origin: SRE/pillars/08-security/README.md
reviewed: no
---
> "Security is a process, not a product."

## What is Security in SRE?

Protecting systems, data, and users from unauthorized access, breaches, and attacks — while maintaining reliability and velocity.

## Core Principles

### Defense in Depth
Multiple layers of security controls:
```
Network → Infrastructure → Application → Data
```

### Least Privilege
- Minimum permissions necessary
- Time-bound access
- Regular access reviews

### Zero Trust
- Never trust, always verify
- Authenticate everything
- Encrypt everything

### Shift Left
- Security early in development
- Automated security testing
- Developer education

## Key Concepts

### CIA Triad
- **Confidentiality** — Only authorized access
- **Integrity** — Data is accurate and unmodified
- **Availability** — Systems accessible when needed

### Attack Surface
- External endpoints
- Internal services
- Third-party integrations
- Supply chain (dependencies)

### Threat Modeling
- What are we building?
- What can go wrong?
- What are we doing about it?
- Did we do a good job?

## Topics

- [ ] Secrets management
- [ ] Identity and access management
- [ ] Network security
- [ ] Container security
- [ ] Supply chain security
- [ ] Vulnerability management
- [ ] Security monitoring
- [ ] Incident response
- [ ] Compliance automation
- [ ] Penetration testing

## Secrets Management

### Don't
- Secrets in code
- Secrets in environment variables (visible in process list)
- Secrets in CI/CD logs
- Shared secrets

### Do
- Secrets in vault (HashiCorp Vault, AWS Secrets Manager)
- Dynamic/short-lived credentials
- Rotation automation
- Audit logging

## Container Security

### Image Security
- Minimal base images (distroless, alpine)
- No root user
- Scan for vulnerabilities
- Sign images

### Runtime Security
- Read-only filesystem
- Drop capabilities
- Resource limits
- Network policies

### Kubernetes Security
```yaml
securityContext:
  runAsNonRoot: true
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop: ["ALL"]
```

## Supply Chain Security

### SLSA Framework (Levels 1-4)
- Source integrity
- Build integrity
- Provenance
- Common requirements

### Dependency Management
- Pin versions
- Automated updates (Dependabot, Renovate)
- Vulnerability scanning
- SBOM generation

## Tools

| Tool | Purpose |
|------|---------|
| HashiCorp Vault | Secrets management |
| AWS Secrets Manager | Cloud secrets |
| Trivy | Container scanning |
| Snyk | Dependency scanning |
| Falco | Runtime security |
| OPA/Gatekeeper | Policy enforcement |
| SOPS | Encrypted secrets in Git |
| Teleport | Zero-trust access |

## Security Monitoring

### What to Monitor
- Authentication failures
- Authorization failures
- Privileged operations
- Data access patterns
- Network anomalies
- Configuration changes

### Alerting
- Failed login attempts (brute force)
- Privilege escalation
- Unusual data access
- Policy violations

## Anti-Patterns

- Security as afterthought
- Perimeter-only security
- Long-lived credentials
- Shared accounts
- No audit logging
- Security through obscurity

## Compliance

### Cross-sector InfoSec management

- [[ISO 27001 Cluster]] — ISMS standard. Annex SL aligned. Certifiable. Cl 4-10 + 93 Annex A controls.
- [[SOC 2 Cluster]] — AICPA TSC attestation. US procurement default.
- [[NIST CSF Cluster]] — voluntary US framework. Six functions (Govern/Identify/Protect/Detect/Respond/Recover).
- [[BSI IT-Grundschutz Cluster]] — DE national framework. ISO 27001 auf Basis IT-Grundschutz path.
- [[HITRUST Cluster]] — healthcare-broadened. e1 / i1 / r2 certification levels.

### EU regulatory

- [[GDPR Cluster]] — Reg 2016/679. Personal data protection. €20M / 4% turnover penalties.
- [[NIS2 Cluster]] — Dir 2022/2555. Essential / important entities. €10M / 2% turnover penalties.
- [[DORA Cluster]] — Reg 2022/2554. Financial services ICT resilience. Applicable 17 Jan 2025.
- [[Cyber Resilience Act Cluster]] — Reg 2024/2847. Product cybersecurity. Applicable late 2027.
- [[EU AI Act Cluster]] — Reg 2024/1689. Risk-tier AI obligations. 2026-2027 ramp.

### AI governance

- [[ISO 42001 Cluster]] — AI Management System. Annex SL sibling to ISO 27001.
- [[NIST AI RMF Cluster]] — voluntary US AI risk framework. GenAI Profile (NIST AI 600-1).
- [[OWASP LLM Top 10 Cluster]] — operational LLM threat taxonomy (v2.0 / 2025).
- [[OECD AI Cluster]] — international voluntary AI principles.

### Threat intelligence

- [[MITRE Cluster]] — ATT&CK + D3FEND + ATLAS frameworks.

### Sector-specific

- [[PCI DSS Cluster]] — Payment Card Industry Data Security Standard v4.0.
- [[TISAX Cluster]] — German automotive supplier assurance.
- [[ISO 21434 Cluster]] — Road vehicles cybersecurity engineering.
- [[UN R155 R156 Cluster]] — Vehicle CSMS + SUMS type approval.
- [[FedRAMP CMMC Cluster]] — US federal cybersecurity compliance.
- [[CSA CCM Cluster]] — Cloud Security Alliance Cloud Controls Matrix.

### Supply chain integrity

- [[SLSA SBOM Cluster]] — Software supply chain (SLSA levels + SBOM via SPDX / CycloneDX). Maps to ISO 27001 A.5.21 + A.8.30.

### Continuity and resilience

- [[ISO 22301 Cluster]] — Business Continuity Management Systems.

### Governance and process

- [[COBIT Cluster]] — IT governance framework.
- [[ITIL Cluster]] — IT service management framework.
- [[TOGAF Cluster]] — enterprise architecture framework.

### Automation
- Policy as code
- Continuous compliance
- Evidence collection
- Drift detection

## Reading

- Google SRE Book: Chapter 9 (Simplicity)
- Building Secure & Reliable Systems (Google)
- OWASP guidelines

## Atoms

- [[Defense in Depth and Trust Boundaries]]

## Published expressions

- "Shifting left security" is a misnomer that needs to die (9-part series) -- the long-form argument behind this pillar's "security is a process, not a product" stance. Start at [[2024-12-30_shifting-left-security-is-a-misnomer-that-needs-to-die-part-1-of-9|Part 1 of 9]]; the series chains prev/next through [[2024-12-30_shifting-left-security-is-a-misnomer-that-needs-to-die-part-9-of-9|Part 9 of 9]].

## People-substrate cross-cluster

Security at the people layer = psychological safety + boundary integrity + structural defenses against the team-level failure modes. Fawning is the human auth-bypass (yes-by-default = compromised input validation). Scapegoat dynamics are the team-level incident-response failure that targets a projection surface. Narcissism is the persistent-threat actor at organisational scale.

- Bridge essay: [[interview-training-psychology-parallels|Interview Training as Applied Clinical Psychology]] -- Item 7 (debrief room as miniature dysfunctional family)
- Competency: [[psychological-safety|Psychological Safety dimension]] -- the team-level confidentiality + integrity property; people speak up = honest input
- Competency: [[boundary-integrity|Boundary Integrity dimension]] -- least-privilege at the relational layer
- Psychology: [[pillars/psychology/fawning-and-female-conditioning|Fawning]] -- the auth-bypass failure mode; nervous-system-default yes is the human equivalent of permissive ACLs
- Psychology: [[pillars/psychology/narcissism-and-relational-abuse-patterns|Narcissism and relational abuse patterns]] -- the APT at human scale; entropy-management at the team's expense
- Psychology: [[pillars/psychology/scapegoat-child-in-dysfunctional-families|Scapegoat-child dynamics]] -- the team-level incident-response failure mode; analogous to mis-routing a security alert to the wrong service
- Developmental-position: [[pillars/developmental-position/Social-Defense Band - Target-Direction Axis|Social-Defense Band]] -- diagnostic for whether reports are running fawn / fight / flee around the leader; the security posture of the team
