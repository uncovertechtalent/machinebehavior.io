title: OWASP LLM vs Top 10 Web
summary: The OWASP Top 10 for Web Applications (since 2003, current 2021 edition) and the OWASP LLM Top 10 (since 2023, current 2025 edition) are sibling Top 10 lists with overlapping but distinct concerns.
parent: owasp-llm-top-10
order: 100
labels: cross-cutting, owasp-llm-top-10
aliases: OWASP LLM vs Top 10 Web | OWASP LLM vs OWASP Web Top 10 | LLM Top 10 vs Web Top 10 Comparison
type: cross-cutting
created: 2026-05-12
updated: 2026-06-08
origin: pillars/owasp-llm-top-10/OWASP LLM vs Top 10 Web.md
reviewed: no
---
# OWASP LLM Top 10 vs OWASP Top 10 (Web)

> The OWASP Top 10 for Web Applications (since 2003, current 2021 edition) and the OWASP LLM Top 10 (since 2023, current 2025 edition) are sibling Top 10 lists with overlapping but distinct concerns. LLM applications are web applications; they inherit web-app concerns and add LLM-specific ones. This atom maps the overlap and the LLM-specific delta.

## Side-by-side mechanics

| Aspect | OWASP Top 10 (Web) | OWASP LLM Top 10 |
|---|---|---|
| Origin | 2003 | 2023 |
| Current edition | 2021 | 2025 (Nov 2024) |
| Revision cycle | ~4-year | ~Annual |
| Scope | Web applications | LLM-integrated applications |
| Audience | Web developers, app sec teams | AI engineers, AI app sec teams |
| Risk count | 10 | 10 |
| Maturity | Established | Emerging |
| Practitioner adoption | Universal in web security | High in AI security |
| Test tooling | Mature (Burp, ZAP, Nuclei, etc.) | Growing (PyRIT, Garak, Promptfoo) |

## OWASP Top 10 (2021 Web edition) — for context

The current web Top 10:

- A01:2021 Broken Access Control
- A02:2021 Cryptographic Failures
- A03:2021 Injection (SQL, NoSQL, OS command, XSS)
- A04:2021 Insecure Design
- A05:2021 Security Misconfiguration
- A06:2021 Vulnerable and Outdated Components
- A07:2021 Identification and Authentication Failures
- A08:2021 Software and Data Integrity Failures
- A09:2021 Security Logging and Monitoring Failures
- A10:2021 Server-Side Request Forgery (SSRF)

## How web Top 10 concerns appear in LLM applications

LLM applications inherit all web-app concerns. The mapping:

### A01 Broken Access Control → still applies

LLM apps need access control over: which users can use which LLM features, which data the LLM can retrieve, which tools the agent can call, multi-tenant isolation. LLM-specific manifestations: tenant data leakage via RAG (overlap with LLM02 / LLM08), agent action authorization (overlap with LLM06).

### A02 Cryptographic Failures → still applies

LLM apps handle sensitive data (prompts, completions, training data, RAG content). Cryptographic controls (TLS, at-rest encryption, key management) apply. Vendor-side encryption commitments under DPAs.

### A03 Injection → re-emerges in new form

Traditional injection (SQL, command, XSS) still applies when LLM output is used by downstream executors. LLM-specific manifestation: prompt injection (LLM01) — a distinct category needing distinct controls. LLM05 Improper Output Handling overlaps where LLM-generated content feeds executors.

### A04 Insecure Design → still applies

LLM application architecture decisions (where to put guardrails, how to scope agents, how to handle errors) are design choices. Cross-references LLM06 Excessive Agency at design level.

### A05 Security Misconfiguration → still applies

Default-permissive plugin configurations, model API keys with broad scope, RAG-corpus access without restriction — all manifestations of misconfiguration in LLM apps.

### A06 Vulnerable and Outdated Components → still applies

Dependency vulnerabilities in langchain, llamaindex, agent framework, plugins. LLM-specific manifestation: LLM03 Supply Chain at framework / dependency layer.

### A07 Identification and Authentication Failures → still applies

LLM apps still authenticate users; tokens still leak. LLM-specific manifestation: when the LLM is given long-lived service-account credentials with broad scope (overlap with LLM06 Excessive Agency).

### A08 Software and Data Integrity Failures → still applies

Pipeline integrity, dependency signing, training data integrity. LLM-specific manifestation: LLM04 Data and Model Poisoning at training-data and RAG-corpus layers.

### A09 Security Logging and Monitoring Failures → still applies

LLM apps need logging across the inference pipeline: prompt content, model version, retrieved context, tool calls, outputs. Failure here makes incident response impossible.

### A10 Server-Side Request Forgery (SSRF) → still applies

LLM apps with web-fetching tools can be tricked into SSRF via prompt injection (overlap with LLM01) or via RAG retrieval of attacker-controlled URLs.

## What LLM Top 10 adds beyond web Top 10

LLM Top 10 risks not directly covered by web Top 10:

- **LLM01 Prompt Injection** — fundamentally different from traditional injection. Adversarial input acts on the model itself, not on a downstream executor.
- **LLM02 Sensitive Information Disclosure** (LLM-specific aspects) — memorization, inference attacks, context leakage. Some overlap with A01 Broken Access Control but LLM mechanisms are distinct.
- **LLM04 Data and Model Poisoning** — training-data and model-integrity concerns. Some overlap with A08 but mechanisms are LLM-specific.
- **LLM06 Excessive Agency** — autonomy and scope concerns specific to agent systems.
- **LLM07 System Prompt Leakage** — model-specific concern; no web-Top-10 equivalent.
- **LLM08 Vector and Embedding Weaknesses** — RAG-specific. No web-Top-10 analog.
- **LLM09 Misinformation** — hallucination and confabulation. Distinct from web-Top-10 concerns.
- **LLM10 Unbounded Consumption** — token-spend / model-API-resource DoS. Web Top 10 has resource concerns generally; LLM specifics differ.

## What web Top 10 covers that LLM Top 10 doesn't directly

- **A01 Access Control** — full coverage in web Top 10; LLM Top 10 touches via LLM02 / LLM06 / LLM08 but doesn't centralize.
- **A02 Cryptographic Failures** — not in LLM Top 10; remains a web Top 10 concern.
- **A05 Security Misconfiguration** — not in LLM Top 10 directly.
- **A07 Authentication Failures** — not in LLM Top 10 directly.
- **A10 SSRF** — not in LLM Top 10 directly.

## Combined implementation pattern

For LLM applications, security work needs both:

- **Web Top 10 coverage** for the application platform itself.
- **LLM Top 10 coverage** for LLM-specific concerns.

Combined coverage uses:

- Traditional appsec tooling (Burp, ZAP, SAST, DAST) for web Top 10 categories.
- LLM-specific tooling (PyRIT, Garak, Promptfoo) for LLM Top 10 categories.
- Combined red teaming covering both layers.

Treating LLM apps as "just AI" misses the web Top 10 inheritance. Treating LLM apps as "just web" misses the LLM Top 10 specifics. Both layers need attention.

## Cross-references

| OWASP LLM Top 10 risk | Closest OWASP Top 10 (Web) analog |
|---|---|
| LLM01 Prompt Injection | A03 Injection (new variant) |
| LLM02 Sensitive Information Disclosure | A01 Broken Access Control / A04 Insecure Design |
| LLM03 Supply Chain | A06 Vulnerable Components / A08 Integrity Failures |
| LLM04 Data and Model Poisoning | A08 Integrity Failures |
| LLM05 Improper Output Handling | A03 Injection (output side) |
| LLM06 Excessive Agency | A01 Broken Access Control / A04 Insecure Design |
| LLM07 System Prompt Leakage | A04 Insecure Design / A05 Misconfiguration |
| LLM08 Vector and Embedding Weaknesses | A01 + A03 + A04 (combined) |
| LLM09 Misinformation | A04 Insecure Design (output trust) |
| LLM10 Unbounded Consumption | A04 Insecure Design (rate limiting) |

## Implementation team implication

For an LLM-feature SaaS:

- **App sec team** continues covering web Top 10 as before.
- **AI / ML team** covers LLM Top 10 with cross-pollination to app sec.
- **Cross-team coordination** essential — LLM Top 10 risks have web-app implications and vice versa.

Single-team coverage is risky. Mature implementations have app sec + AI security as collaborative functions.

## See also

- [[OWASP LLM Top 10 Cluster|cluster MOC]] · [[OWASP LLM Top 10 2025]] · [[OWASP LLM Mitigations]]
- OWASP Top 10 (Web) 2021 — owasp.org/Top10/
