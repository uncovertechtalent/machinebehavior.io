title: Personal Digital Twin Architecture
summary: Per-person vault (private, IP-owned by the individual) plus a curated public projection (expertise, decisions, communication patterns).
parent: patterns
order: 100
labels: ai-agents, digital-twin, knowledge-management, pattern
aliases: Digital Twin | Personal Twin | Twin Architecture
type: pattern
created: 2026-04-25
updated: 2026-04-25
origin: SRE/patterns/Personal Digital Twin Architecture.md
reviewed: no
---
> Per-person vault (private, IP-owned by the individual) plus a curated public projection (expertise, decisions, communication patterns). The company layer is the aggregate of public projections. Knowledge survives when people leave; IP ownership stays with the person who created it.

## The three layers

**Private layer (per person).** The full Obsidian vault, raw, unfiltered, personal IP. Continuously enriched from Confluence, Jira, Slack, GitHub. Never leaves the individual's control. The source of truth for the twin. Contains the [[Memory Architecture L0-L4]] stack: L0 context, L1 beads, L2 memories, L3 vault.

**Public projection (per person).** A curated subset: expertise domains, decisions, published work, communication patterns. What the person chooses to expose. Not a sanitized PR version, an accurate professional representation. The "best public version" of the individual at realistic standards.

**Company layer (shared).** The aggregate of all public projections. An active entity, not a static knowledge base. It knows what the company knows, reasons about what the company can do, surfaces expertise, identifies gaps, routes questions to the right person or their twin. Roughly: a living org chart crossed with a knowledge graph crossed with an agent.

## Why the boundary matters

The private/public boundary is the key design decision and it's the right place to start.

Right now, when someone leaves a company, their knowledge walks out with them. Institutional memory gets rebuilt from scratch with every onboard. This architecture flips that: knowledge accumulation becomes a property of the org, not the headcount, while IP ownership stays with the person who generated it.

The twin is valuable because it's *specific* to the person: their decisions, their voice, their patterns. That specificity requires either per-person fine-tuning or heavy RAG against the individual vault. Pure retrieval against a shared base model with different context shaping is the cheaper path and the one that preserves sovereignty.

## What crosses the boundary

Private (stays local):
- Raw session notes and journals
- Personal frustrations, half-formed ideas, unfiltered opinions
- Client-confidential material
- Health, family, relationship content
- Anything that would embarrass the person if public

Public projection (curated):
- Published decisions and their rationale
- Areas of demonstrated expertise
- Communication patterns (how you ask, how you explain)
- Completed project artifacts
- Architectural diagrams, runbooks, postmortems
- Documented mentorship content

The curation itself has to be explicit consent plus tooling, not policy. Policy alone fails under load. The tooling needs to make the boundary visible and make exposure a deliberate act, not a default.

## The company layer as an active entity

Not a RAG over the combined public projections. An *organism*:

- Surfaces expertise ("who has shipped ingestion pipelines before?")
- Routes questions to the right person or their twin
- Identifies knowledge gaps (topics no projection covers)
- Tracks decision patterns across people
- Presents a queryable, interactive representation of the company

A centrally-hosted small language model acts as the intermediary. Purpose-built router and synthesizer, not a general-purpose LLM. Understands the graph of people, their knowledge domains, their relationships, their work history. Locally hosted for data sovereignty.

## Implementation constraints

The central SLM needs to be small enough to run locally (matters for GDPR, matters for client data). The per-person enrichment pipelines do heavy lifting: entity extraction, resolution, deduplication across four source systems. That's where the compute budget goes.

Identity boundary is the hard problem. The twin is only valuable because it's specific. Generic retrieval against a shared vault loses that specificity. Per-person fine-tuned adapters on top of a shared base are one option; pure RAG against each person's vault with a shared reasoning model is the other. The choice shapes the infrastructure model significantly.

## Why this is different from a knowledge base

A knowledge base is passive: you query it, it returns documents. A digital twin is *active*: it can reason, synthesize, and act within the person's domain at their standards. The company layer is the collective version of that capability.

Knowledge lives in files, not in memory. Files outlive employment. The architecture makes this explicit.

## See also
[[Memory Architecture L0-L4]] · [[BM25 Hybrid Retrieval for Graph-RAG]] · [[Claude Data Export for Graph Ingestion]] · [[OpenCode Self-Hosted LLM Configuration]] · [[Headscale Mesh VPN for Data Sovereignty]]
