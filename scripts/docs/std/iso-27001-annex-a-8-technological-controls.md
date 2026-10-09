title: ISO 27001 Annex A.8 Technological Controls
summary: Thirty-four controls: endpoint and access controls, malware protection, vulnerability management, configuration and change management, deletion / masking / DLP, backup and redundancy, logging and monitoring, network security, cryptography,.
parent: iso-27001
order: 100
labels: annex-a-theme, iso-27001, theme-technological
aliases: ISO 27001 Annex A.8 | ISO 27001 Technological Controls | Annex A.8 Controls
type: annex-a-theme
created: 2026-05-12
updated: 2026-06-08
origin: pillars/iso-27001/ISO 27001 Annex A.8 Technological Controls.md
reviewed: no
---
> Thirty-four controls: endpoint and access controls, malware protection, vulnerability management, configuration and change management, deletion / masking / DLP, backup and redundancy, logging and monitoring, network security, cryptography, secure development lifecycle, application security, secure coding, testing, environment separation, supplier-development, audit-testing protections. The largest engineering-led theme and the one most directly affected by the AI-system shift.

## How to read this atom

Each control listed below has its reference number and title from ISO 27001:2022 Annex A. Notes cover purpose, typical implementation, common evidence, SRE / AI-agent fit notes.

New controls in :2022 (eight of the eleven new controls live in A.8): A.8.9, A.8.10, A.8.11, A.8.12, A.8.16, A.8.23, A.8.28.

## A.8.1 User endpoint devices

Information on user endpoint devices is protected. Encryption at rest, MDM where applicable, posture compliance, EDR, separation of business and personal use.

## A.8.2 Privileged access rights

Privileged access allocated and used restrictively. Just-in-time access, time-limited grants, named accounts (no shared admin), audit logging of privileged actions.

AI-agent fit: agents granted tool access with administrative scope are privileged-access holders. Apply: scope tightening, audit logging of agent privileged actions, time-limited tokens, human approval gate for highest-scope tool calls.

## A.8.3 Information access restriction

Access to information restricted per access control policy. Need-to-know basis.

## A.8.4 Access to source code

Source code repositories controlled. Read access typically broad within engineering; write access controlled; protected branches; mandatory review.

AI-agent fit: agent coding assistants (Copilot, Claude Code, etc.) have read and sometimes write access to source code. Treat them as privileged identities under A.8.4. License-and-IP considerations under A.5.32.

## A.8.5 Secure authentication

Authentication technologies appropriate to the access risk. MFA for sensitive systems, phishing-resistant factors (FIDO2 / WebAuthn) for highest-sensitivity, password policy aligned with NIST 800-63B current guidance (length over complexity, no forced periodic rotation absent compromise indication).

## A.8.6 Capacity management

Capacity managed to meet current and projected demand. Performance monitoring, capacity planning, scaling procedures.

## A.8.7 Protection against malware

Anti-malware on endpoints and servers. EDR/XDR, behavior-based detection, sandboxing of untrusted content, awareness training (A.6.3 link).

## A.8.8 Management of technical vulnerabilities

Vulnerability identification, assessment, treatment. CVE scanning, dependency scanning, secrets scanning, periodic penetration testing, bug bounty (where mature), patch management.

Patch SLA aligned with severity: critical 7 days, high 30 days, medium 90 days (typical baseline; org calibrates per risk).

## A.8.9 Configuration management (NEW)

Configurations of hardware, software, services, networks established, documented, monitored, reviewed. Baselines, drift detection, configuration-as-code.

AI-agent fit: configurations include model versions, system prompts, tool scopes, retrieval-corpus configurations, embedding model versions, vector DB settings. Treat them as version-controlled configuration artefacts. Drift between documented and deployed = nonconformity under Cl 10.

## A.8.10 Information deletion (NEW)

Information no longer required is deleted. Right-to-erasure obligations under GDPR. Vendor-side deletion (cloud, model providers) confirmed contractually and operationally.

AI-agent fit: model providers' retention defaults vary (training-data-use, abuse-monitoring retention, conversation history). Enterprise tiers typically offer zero-retention or short-retention options. Document the chosen tier per vendor; verify periodically.

## A.8.11 Data masking (NEW)

PII and other sensitive data masked / tokenized / anonymized where the full data is not required. Production data in test environments masked; data shared with third parties masked.

AI-agent fit: data shipped to model APIs masked where the agent can operate on masked data. Common pattern: replace customer-identifying tokens with synthetic equivalents pre-API-call, de-mask post-response.

## A.8.12 Data leakage prevention (NEW)

DLP controls on endpoints, networks, cloud. Outbound monitoring, egress filtering, copy-paste restrictions, watermarking.

AI-agent fit: monitor agent output channels for PII leakage. Tools: structured output validation, regex / classifier-based detection on agent response payloads, blocked categories on outbound paths.

## A.8.13 Information backup

Backup of information and systems. Restoration testing. Off-site / cross-region copies.

3-2-1 rule (three copies, two media, one off-site) is a common baseline.

## A.8.14 Redundancy of information processing facilities

Redundancy sufficient to meet availability requirements. HA architectures, multi-region, failover testing.

## A.8.15 Logging

Logs produced, stored, protected, reviewed. User activity, exceptions, faults, security events.

AI-agent fit: agent action logs are first-class. Capture: input context (prompt + retrieved context + tool-call inputs), model version, agent identity, tool-call outputs, decision rationale where available, downstream effects. Retention per A.5.31 obligations.

## A.8.16 Monitoring activities (NEW)

Networks, systems, applications monitored for anomalous behavior; appropriate actions taken on detection. SIEM, SOC capability, automated response.

AI-agent fit: anomaly detection on agent behavior. Examples: unusual tool-call patterns, off-distribution prompts, output classifications outside trained distribution, vendor-side latency / error anomalies that may indicate model behavior changes.

## A.8.17 Clock synchronization

Clocks synchronized to approved time sources. Forensic evidence quality depends on this.

## A.8.18 Use of privileged utility programs

Privileged utilities (debuggers, registry editors, raw network tools, root-equivalent CLI access, agent-level tool runners) restricted and monitored.

## A.8.19 Installation of software on operational systems

Software installation controlled. Approved-software lists, package signing, EDR allow-list / deny-list, container image policy.

AI-agent fit: agents installing software on dev / prod systems are doing controlled installation. Apply A.8.19 (approval, logging) to agent-initiated installs.

## A.8.20 Networks security

Networks secured. Segmentation, perimeter, ingress / egress controls, NAC, encryption in transit.

## A.8.21 Security of network services

Network services secured. Service-level agreements, monitoring, periodic review.

## A.8.22 Segregation of networks

Network segregation between functional / sensitivity zones. Per-environment segregation (dev / test / prod), per-tenant in multi-tenant, per-risk-class within prod.

## A.8.23 Web filtering (NEW)

Outbound web access filtered. Malicious-site blocking, content-category filtering, DNS filtering.

## A.8.24 Use of cryptography

Cryptography policy and procedures. Key management, approved algorithms, key rotation, post-quantum migration planning.

Current algorithm baselines (2026): AES-256-GCM symmetric, ChaCha20-Poly1305 alternative, RSA-3072 / Ed25519 / ECDSA P-384 asymmetric, SHA-256 / SHA-3 hashing, TLS 1.3 transport. Post-quantum: NIST-selected ML-KEM (Kyber), ML-DSA (Dilithium), SLH-DSA (SPHINCS+) — migration planning expected by mature audits.

## A.8.25 Secure development life cycle

SDLC with security integrated throughout. Requirements, threat modelling, secure design, secure coding, testing, deployment review, post-deployment monitoring, EOL.

## A.8.26 Application security requirements

Security requirements specified for applications. Functional security (authn, authz, audit), non-functional (cryptography, availability), regulatory (data residency, retention).

## A.8.27 Secure system architecture and engineering principles

Secure-by-design principles applied. Defense in depth, least privilege, fail-secure, separation of concerns, secure defaults.

AI-agent fit: secure-by-design for agent systems means: smallest-tool-scope-by-default, mandatory-output-validation, immutable-audit-logs, time-delayed-execution-for-irreversible-actions, two-agent-design for high-stakes actions, no-implicit-trust-of-retrieved-context.

## A.8.28 Secure coding (NEW)

Secure coding standards applied. OWASP guidance, language-specific guidelines, code review with security focus, SAST in CI.

AI-agent fit: extends to "secure prompting" and tool-scope design. System prompts treated as code: version controlled, peer reviewed, tested. Tool definitions treated as API contracts with security review. OWASP LLM Top 10 covers the new failure modes.

## A.8.29 Security testing in development and acceptance

Security testing throughout SDLC. SAST, DAST, SCA, IAST, penetration testing, fuzz testing, red team exercises.

AI-agent fit: prompt-injection testing, tool-misuse testing, output-validation testing, jailbreak testing. Tools: PyRIT (Microsoft), Garak (NVIDIA), Promptfoo, vendor-specific eval harnesses.

## A.8.30 Outsourced development

Outsourced development supervised and monitored. Contractual requirements, security review of deliverables, source code escrow where applicable.

AI-agent fit: outsourced development includes AI-coding-assistant-generated code. Treat AI-coding-tool output as outsourced-development output for review purposes: same security review, same testing, no exemption based on perceived AI competence.

## A.8.31 Separation of development, test and production environments

Dev, test, prod separated. Different credentials, different data, different network zones.

## A.8.32 Change management

Changes to information processing facilities and systems controlled. Change requests, security review where applicable, approval, post-change verification, rollback plans.

Mirrors and extends Cl 6.3 (planning of changes) into operations.

## A.8.33 Test information

Test data selected, protected, managed. Production data in test = subject to A.8.11 masking; synthetic data preferred for sensitive scenarios.

## A.8.34 Protection of information systems during audit testing

Audit testing controlled to avoid disrupting operations. Pre-agreed scope, change-windows, read-only credentials where possible, rollback procedures.

## SRE and AI-agent quick map (load-bearing A.8 controls)

| Concern | Primary A.8 controls |
|---|---|
| Agent identity, scope, and audit | A.8.2, A.8.4, A.8.5, A.8.15, A.8.16, A.8.18 |
| System prompts and tool definitions as code | A.8.9, A.8.25, A.8.28, A.8.32 |
| Model version drift and provider relationships | A.8.9, A.8.32, A.5.22, A.5.23 |
| Data handling in / out of model APIs | A.8.10, A.8.11, A.8.12, A.8.24 |
| Prompt-injection and jailbreak resistance | A.8.27, A.8.28, A.8.29 |
| Agent action logging and monitoring | A.8.15, A.8.16, A.8.17 |
| Network security for agent infrastructure | A.8.20, A.8.21, A.8.22, A.8.23 |
| Backup and recovery for vault and bd databases | A.8.13, A.8.14 |
| AI-coding-assistant-generated code review | A.8.4, A.8.28, A.8.30 |

## Common audit observations

- **A.8.28 secure coding not extended to prompting.** Standard SAST coverage exists; system prompts and tool definitions reviewed informally if at all. Increasingly flagged in 2025+ audits.
- **Configuration management (A.8.9) excludes prompts and tool scopes.** Code in CM, prompts in someone's terminal history. Major gap.
- **A.8.16 monitoring activities does not include agent behavior.** SIEM watches infrastructure but not agent decisions. Gap for orgs operating production AI features.
- **A.8.30 not applied to AI-coding-assistant output.** "It's just our developer using a tool" — but the output is third-party-generated and merits the same supervision as outsourced developer output.
- **Post-quantum migration planning absent.** A.8.24 expects forward planning. Not yet a major-nonconformity item but increasingly observation-level by mature auditors.

## Stefan-context implementation sketch

- A.8.9 configuration management: vault git history covers documents; system prompts and skill definitions in `~/.claude/skills/` and `~/work/opskit/` under git equivalent (rsync from mac canonical). Document the canonicality.
- A.8.15 logging: bd action history, vault git log, model-provider request logs (where retention permits). Define retention.
- A.8.16 monitoring: lightweight self-applied — review bd activity, vault commits, vendor billing for anomaly indication.
- A.8.24 cryptography: FileVault on macOS, SSH keys via OpenSSH defaults (Ed25519), age / GPG for at-rest sensitive items, TLS 1.3 enforced where configurable.
- A.8.28 secure coding: extend to system prompts (peer reviewed, versioned) and tool scopes (intentionally narrow, documented).
- A.8.29 security testing: lightweight self-test for agent setups, especially after vendor model version changes.

## See also

- [[ISO 27001 Cluster|cluster MOC]]
- [[ISO 27001 Annex A.5 Organizational Controls]] · [[ISO 27001 Annex A.6 People Controls]] · [[ISO 27001 Annex A.7 Physical Controls]]
- [[ISO 27001 Family and Sector Variants]] (ISO 27034 application security; ISO 27040 storage; OWASP LLM Top 10 link)
- [[SRE/pillars/08-security/index|SRE Security pillar]]
