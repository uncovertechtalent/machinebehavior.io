title: OWASP LLM Top 10
summary: Map of the OWASP Top 10 for LLM Applications.
parent: index
order: 160
labels: ai-security, moc, owasp-llm-top-10, threat-taxonomies
aliases: OWASP LLM Top 10 Cluster | OWASP LLM Top 10 | OWASP Top 10 for LLM Applications | OWASP LLM | LLM Top 10 2025
type: MOC
created: 2026-05-12
updated: 2026-06-08
origin: pillars/owasp-llm-top-10/OWASP LLM Top 10 Cluster.md
reviewed: no
---
> Map of the OWASP Top 10 for LLM Applications. Current version: 2025 (published November 2024). Operational threat taxonomy for LLM-integrated applications and agent systems. Reference cluster for technical AI security work and as input to NIST AI RMF / ISO 42001 risk registers.

## Anchors

- [position](pillars/owasp-llm-top-10/position.md): current view, dated, revisable
- [anchors](pillars/owasp-llm-top-10/anchors.md): OWASP, working group, related projects

## Provenance

- **OWASP Foundation** — Open Worldwide Application Security Project. Long-standing application-security community known for the OWASP Web Top 10 (since 2003), OWASP API Security Top 10, OWASP ASVS, OWASP SAMM, OWASP Mobile Top 10, others.
- **OWASP LLM AI Cybersecurity & Governance Initiative** — established 2023.
- **LLM Top 10 v1.0** — first published August 2023.
- **LLM Top 10 v1.1** — revision October 2023; minor refinements.
- **LLM Top 10 v2.0 (2025 edition)** — published November 2024. Substantial revision reflecting one year of practitioner experience. Several risks renamed, merged, or replaced.

## What the OWASP LLM Top 10 is, in one paragraph

A consensus list of the ten most critical security risks for LLM-integrated applications. Authored by a working group of security practitioners, AI engineers, and academics. Operational rather than governance-focused: each risk has description, common examples, prevention guidance, attack scenarios. Maps onto NIST AI RMF Category 9 (Information Security) of the GenAI Profile, ISO 42001 risk register inputs, and MITRE ATLAS adversary tactics. The de facto operational threat taxonomy for LLM application security.

## The 2025 list (current as of 2026-05-12)

- **LLM01:2025 Prompt Injection** — adversarial input causing the LLM to behave outside intended scope. Direct (in user prompt) and indirect (in retrieved or tool-returned content).
- **LLM02:2025 Sensitive Information Disclosure** — LLM exposing sensitive data (PII, secrets, business-confidential) through outputs. Renamed and broadened from 2023 v1.1.
- **LLM03:2025 Supply Chain** — vulnerabilities in model, training data, dependencies, plugins, agent framework components.
- **LLM04:2025 Data and Model Poisoning** — adversarial manipulation of training data, fine-tuning data, RAG corpus, or model itself.
- **LLM05:2025 Improper Output Handling** — insufficient validation/sanitization of LLM output before downstream use. Outputs treated as trustworthy and fed to executors / browsers / SQL / shell.
- **LLM06:2025 Excessive Agency** — agents granted overly-broad tool access, autonomy, or autonomy-without-oversight. Tool misuse, irreversible actions, scope creep.
- **LLM07:2025 System Prompt Leakage (NEW)** — system prompt revealing to user, often via prompt injection. System prompt may contain instructions, credentials, business logic.
- **LLM08:2025 Vector and Embedding Weaknesses (NEW, RAG-specific)** — vulnerabilities in retrieval-augmented generation pipelines: corpus poisoning, embedding manipulation, retrieval-time injection.
- **LLM09:2025 Misinformation** — LLM generating false or misleading content. Renamed from Overreliance (2023 v1.1); broader framing.
- **LLM10:2025 Unbounded Consumption** — resource exhaustion attacks; model API quota / token-spend / compute DoS. Replaces 2023's Model DoS and absorbs aspects of Model Theft framing.

Detail per risk in [[OWASP LLM Top 10 2025]].

## Changes from 2023 v1.1 to 2025

- **LLM07 (NEW)**: System Prompt Leakage. Was implicit in 2023 v1.1; promoted to standalone risk.
- **LLM08 (NEW)**: Vector and Embedding Weaknesses. New as RAG architectures became dominant.
- **Renamed**: Insecure Plugin Design (v1.1 LLM07) absorbed into LLM06 Excessive Agency.
- **Renamed**: Model Theft (v1.1 LLM10) consolidated into LLM10 Unbounded Consumption.
- **Renamed**: Overreliance (v1.1 LLM09) → LLM09 Misinformation (broader framing).
- **Renamed**: Sensitive Information Disclosure (v1.1 LLM06) → LLM02 (reflecting elevated importance).
- **Renamed**: Training Data Poisoning (v1.1 LLM03) → LLM04 Data and Model Poisoning (broader to cover RAG-corpus and inference-time data).
- **Reordered**: priorities shifted reflecting attacker maturation; Prompt Injection retains #1 position.

## Why this matters for SRE and AI-agent work

- **Operational threat taxonomy.** Provides the technical content that ISO 42001 / NIST AI RMF don't directly provide. Risk registers cite OWASP LLM categories for AI-specific entries.
- **Agent system relevance is high.** Excessive Agency (LLM06), Improper Output Handling (LLM05), System Prompt Leakage (LLM07) all directly relevant to agent systems with tools and complex prompts.
- **RAG architecture coverage** via Vector and Embedding Weaknesses (LLM08). Important for any system using retrieval-augmented generation.
- **Supply chain awareness** via Supply Chain (LLM03). Model provider, training data, dependency, plugin, framework supply chain all in scope.
- **Test-suite scaffolding.** Many practitioner test suites (PyRIT, Garak, Promptfoo) organize attacks by OWASP LLM Top 10 categories.

## Stefan-context relevance

Stefan does AI-agent work touching:

- Agent systems with tool use (LLM06 Excessive Agency directly relevant)
- System prompts containing business logic (LLM07 System Prompt Leakage)
- RAG architectures using vault content (LLM08 Vector and Embedding Weaknesses)
- Model API consumption from multiple vendors (LLM03 Supply Chain)
- Output handling where agent output feeds downstream processes (LLM05 Improper Output Handling)
- Customer-facing AI features (LLM02 Sensitive Information Disclosure, LLM09 Misinformation)

Cluster atoms should:

- Stay operationally grounded with example attack scenarios
- Bridge OWASP LLM Top 10 to ISO 42001 / NIST AI RMF risk registers
- Surface agent-system-specific concerns within each risk
- Provide actionable mitigation guidance

## Related clusters and atoms

- [[ISO 42001 Cluster|ISO 42001]] — AI management system; risk register input
- [[NIST AI RMF Cluster|NIST AI RMF]] — operational framework; LLM Top 10 maps to GenAI Profile Category 9
- [[EU AI Act Cluster|EU AI Act]] — regulatory layer; LLM Top 10 risks inform AI Act risk management
- [[ISO 27001 Cluster|ISO 27001]] — InfoSec management system; LLM risks integrate into InfoSec risk register

## Conventions for this cluster

- Atoms named `OWASP LLM <Topic>.md` with consistent structure
- 2025 version is the default reference
- Cross-link to ISO 42001 / NIST AI RMF where risks feed risk register
- All risks cite LLM##:2025 ID explicitly

## See also

[[OWASP LLM Top 10 Cluster]] (pillars MOC) · [position](pillars/owasp-llm-top-10/position.md) · [anchors](pillars/owasp-llm-top-10/anchors.md) · [[ISO 42001 Cluster]] · [[NIST AI RMF Cluster]]
