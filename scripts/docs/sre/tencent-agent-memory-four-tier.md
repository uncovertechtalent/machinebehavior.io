title: tencent-agent-memory-four-tier
summary: An open-source, fully-local memory layer that gives an agent human-like long-term recall, so it stops starting from scratch every session.
parent: patterns
order: 100
labels: agent-memory, rag, reference, sre-patterns
aliases: Tencent Agent Memory | Four-Tier Agent Memory | Local Agent Long-Term Recall | TencentDB Agent Memory
type: reference
created: 2026-08-07
updated: 2026-08-07
origin: SRE/patterns/tencent-agent-memory-four-tier.md
reviewed: no
---
# Tencent's four-tier agent memory system

> An open-source, fully-local memory layer that gives an agent human-like long-term recall, so it stops starting from scratch every session. Directly relevant as a reference point for the L0-L4 memory architecture: it is the same problem (durable memory across sessions to stop re-reading context) solved by an external vendor.

## What it is

- **The problem it targets:** every agent session starts cold. Close it, reopen, and it has no idea who you are, what you prefer, or what you were doing last week, so it burns context re-reading background.
- **The design:** a four-tier memory modeled on human memory. Short-term handles the current exchange; longer tiers store habits, preferences, and personality over time. It watches conversations, extracts key facts ("this user prefers Python," "wants concise responses"), and stores them in layers that sharpen with use.
- **Claimed gains:** ~61% lower token cost and >50% better task success, on the argument that the agent stops re-reading the same background each session. Treat these as vendor/creator figures, unverified.
- **Open-source and runs locally.** That is the load-bearing property for this corpus.

## Why it is here

A concrete external instance of the [[Memory Architecture L0-L4]] problem, useful as a comparison and a candidate. It maps roughly onto the personal stack: the "extract key facts and store in sharpening layers" is L2 (persistent memories), the session-context tier is L0, and the durability gradient is the same principle (durability up, speed down across tiers). Two reasons it fits the token-savings play in the local-migration token-savings principle: it is local (no paid-API memory calls) and its whole pitch is cutting token spend by not re-sending context. Worth evaluating against the existing vault-search / beads / memory setup rather than adopting blind, since the personal stack already covers L1-L3.

## See also

[[Memory Architecture L0-L4]] · [[BM25 Hybrid Retrieval for Graph-RAG]] · [[Compaction is the New OOM]]
