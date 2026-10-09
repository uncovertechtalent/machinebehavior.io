title: MITRE D3FEND
summary: MITRE's framework for defensive countermeasures.
parent: mitre
order: 100
labels: framework-concept, mitre
aliases: MITRE D3FEND | D3FEND | MITRE Defensive Countermeasures
type: framework-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/mitre/MITRE D3FEND.md
reviewed: no
---
> MITRE's framework for defensive countermeasures. Counterpart to ATT&CK on the defense side. Published 2021, funded by NSA. Provides taxonomy of defensive techniques mapped to the offensive techniques they counter.

## Structure

D3FEND organizes defensive countermeasures by tactic:

### Defensive tactics

1. **Model** — understand the environment / adversary.
2. **Harden** — make systems more resistant to attack.
3. **Detect** — discover adversary activity.
4. **Isolate** — limit adversary movement.
5. **Deceive** — confuse / mislead the adversary.
6. **Evict** — remove adversary from the environment.

### Defensive techniques

Per tactic, specific defensive methods:

- **Harden**: Application Hardening, Credential Hardening, Message Hardening, Platform Hardening.
- **Detect**: File Analysis, Identifier Analysis, Network Traffic Analysis, Platform Monitoring, Process Analysis, User Behavior Analysis.
- **Isolate**: Network Isolation, Execution Isolation.
- **Deceive**: Decoy Object, Decoy Environment.
- **Evict**: Credential Eviction, Process Eviction.

## D3FEND-ATT&CK mapping

For each ATT&CK technique, D3FEND identifies which defensive techniques can counter it. Bidirectional mapping:

- ATT&CK technique → relevant D3FEND defensive techniques.
- D3FEND defensive technique → ATT&CK techniques it addresses.

This enables control-selection workflows:

1. Identify ATT&CK techniques relevant to the org's threat model.
2. Look up D3FEND defensive techniques that counter them.
3. Select defensive techniques to implement.
4. Identify products / configurations / processes implementing the chosen defensive techniques.

## D3FEND digital artifact ontology

D3FEND uses an ontology of digital artifacts (files, processes, network traffic, etc.) to structure both adversary behavior and defensive countermeasures. Each artifact:

- Has properties (name, type, location, etc.).
- Has relationships (file contains, process executes, etc.).
- Is subject to specific defensive techniques.

The ontology supports formal reasoning about defense and is used by tooling to automate control mapping.

## D3FEND coverage maturity

D3FEND is younger than ATT&CK. Coverage varies:

- **Strong**: well-established defensive practices (anti-malware, network segmentation, identity protection).
- **Growing**: emerging defensive practices (deception, automation).
- **Lighter**: AI-specific defensive techniques.

D3FEND updates continuously with community contributions.

## Operational uses

### Control gap analysis

For each ATT&CK technique relevant to the org:

- What D3FEND defensive techniques counter it?
- Which of those defensive techniques does the org currently implement?
- What's missing?

Output: prioritized list of defensive capability gaps.

### Procurement evaluation

For security product procurement:

- What D3FEND defensive techniques does the product implement?
- What ATT&CK techniques does that coverage address?
- How does this product complement existing coverage?

### Architecture review

For new system designs:

- What ATT&CK techniques are relevant to this system's threat model?
- What D3FEND defensive techniques should be built in?

### Security strategy

For multi-year cybersecurity programs:

- Current state: D3FEND coverage assessment.
- Target state: enhanced D3FEND coverage.
- Roadmap: defensive techniques to add.

## Bridge to ISO 27001 Annex A

D3FEND defensive techniques map heavily to ISO 27001 Annex A:

- **Application Hardening** ≈ A.8.9 Configuration management, A.8.27 Secure architecture.
- **Credential Hardening** ≈ A.5.17 Authentication information, A.8.5 Secure authentication.
- **Network Isolation** ≈ A.8.22 Segregation of networks.
- **File Analysis** ≈ A.8.7 Protection against malware.
- **Process Analysis** ≈ A.8.16 Monitoring activities.
- **User Behavior Analysis** ≈ A.8.16 Monitoring activities.

D3FEND provides a different organizing axis than ISO 27001 controls — defensive-tactics-oriented vs control-category-oriented. Useful for cross-referencing.

## Bridge to NIST CSF

NIST CSF 2.0 functions (Govern, Identify, Protect, Detect, Respond, Recover) map onto D3FEND tactics broadly:

- Identify ≈ Model
- Protect ≈ Harden + Isolate + Deceive
- Detect ≈ Detect
- Respond ≈ Isolate + Evict
- Recover ≈ Evict + restoration practices outside D3FEND scope

Different abstraction levels: NIST CSF is high-level functions; D3FEND is specific defensive techniques.

## SRE and AI-agent fit notes

### Cloud-platform defensive mapping

D3FEND defensive techniques relevant to typical SRE / cloud work:

- Platform Monitoring → cloud-platform audit logging.
- Network Isolation → VPC segmentation, security groups, service mesh.
- Credential Hardening → MFA, passwordless auth, just-in-time access.
- Application Hardening → secure cloud-platform configurations.

### AI-feature defensive mapping (limited)

D3FEND has limited AI-specific defensive techniques currently. AI-feature defense draws from:

- D3FEND general defensive techniques.
- ATLAS-aware mitigations.
- OWASP LLM Top 10 mitigations.
- Practitioner-driven AI-specific patterns.

Future D3FEND expansion expected for AI-specific defense as the practice matures.

## Stefan-context implementation sketch

- For control selection: D3FEND-ATT&CK mapping as input.
- For client procurement: D3FEND coverage assessment for proposed products.

## See also

- [[MITRE Cluster|cluster MOC]] · [[MITRE ATT&CK]] · [[MITRE ATLAS]]
- [[ISO 27001 Annex A.8 Technological Controls]]
