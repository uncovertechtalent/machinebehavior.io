title: OWASP LLM Top 10 position
summary: Current view on what the OWASP Top 10 for LLM Applications is good for, what it is not good for, where it sits in the AI security landscape.
parent: owasp-llm-top-10
order: 5
labels: owasp-llm-top-10, position
aliases: OWASP LLM Top 10 Position | OWASP LLM Position
type: position
created: 2026-05-12
updated: 2026-05-12
origin: pillars/owasp-llm-top-10/position.md
reviewed: no
---
> Current view on what the OWASP Top 10 for LLM Applications is good for, what it is not good for, where it sits in the AI security landscape. Dated, revisable, diff-tracked.

## State of the view as of 2026-05-12

### What OWASP LLM Top 10 does well

- **Operational rather than governance-oriented.** Each risk has concrete attack scenarios and prevention guidance. Practitioners can act on the content directly.
- **Community-authored, vendor-neutral.** OWASP's open community model produces taxonomy that is not captured by any single vendor's interests.
- **Updates faster than ISO / NIST cycles.** v1.0 August 2023, v1.1 October 2023, v2.0 (2025) November 2024. Annual-ish revision tracks threat-landscape maturation.
- **De facto operational taxonomy.** Practitioner literature, test-suite tooling (PyRIT, Garak, Promptfoo), security-tool integrations, and red-team work increasingly organize around OWASP LLM Top 10 categories.
- **Risk descriptions are actionable.** Common examples, prevention strategies, attack scenarios per risk. Implementation teams can use the content directly.
- **Free and openly licensed.** Adoption barrier is zero. Translation into multiple languages.
- **Maps to adjacent frameworks.** NIST AI RMF GenAI Profile Category 9, ISO 42001 risk register inputs, MITRE ATLAS, traditional OWASP Web Top 10.
- **Working group continues to evolve.** Membership includes security practitioners, AI engineers, academics, vendors. Multi-perspective input.

### What OWASP LLM Top 10 does poorly

- **Only ten risks.** AI security risk space is broader. The "top 10" framing forces selection; some real risks fall outside the list.
- **Coverage of training-time risks is uneven.** Data and Model Poisoning (LLM04) covers training-time concerns but at high level; deep training-time threat coverage requires supplementary sources (MITRE ATLAS, academic literature).
- **Agent-system specifics need extension.** LLM06 Excessive Agency captures the umbrella; specific autonomous-agent threats (multi-agent collusion, tool-call chain injection, agent escalation) need practitioner extension.
- **Multimodal model coverage is light.** Image, audio, video input concerns are mentioned but not deeply covered. Multimodal-specific attacks (visual prompt injection, audio attacks) emerging faster than the taxonomy adapts.
- **Quantitative risk ranking is rough.** "Top 10" position reflects working-group consensus, not measured prevalence or severity data.
- **Mitigation guidance varies in depth.** Some risks have detailed prevention sections; others are general.
- **Not a complete AI security framework.** OWASP LLM Top 10 is taxonomy + guidance, not a comprehensive security program. Implementations layer it with broader frameworks (ISO 27001, ISO 42001, NIST 800-53, NIST AI RMF).

### Where the evidence currently sits

- **Practitioner adoption is high.** Most AI security writing, red-team reports, and security-tool documentation references OWASP LLM Top 10 categories.
- **Prompt injection (LLM01) is consistently the most active attack surface.** Direct, indirect (via RAG), tool-call-injected variants all evolving rapidly.
- **System Prompt Leakage (LLM07) emergence reflects practitioner experience.** Multiple high-profile leaks (system prompts of major LLM applications) drove the 2025 elevation to standalone risk.
- **Vector / Embedding Weaknesses (LLM08) is increasingly load-bearing** as RAG architectures dominate enterprise AI deployments.
- **Agent-system attacks (under LLM06) are evolving rapidly.** Multi-step prompt injection through tool calls, agent jailbreak chains, multi-agent collusion all emerging.
- **Defense maturation lags attack maturation.** OWASP LLM Top 10 v2.0 is current taxonomy; defensive tooling is still catching up.

## Personal calibration

- **Working assumption for agent system design:** LLM01, LLM05, LLM06, LLM07, LLM08 are the load-bearing risks. Threat model each agent against this subset; broader subset for higher-stakes agents.
- **Working assumption for evaluation harnesses:** OWASP LLM Top 10 categories provide test-suite scoping. Lightweight harness covering LLM01 prompt injection + LLM05 output handling + LLM06 agent scope abuse is a reasonable starting bar.
- **Working assumption for vendor evaluation:** model provider responses to OWASP LLM Top 10 (jailbreak defense, output filtering, prompt injection defense) inform vendor selection.
- **Working assumption for documentation:** AI risk register entries cite OWASP LLM ## category for clarity. Mature implementations also cite NIST AI RMF function and ISO 42001 control.

## What would shift this view

- **OWASP LLM Top 10 v3.0** (plausibly 2025-2026) — substantive revision reflecting agent-system maturity. Will be the bigger update than 2023-2025 was.
- **Quantitative risk-ranking data publication.** If OWASP working group publishes prevalence / severity data alongside categories, the prioritization weight hardens.
- **Multimodal extension.** Dedicated multimodal AI Top 10 (or LLM Top 10 multimodal expansion) would address current coverage gap.
- **Agent-specific Top 10.** Some practitioners argue agent systems deserve their own Top 10 separate from LLM applications. OWASP working group has not committed; pressure growing.

## See also

- [[OWASP LLM Top 10 Cluster|cluster MOC]] · [[OWASP LLM Top 10 Controversies]]
- [anchors](pillars/owasp-llm-top-10/anchors.md)
