title: Memory Architecture L0-L4
summary: A five-layer memory stack for AI coding agents: L0 context, L1 beads, L2 memories, L3 vault, L4 Hivemind.
parent: patterns
order: 100
labels: ai-agents, architecture, memory, pattern
aliases: L0-L4 | Hivemind Memory Stack | Memory Stack
type: pattern
created: 2026-04-25
updated: 2026-04-25
origin: SRE/patterns/Memory Architecture L0-L4.md
reviewed: no
---
> A five-layer memory stack for AI coding agents: L0 context, L1 beads, L2 memories, L3 vault, L4 Hivemind. Durability increases with layer number, speed decreases. Each layer has a flush mechanism. Compaction is a fundamental constraint, not a bug.

## The layers

**L0, Conversation Context (volatile).** The LLM's context window itself. Ephemeral. Subject to compaction: silent, total erasure when token limits hit. No warning, no summary. Design principle: treat L0 as expendable, externalise early.

**L1, Beads / Task Tracking (survives compaction).** A local git-backed graph issue tracker (`bd`) running on a Dolt database (MySQL-compatible, versioned) on the user's laptop, localhost:3307. Tracks active tasks, dependencies, notes, status. On compaction, the agent reloads via `bd prime`. Flush: `/sync` pushes volatile context into beads notes, think `fsync()`. Speed: milliseconds. See [[Dolt Versioned Database for Task State]].

**L2, Persistent Memories (survives sessions).** Key-value store of insights, decisions, operational constants, and session summaries. Saved via `/rem` at session end (REM sleep). Retrieved via `/recall <query>` at session start. Also `bd remember` for constants that auto-inject at every `bd prime`. Speed: fast, local JSON/SQLite. Durability: survives sessions.

**L3, Personal Vault (survives people).** An Obsidian knowledge vault (~5,500 markdown files) of curated runbooks, infra docs, project notes, scripts, references. Each engineer has their own. Indexed by a vault-search MCP server providing BM25-ranked full-text search. Flush: `git commit`. Survives people: knowledge persists independent of any single person's sessions. See [[BM25 Hybrid Retrieval for Graph-RAG]].

**L4, Hivemind (survives teams).** Shared knowledge layer. FastAPI service with hybrid search (BM25 keyword + Cohere semantic embeddings + cross-encoder reranking) over Confluence. Currently 12,125 chunks from 2,233 pages across 11 spaces. Incremental sync every 6 hours. Two access paths: OpenCode as MCP tool, and Orion web UI via OpenWebUI filter pipeline. Network call, sub-second. Survives teams.

## Design principles

Durability increases with layer number. L1 survives compaction. L2 survives sessions. L3 survives people. L4 survives teams. Speed decreases in the same direction because distance from the CPU grows.

Each layer has a natural flush mechanism: `/sync` for L1, `/rem` for L2, `git commit` for L3, Confluence publish for L4.

Recovery is automatic. `bd prime` plus agent config injection means zero manual recovery after compaction.

Compaction is not a bug to work around. It's the fundamental constraint that drives the whole architecture. Accept L0 as volatile, build durable layers underneath, the agent can lose its full context window and recover in seconds.

## Personal vs work deployment

**Personal deployment:** single-user vault, local Dolt, no L4. The stack collapses to L0-L3 with the engineer's own Obsidian vault as the authoritative source. Graph-RAG over `~/vault` with BM25 is the retrieval primitive.

**Work deployment:** L4 becomes the shared organisational layer. Each engineer still runs their own L1-L3 locally. Two engineers asking the same question get different answers because their personal layers shape the synthesis. Personalisation is free because L1-L3 are per-person. L4 is what the tribe knows, curated slowly by many hands.

## Session lifecycle

1. Session start: agent loads L1 (`bd prime`), L2 (`bd memories`), identity (AGENTS.md)
2. During work: agent reads from all layers, writes findings to L1 notes
3. Periodically: `/sync` flushes L0 to L1
4. Session end: `/rem` summarises into L2
5. Over time: engineer curates L3 vault
6. Continuously: L4 syncs from Confluence every 6 hours

## See also
[[LLM as Software-Defined CPU]] · [[Dolt Versioned Database for Task State]] · [[BM25 Hybrid Retrieval for Graph-RAG]] · [[Context Window Sizes and Effective Range]] · [[Personal Digital Twin Architecture]]
