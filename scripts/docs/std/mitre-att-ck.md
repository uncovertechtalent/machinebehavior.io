title: MITRE ATT&CK
summary: MITRE Adversarial Tactics, Techniques, and Common Knowledge framework.
parent: mitre
order: 100
labels: framework-concept, mitre
aliases: MITRE ATT&CK | ATT&CK | MITRE ATT&CK Framework | MITRE Adversary Tactics Techniques
type: framework-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/mitre/MITRE ATT&CK.md
reviewed: no
---
> MITRE Adversarial Tactics, Techniques, and Common Knowledge framework. The de facto operational taxonomy for adversary behavior. Multiple matrices covering different environments.

## Structure

### Tactics

High-level adversary objectives. Each tactic represents a "why" — what the adversary is trying to achieve at that step. Tactics in Enterprise ATT&CK matrix:

1. **Reconnaissance** — gather information
2. **Resource Development** — establish resources for operations
3. **Initial Access** — break into the network
4. **Execution** — run malicious code
5. **Persistence** — maintain foothold
6. **Privilege Escalation** — gain higher permissions
7. **Defense Evasion** — avoid detection
8. **Credential Access** — steal credentials
9. **Discovery** — understand the environment
10. **Lateral Movement** — move through the environment
11. **Collection** — gather data of interest
12. **Command and Control** — communicate with compromised systems
13. **Exfiltration** — steal data
14. **Impact** — manipulate, interrupt, destroy

### Techniques

How tactics are achieved. Each technique has:

- ID (e.g., T1566 Phishing)
- Description
- Sub-techniques (e.g., T1566.001 Spearphishing Attachment, T1566.002 Spearphishing Link)
- Procedure examples (concrete observed instances)
- Mitigations
- Detection methods
- Data sources / data components
- References to threat groups using the technique

### Procedures

Specific implementations of techniques observed in the wild. Linked to known threat groups (e.g., APT29, FIN7, Lazarus).

## ATT&CK matrices

### Enterprise

Most widely-used. Covers Windows, macOS, Linux, plus broader Enterprise tactics:

- Network
- Cloud platforms (AWS, Azure, GCP, Office 365, SaaS, Azure AD/Entra ID, Google Workspace)
- Containers
- ESXi (added 2024)

### Mobile

iOS and Android adversary techniques.

### ICS

Industrial Control Systems. Different tactic set including Process Manipulation, Inhibit Response Function, etc.

### Pre-ATT&CK (deprecated, merged into Reconnaissance + Resource Development tactics in Enterprise).

## Threat groups

ATT&CK catalogs known threat actors:

- **Nation-state APTs** (APT1 - APT41+, Lazarus, Sandworm, Turla, others)
- **Cybercrime groups** (FIN7, FIN8, Carbanak, Wizard Spider, Conti, others)
- **Ransomware operators** (LockBit, BlackCat/ALPHV, Royal, Akira, others)
- **Hacktivist groups**
- **Each group page** lists techniques used.

## Software catalog

ATT&CK catalogs:

- **Malware** families with techniques used.
- **Tools** (legitimate tools used adversarially — PsExec, Mimikatz, Cobalt Strike, etc.).

## Update cadence

ATT&CK updates ~twice per year (April + October). Updates include:

- New techniques
- New sub-techniques
- New threat groups
- New software
- Revised content for existing entries
- Major version changes occasionally

Current version as of 2026-05-12: v16 (October 2024) approximately.

## Operational uses

### Threat modeling

For a system / asset:

1. Identify relevant tactics (where in the kill chain is this asset vulnerable?).
2. Enumerate techniques per tactic relevant to the asset's tech stack.
3. Map existing controls to techniques.
4. Identify gaps.

### Detection engineering

For each technique relevant to the org:

- Identify data sources for detection.
- Build detections (SIEM rules, EDR rules).
- Test detections.
- Maintain detections as adversary tactics evolve.

ATT&CK provides data-source taxonomy supporting this work.

### Red teaming

Red teams plan engagements using ATT&CK techniques:

- Mimicking specific threat group TTPs.
- Comprehensive coverage testing.
- Reporting in ATT&CK language for cross-team understanding.

### Threat intelligence

Threat intel feeds tag indicators with ATT&CK technique IDs:

- Enables automated correlation.
- Common language across vendors.

### Risk assessment

For each control / system:

- Which ATT&CK techniques does it mitigate?
- Which techniques remain unmitigated?
- What's the residual risk?

### Procurement evaluation

Compare security vendor products by ATT&CK technique coverage:

- ATT&CK Evaluations published by MITRE Engenuity compare EDR/XDR products against specific threat group emulation.

## ATT&CK Navigator

Visualization tool:

- Highlight technique coverage by detection/prevention.
- Compare threat group technique sets.
- Identify gaps.

## Cloud-specific techniques

Important subset for SRE work. Cloud ATT&CK matrices cover:

- **AWS, Azure, GCP** platform-specific techniques.
- **Identity provider attacks** (Azure AD/Entra ID, Okta, Google Workspace).
- **Container attacks** (Kubernetes, Docker).
- **SaaS attacks** (Office 365, Google Workspace, Salesforce).

## SRE and AI-agent fit notes

### Cloud-platform threats

For typical SRE work, Cloud ATT&CK matrices most relevant:

- T1078.004 Valid Accounts: Cloud Accounts
- T1213.003 Data from Information Repositories: Code Repositories
- T1078.001 Valid Accounts: Default Accounts
- T1656 Impersonation
- T1098 Account Manipulation
- And many more.

### CI/CD attacks

ATT&CK covers CI/CD attacks (relevant for SRE / DevOps):

- Supply chain compromise (T1195)
- CI/CD pipeline poisoning
- Repository compromise

### AI features in non-AI tactics

AI features can be compromised via non-AI ATT&CK techniques (cloud account compromise, valid accounts, etc.). AI-specific tactics in ATLAS.

## Stefan-context implementation sketch

- Threat modeling for client systems: ATT&CK as taxonomy.
- Detection engineering work for clients with SIEM / EDR: ATT&CK as detection coverage taxonomy.
- AI-feature threat modeling: combine ATT&CK + ATLAS.

## See also

- [[MITRE Cluster|cluster MOC]] · [[MITRE D3FEND]] · [[MITRE ATLAS]]
- [[OWASP LLM Top 10 2025]] (application-level AI threat companion)
- [[ISO 27001 Annex A.5 Organizational Controls]] (A.5.7 threat intelligence)
