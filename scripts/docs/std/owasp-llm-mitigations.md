title: OWASP LLM Mitigations
summary: Cross-cutting defensive practices for LLM application security.
parent: owasp-llm-top-10
order: 100
labels: mitigations, owasp-llm-top-10
aliases: OWASP LLM Mitigations | OWASP LLM Defensive Practices | LLM Top 10 Mitigations | LLM Security Mitigations
type: mitigations
created: 2026-05-12
updated: 2026-06-08
origin: pillars/owasp-llm-top-10/OWASP LLM Mitigations.md
reviewed: no
---
> Cross-cutting defensive practices for LLM application security. Per-risk prevention is covered in [[OWASP LLM Top 10 2025]]. This atom captures patterns that work across multiple Top 10 categories.

## Defense in depth

No single control is reliable. Effective LLM application security layers multiple defenses:

- **Model-side defenses** (training-time): adversarial training, RLAIF, constitutional AI, jailbreak-resistance training. Provider responsibility primarily.
- **Application-side input controls**: prompt structuring, input validation, prompt-injection detection.
- **Application-side output controls**: schema validation, output filtering, structured outputs.
- **Application-side authorization**: agent privilege scoping, tool-call authorization, downstream-action gating.
- **Operational controls**: rate limiting, anomaly detection, audit logging.
- **Human-in-the-loop**: for high-stakes or irreversible actions.

Layering across model + application + operational reduces single-point-of-failure exposure.

## Prompt engineering for security

- **Structured prompts**: separate system instruction, retrieved context, user input clearly. Reduces injection success rate.
- **Output schema enforcement**: function calling, JSON schema validation, structured outputs reduce free-text-parsing attack surface.
- **Instruction hierarchy**: model-side support for instruction precedence (OpenAI's hierarchy work, Anthropic's similar) helps when properly used.
- **Sentinel patterns**: include patterns in system prompt that, if absent in retrieved context, signal injection attempt. Brittle but cheap.
- **Defensive prefixes**: instruct model to validate user input against intended use before responding. Limited effectiveness; useful as one layer.

## Input validation

- **Format validation**: enforce expected input structure where possible.
- **Length limits**: cap input length per use case.
- **Content filtering**: known-malicious patterns blocked (slow-moving baseline).
- **Provenance tagging**: retrieved content tagged with source for downstream filtering.
- **User input vs system input separation**: never mix in the model's context.

## Output validation

- **Schema validation**: enforce expected output structure.
- **Type checking**: outputs must match declared types (e.g., function arguments).
- **Content filtering**: detect prohibited content patterns (PII, credentials, injection markers).
- **Confidence thresholds**: route low-confidence outputs to human review.
- **Citation verification** for fact-claiming outputs.
- **Sandbox before execute**: any LLM-generated executable content runs in a sandbox.

## Authorization and scope

- **Least privilege for agents**: tools at minimum capability needed.
- **Just-in-time credentials**: short-lived, scope-limited credentials per agent invocation.
- **Per-tool authorization decisions**: explicit user authorization for sensitive tool calls.
- **Tenant isolation**: per-tenant agent context, no cross-tenant data leakage.
- **Capability tokens**: cryptographic tokens authorizing specific tool capabilities.
- **Kill switches**: ability to disable agent in real-time.

## Human-in-the-loop patterns

- **Approve-then-execute**: agent proposes action; human approves before execution.
- **Irreversibility gates**: irreversible actions always require human approval.
- **Time-delayed execution**: actions queued with delay allowing review.
- **Anomaly escalation**: anomalous agent behavior triggers human review.
- **Sampling review**: random sample of agent actions reviewed for quality / safety.

## Monitoring and observability

- **Agent action audit logging**: input context, model version, tool calls, outputs, decisions.
- **Behavioral monitoring**: detect anomalies in agent action patterns.
- **Vendor-side change detection**: monitor for changes in model behavior that may signal vendor-side updates.
- **Token spend / quota monitoring**: cost anomalies often signal attack or runaway agent.
- **Output content monitoring**: surface PII leakage, prohibited content patterns.
- **User feedback loops**: capture user reports of bad agent behavior.

## Vendor management

- **Due diligence**: model provider security posture, jailbreak-handling commitments, DPA terms.
- **DPA**: data processing agreement covering AI-system specifics (no training on customer data, retention windows, sub-processor approvals).
- **SOC 2 / ISO 27001 / ISO 42001 review**: vendor's certifications and audit reports.
- **Ongoing monitoring**: vendor TOS changes, vendor security advisories, vendor incident reports.
- **Exit strategy**: ability to switch vendors documented and tested.

## Supply chain

- **SBOM** for LLM application stack: model, framework, dependencies, plugins, tools.
- **Dependency pinning** and vulnerability monitoring (Snyk, Dependabot, OSV).
- **Plugin / tool security review** before adoption.
- **Model integrity verification** (signed weights where available).
- **Provenance documentation** for training data (where org trains/fine-tunes).

## Rate limiting and resource controls

- **Per-user rate limits** at multiple layers.
- **Token-spend budgets** with monitoring and alerts.
- **Cost anomaly detection**.
- **Input length limits**.
- **Output length limits**.
- **Query complexity heuristics**.
- **Vector-store query rate limits** (for RAG).

## Adversarial testing

- **Red teaming**: planned adversarial testing per release. Internal or external red teams.
- **Automated security testing**: PyRIT, Garak, Promptfoo, custom harnesses.
- **OWASP LLM Top 10 coverage** in test suite.
- **Vendor-provided eval suites** where available.
- **Regression testing**: prevent re-introduction of known vulnerabilities.

## Incident response

- **AI-incident classification**: distinguish AI-related incidents from general security incidents.
- **Containment patterns**: agent kill-switches, vendor-side API key revocation, RAG-corpus quarantine.
- **Investigation tooling**: audit logs sufficient to reconstruct incident.
- **Vendor coordination**: incident notification flows with model providers, framework authors.
- **Post-incident review**: lessons-learned feed back into prevention and detection.

## User education

- **Output trust calibration**: communicate model limitations clearly.
- **Distinguishing AI-generated from authoritative content**: UX cues, provenance metadata.
- **Bypass-attempt education**: train users to recognize when they're being manipulated by AI-mediated content.
- **Reporting channels**: easy paths for users to flag bad AI behavior.

## Layered architecture pattern

A defensible LLM application stack typically layers:

1. **User input** → application input validation → 
2. **Application** → prompt structuring → 
3. **Model API** → (model-side defenses) → response → 
4. **Application** → output validation → 
5. **Tool calls / executors** → authorization gates → 
6. **Downstream actions** → audit logging → 
7. **Operational monitoring** → anomaly detection → 
8. **Human review** for triggered cases.

Each layer narrows attack surface for the next.

## SRE and AI-agent applicability

For agent systems with tool use:

- **Defense in depth is mandatory.** No single control is sufficient.
- **Tool-scope discipline is load-bearing.** LLM06 Excessive Agency prevention starts here.
- **Audit logging is non-negotiable.** Without it, incident response is blind.
- **Human-in-the-loop on irreversible actions.** Even mature agent systems benefit.
- **Continuous adversarial testing.** Production agent systems should run regular eval suites.

## Stefan-context implementation sketch

For agent systems on personal infra / client work:

- **Input/output validation patterns** documented and reused across agents.
- **Tool scope** narrowed by default; expand explicitly with rationale.
- **Audit logging** via bd / vault / framework-provided logs; retention 12+ months.
- **Adversarial testing** lightweight per agent before deployment; deeper for client-facing.
- **Vendor management** documented per provider.
- **Kill switches** documented and tested.

## See also

- [[OWASP LLM Top 10 Cluster|cluster MOC]] · [[OWASP LLM Top 10 2025]] · [[OWASP LLM vs Top 10 Web]]
- [[NIST AI RMF GenAI Profile]] (MANAGE function actions overlap)
- [[ISO 42001 Annex A Controls]] (A.6 lifecycle, A.10 third-party)
