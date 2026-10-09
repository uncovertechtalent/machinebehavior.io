title: Graph-RAG over Flat RAG for Operational Knowledge
summary: Operational knowledge is structurally relational: an incident references a service references a deployment references a runbook references a metric references an SLO.
parent: manifesto
order: 100
labels: manifesto, position, retrieval-architecture
aliases: Why Graph-RAG for Ops | Graph Retrieval for SRE
type: position
created: 2026-04-25
updated: 2026-04-25
origin: SRE/manifesto/Graph-RAG over Flat RAG for Operational Knowledge.md
reviewed: no
---
> Operational knowledge is structurally relational: an incident references a service references a deployment references a runbook references a metric references an SLO. Flat RAG flattens this graph and loses the relationships. For agents that operate on operational knowledge, the structure is the signal.

## The shape of operational knowledge

A production incident is never standalone. It points at a service, which has a deployment history, which has owners, which has runbooks, which has dependent services, which have their own SLOs and on-call rotations. The graph of operational entities is dense, typed, and asymmetric.

Compare to a flat-RAG document store: a postmortem becomes a chunk, the runbook becomes a chunk, the service-overview becomes a chunk. They co-occur in retrieval only when the query phrasing accidentally matches all three. The structural relationship (this postmortem is the historical context for that runbook on that service) is lost.

## What graph-RAG preserves

When operational knowledge is encoded as a graph (markdown atoms with frontmatter typing plus wikilink edges), retrieval can:

- Traverse relationships, not just match strings
- Surface the runbook AND its parent pillar AND the service that uses it
- Find dependency chains (this service → this database → this index → this query pattern)
- Filter by entity type (only show me runbooks for incident category X)
- Compose queries (give me all SLO-impact postmortems from Q3 that mention payment)

Flat RAG can do none of these without scoring tricks that approximate the missing graph.

## The vault is the substrate

L3 of the [[Memory Architecture L0-L4]] is a markdown graph. Each atom is a node. Wikilinks are typed by frontmatter. Filenames resolve to entities. This is intentional graph encoding, not a document corpus.

When the agent queries the vault, the retrieval pipeline does:

1. BM25 keyword match for entry points
2. Embedding similarity for semantic neighbors  
3. **Graph expansion** along wikilink edges from the entry-point candidates
4. Cross-encoder rerank over the expanded set
5. Return the top-K with their structural context attached

Without step 3, you have flat RAG dressed up. With step 3, you have something agents can actually reason over.

## Practical consequence

This is why the vault uses:

- Atomic notes (one entity per file)
- Frontmatter typing (`type: pattern`, `type: incident`, `type: service`)
- Explicit `## See also` sections (the explicit graph is more reliable than inferred semantic edges)
- Filename-as-canonical-id (Obsidian wikilink resolution as cheap entity disambiguation)
- MOC files per subdir (entry-point hubs)

Every choice is a graph-construction choice. Skip them and you regress to flat RAG.

## See also

[[Memory Architecture L0-L4]] · [[Personal Digital Twin Architecture]] · [[BM25 Hybrid Retrieval for Graph-RAG]] · [[Claude Data Export for Graph Ingestion]] · [[AI Agents are Ops Work]]
