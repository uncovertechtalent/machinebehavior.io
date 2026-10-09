title: MITRE ATLAS
summary: Adversarial Threat Landscape for Artificial-Intelligence Systems.
parent: mitre
order: 100
labels: framework-concept, mitre
aliases: MITRE ATLAS | ATLAS | MITRE Adversarial Threat Landscape AI Systems | MITRE AI Threats
type: framework-concept
created: 2026-05-12
updated: 2026-06-08
origin: pillars/mitre/MITRE ATLAS.md
reviewed: no
---
> Adversarial Threat Landscape for Artificial-Intelligence Systems. MITRE's ATT&CK-style framework for adversary tactics and techniques against AI/ML systems. Published 2020; expanded 2021-2024 with generative-AI techniques.

## Structure

ATLAS mirrors ATT&CK structure adapted for AI / ML:

### Tactics

1. **Reconnaissance** — gather information about AI systems.
2. **Resource Development** — establish resources for AI attacks.
3. **Initial Access** — obtain access to AI system.
4. **ML Model Access** — gain access to model.
5. **Execution** — run malicious code in AI environment.
6. **Persistence** — maintain access to AI environment.
7. **Privilege Escalation** — escalate privileges.
8. **Defense Evasion** — avoid detection in AI context.
9. **Credential Access** — steal credentials affecting AI.
10. **Discovery** — discover AI environment details.
11. **Collection** — gather AI-related data.
12. **ML Attack Staging** — prepare ML-specific attacks.
13. **Exfiltration** — steal AI-related data.
14. **Impact** — affect AI system behavior or outputs.

### Techniques (selected, with IDs)

Notable ATLAS techniques relevant for agent-system work:

- **AML.T0000 Search Open Technical Databases** — recon on published AI literature.
- **AML.T0006 Active Scanning** — probe AI endpoints.
- **AML.T0010 ML Supply Chain Compromise** — compromise model / training data supply chain.
- **AML.T0018 Backdoor ML Model** — deliberate backdoor in model weights.
- **AML.T0019 Publish Poisoned Datasets** — poison public datasets used in training.
- **AML.T0024 Exfiltration via ML Inference API** — extract model via queries.
- **AML.T0040 ML Model Inference API Access** — abuse API access.
- **AML.T0043 Craft Adversarial Data** — adversarial input crafting.
- **AML.T0044 Full ML Model Access** — attacker has full model access.
- **AML.T0048 Societal Harm** — broad impact.
- **AML.T0051 LLM Prompt Injection** — prompt injection.
- **AML.T0052 Phishing via LLM** — LLM-generated phishing.
- **AML.T0053 LLM Jailbreak** — bypass model safety constraints.
- **AML.T0054 LLM Meta Prompt Extraction** — extract system prompt.
- **AML.T0055 Unsecured Credentials in LLM** — credentials in LLM training data.

(IDs may shift in updates; consult ATLAS for current.)

## Case studies

ATLAS includes documented real-world cases:

- **Microsoft Tay** — early adversarial conditioning of public-facing AI chatbot (2016).
- **Various model extraction attacks** on cloud-hosted ML APIs.
- **Adversarial-input attacks** on image classifiers.
- **LLM jailbreak demonstrations**.
- **Multi-modal adversarial attacks**.

Case studies updated as significant incidents become public.

## Mitigations

For each ATLAS technique, ATLAS catalogs:

- Mitigations (defensive practices).
- Detection approaches.
- Real-world incident references.

Mitigations draw on general security practice plus AI-specific countermeasures.

## ATLAS vs OWASP LLM Top 10

| Aspect | ATLAS | OWASP LLM Top 10 |
|---|---|---|
| Origin | MITRE | OWASP |
| Scope | All AI / ML (not just LLMs) | LLM-integrated applications |
| Structure | ATT&CK-style (14 tactics, many techniques) | Top 10 list |
| Adversary perspective | Yes (tactics, techniques, procedures) | Risk-oriented |
| Defense perspective | Mitigations per technique | Prevention guidance per risk |
| Maturity | Growing | Mature (2 years iteration) |
| Adoption | Growing in AI security community | Widely adopted |

Complementary, not competing. Use both:

- **OWASP LLM Top 10** for application-level risk taxonomy.
- **ATLAS** for adversary-modeling and TTP analysis.

## Contributors

Notable ATLAS contributors:

- **MITRE** (primary author).
- **Microsoft**.
- **Bosch**.
- **IBM**.
- **NVIDIA**.
- **Anthropic, OpenAI** (since GenAI focus expanded).
- **Various academic and practitioner contributors**.

## Update cadence

ATLAS updates as new techniques emerge from research and incidents. More frequent updates than ISO standards; less frequent than OWASP LLM Top 10 (which has shorter list).

## Operational uses

### AI feature threat modeling

For an AI feature:

1. Map system to ATLAS tactics relevant to its architecture (LLM-based, ML-based, multimodal, etc.).
2. Enumerate techniques per relevant tactic.
3. Map existing controls.
4. Identify gaps.
5. Plan mitigations.

### Red teaming AI systems

ATLAS-informed red teaming:

- Use ATLAS techniques as test suite.
- Cover relevant techniques per system.
- Report findings in ATLAS language.

### AI incident classification

Incidents involving AI systems classified by ATLAS technique:

- Aids cross-organization sharing.
- Builds threat intelligence base.

### AI-system risk register

ATLAS technique IDs as risk-entry references.

## Practitioner tooling

Tools using ATLAS / supporting ATLAS-informed work:

- **PyRIT** (Microsoft) — adversarial testing toolkit; some ATLAS alignment.
- **Garak** (NVIDIA) — LLM vulnerability scanner; ATLAS-relevant tests.
- **AI Verify** (Singapore) — testing toolkit including ATLAS-relevant tests.
- **Various academic tools** for adversarial ML research.

## SRE and AI-agent fit notes

### Most-load-bearing ATLAS techniques for agent systems

- AML.T0051 LLM Prompt Injection
- AML.T0053 LLM Jailbreak
- AML.T0054 LLM Meta Prompt Extraction (system prompt leakage)
- AML.T0043 Craft Adversarial Data
- AML.T0010 ML Supply Chain Compromise (model provider compromise)
- AML.T0040 ML Model Inference API Access (vendor API key abuse)
- AML.T0052 Phishing via LLM (defense — recognize LLM-generated phishing)

### Integration with non-AI ATT&CK

AI features are accessed via non-AI infrastructure. Combined threat model:

- Standard ATT&CK techniques for accessing the AI feature (cloud account compromise, valid accounts, etc.).
- ATLAS techniques for attacking the AI feature itself.
- Combined coverage essential.

## Stefan-context implementation sketch

- AI-feature threat modeling: ATLAS + OWASP LLM Top 10 as taxonomy.
- Red team work for client AI features: ATLAS-informed test plans.
- Risk register for client AI features: ATLAS technique IDs as references.

## See also

- [[MITRE Cluster|cluster MOC]] · [[MITRE ATT&CK]] · [[MITRE D3FEND]]
- [[OWASP LLM Top 10 2025]] (companion application-level taxonomy)
- [[NIST AI RMF GenAI Profile]] · [[ISO 42001 Annex A Controls]]
