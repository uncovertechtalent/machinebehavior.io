title: AI Agents are Ops Work
summary: Managing the lifecycle of an AI agent in production is operational engineering, not developer engineering.
parent: manifesto
order: 100
labels: ai-era-ops, manifesto, position
aliases: Agents as Ops | Agentic SRE
type: position
created: 2026-04-25
updated: 2026-06-08
origin: SRE/manifesto/AI Agents are Ops Work.md
reviewed: no
---
> Managing the lifecycle of an AI agent in production is operational engineering, not developer engineering. Agents need SLOs, error budgets, paging, and runbooks. Treat them like services because they fail like services.

## The category mistake

When companies first deploy LLM agents, the agents typically land on a developer team's plate. The result is predictable: outages happen during business hours because nobody is on standby, drift goes unnoticed because nobody is measuring quality, costs explode because nobody owns capacity, and prompt regressions ship because nobody runs canary deployments.

This happens because the developer team that built the agent treats it as their feature. Once the agent is in production, it stops being a feature and starts being a service. Services need operations.

## What an agent SLO looks like

Agents have measurable behavior at multiple layers:

| Layer | Example SLI | Common SLO |
|---|---|---|
| Latency | p95 time-to-first-token, p95 full response | < 3s TTFT, < 30s full |
| Availability | successful request rate excluding user errors | 99.5% over 30 days |
| Quality | rubric-graded response score on canary set | > 0.85 on weekly batch |
| Cost | token spend per request, per user, per day | within budget envelope |
| Tool reliability | tool-call success rate, tool-call latency | 99% success, p95 < 1s |
| Compaction integrity | survives N compactions without behavior drift | tested per release |

If you cannot answer these for a production agent, you do not have an operations posture. You have wishful thinking.

## What pages an SRE for an agent

- LLM provider outage (cascade if no fallback)
- Tool dependency outage (MCP server, vector DB, API gateway)
- Quality regression on canary set (often the silent killer)
- Cost spike (runaway loops, jailbroken sessions, prompt injection)
- Context-window saturation as steady-state behavior
- Auth/secret expiry on tool credentials

These are operational events. They wake someone up. They have rollbacks. They generate postmortems.

## The runtime is the new container

Just as containers introduced a new operational layer (Kubernetes, runtime security, container escape) that ops teams had to absorb, AI agents introduce a new operational layer: prompt regressions are the new dependency upgrades, context exhaustion is the new memory leak, tool-call failures are the new network partitions. The pattern repeats. Ops absorbs.

## Governance and risk frameworks for agentic systems

- [[ISO 42001 Cluster]] — AI Management System. Lifecycle + impact assessment + vendor relationships.
- [[NIST AI RMF Cluster]] — Govern / Map / Measure / Manage + GenAI Profile (200+ actions, 12 risk categories).
- [[OWASP LLM Top 10 Cluster]] — operational threat taxonomy. Particularly LLM06 Excessive Agency for agents.
- [[MITRE ATLAS]] — AI-specific adversary tactics.
- [[EU AI Act Cluster]] — regulatory tier obligations. High-risk system requirements 2026+.
- [[OECD AI Cluster]] — international voluntary principles.
- [[ISO 27001 Cluster]] — InfoSec management spine integrating with AI governance.

## See also

[[Compaction is the New OOM]] · [[Memory Architecture L0-L4]] · [[Graph-RAG over Flat RAG for Operational Knowledge]] · [[README]] (manifesto) · [[04-incident-management]] · [[ISO 42001 Cluster]] · [[OWASP LLM Top 10 Cluster]]
