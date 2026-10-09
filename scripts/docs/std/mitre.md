title: MITRE
summary: Map of MITRE's adversary-and-defense knowledge bases: ATT&CK (adversary tactics, techniques, procedures), D3FEND (defensive countermeasures), ATLAS (adversarial AI threats).
parent: index
order: 170
labels: adversary-frameworks, mitre, moc, threat-intelligence
aliases: MITRE Cluster | MITRE Adversary Frameworks | MITRE ATT&CK D3FEND ATLAS
type: MOC
created: 2026-05-12
updated: 2026-06-08
origin: pillars/mitre/MITRE Cluster.md
reviewed: no
---
# MITRE Adversary Frameworks Cluster

> Map of MITRE's adversary-and-defense knowledge bases: ATT&CK (adversary tactics, techniques, procedures), D3FEND (defensive countermeasures), ATLAS (adversarial AI threats). De facto operational threat-intelligence references. Reference cluster for threat modeling, incident response, security control selection, AI-specific adversarial threats. Free, openly licensed, community-maintained.

## Anchors

- [position](pillars/mitre/position.md): current view, dated, revisable
- [anchors](pillars/mitre/anchors.md): MITRE Corporation, contributing community

## Provenance

- **MITRE Corporation** — US federally funded research and development center (FFRDC). Operates multiple FFRDCs for US government.
- **ATT&CK** — first published 2013. Adversary tactics, techniques, procedures (TTPs) framework.
- **D3FEND** — published 2021. Defensive countermeasures framework. Funded by NSA.
- **ATLAS** — published 2020 (initial), 2021-2024 expanded. Adversarial Threat Landscape for AI Systems.

## What MITRE frameworks provide

Three complementary knowledge bases:

- **ATT&CK** — what adversaries do (offensive perspective).
- **D3FEND** — what defenders do (defensive perspective).
- **ATLAS** — what adversaries do against AI systems specifically.

Together provide the operational threat-intelligence and defense-mapping foundation for cybersecurity programs.

## ATT&CK overview

Adversary behaviors organized as:

- **Tactics** — adversary goals (e.g., Initial Access, Persistence, Lateral Movement, Exfiltration).
- **Techniques** — methods to achieve tactics (e.g., Phishing, Valid Accounts, PowerShell, Web Service).
- **Sub-techniques** — specific variations.
- **Procedures** — concrete implementations observed in the wild.

Multiple matrices: Enterprise, Mobile, ICS, Cloud variants.

Detail in [[MITRE ATT&CK]].

## D3FEND overview

Defensive countermeasures organized as:

- **Tactics** — defensive goals (e.g., Harden, Detect, Isolate, Deceive, Evict).
- **Techniques** — defensive methods (e.g., Application Hardening, File Analysis, Network Isolation).

Mapped to ATT&CK techniques — for each adversary technique, possible defensive countermeasures.

Detail in [[MITRE D3FEND]].

## ATLAS overview

AI-specific adversary tactics:

- Adapted ATT&CK structure for AI / ML systems.
- Tactics include ML Model Access, ML Attack Staging, Initial Access, Defense Evasion, Discovery, etc.
- Techniques include Adversarial ML Attack, Data Poisoning, Model Theft, ML Supply Chain Compromise, Prompt Injection.

Detail in [[MITRE ATLAS]].

## Why this matters for SRE and AI-agent work

- **Threat modeling** organized around adversary behavior produces realistic threat models.
- **Control selection** via D3FEND mapping to ATT&CK techniques.
- **AI-specific threats** captured in ATLAS — most operational taxonomy for AI adversaries.
- **Incident response** uses ATT&CK techniques as classification taxonomy.
- **Red team / blue team coordination** uses common ATT&CK language.
- **Security product evaluation** vendors map products to ATT&CK; comparison facilitated.

## Related clusters

- [[OWASP LLM Top 10 Cluster|OWASP LLM Top 10]] — application-level AI threat taxonomy; complementary to ATLAS
- [[NIST AI RMF Cluster|NIST AI RMF]] — threat-informed risk management
- [[ISO 27001 Cluster|ISO 27001]] — A.5.7 threat intelligence input source
- [[ISO 42001 Cluster|ISO 42001]] — AI-system threat input

## Conventions

- Atoms named `MITRE <Framework>.md`
- Specific technique IDs (e.g., T1566 Phishing, AML.T0051 Prompt Injection) cited explicitly
- Cross-link to OWASP LLM Top 10 / NIST AI RMF / ISO 27001

## See also

[[MITRE Cluster]] (pillars MOC) · [position](pillars/mitre/position.md) · [anchors](pillars/mitre/anchors.md) · [[OWASP LLM Top 10 Cluster]] · [[ISO 27001 Cluster]]
