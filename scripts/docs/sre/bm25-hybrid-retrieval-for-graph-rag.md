title: BM25 Hybrid Retrieval for Graph-RAG
summary: BM25 is a 1990s ranking function that's still the backbone of serious retrieval.
parent: patterns
order: 100
labels: graph-rag, pattern, rag, retrieval, search
aliases: BM25 | Hybrid Retrieval | BM25 Hybrid
type: pattern
created: 2026-04-25
updated: 2026-04-25
origin: SRE/patterns/BM25 Hybrid Retrieval for Graph-RAG.md
reviewed: no
---
> BM25 is a 1990s ranking function that's still the backbone of serious retrieval. TF with diminishing returns, IDF for rare-term boost, length normalization. Fast, interpretable, no GPU. Hybrid BM25 + embeddings + cross-encoder reranker beats pure semantic for code, identifiers, and exact-match queries.

## What BM25 actually computes

Best Match 25 scores relevance by combining three signals per query term:

**Term Frequency (TF), saturated.** How often the term appears in a document, with diminishing returns. Doubling occurrences does not double the score. Controlled by `k1`, typical 1.2-2.0. Higher `k1` gives more weight to repeated matches.

**Inverse Document Frequency (IDF).** Rare terms across the corpus score higher than common ones. A query for "Kubernetes admission webhook TLS" scores mostly on the rare tokens.

**Length normalization.** Penalizes long documents that only match because they're long. Controlled by `b`, 0-1, default 0.75. `b=0` disables normalization, `b=1` applies it fully.

Total score is a sum over query terms: IDF(t) × saturated-TF(t, d) × length-factor(d).

## Where it sits

BM25 is *lexical* / sparse retrieval: it matches exact tokens. It does not understand semantics. "car" and "automobile" are unrelated to BM25. It's the default ranker in Elasticsearch, Solr, and every Lucene-based system, and it still wins benchmarks three decades after it was published.

## Why BM25 still beats pure semantic for some queries

For code, identifiers, error strings, and anything with proper nouns or acronyms, dense embeddings blur the signal. "KubernetesAdmissionWebhook" is distinctive; its embedding is close to a lot of unrelated DevOps content. BM25 treats it as a single rare token and scores high only on documents that literally contain it.

Exact-match queries, rare terms, and log-like text all favour BM25. Open-ended semantic questions favour embeddings. Production graph-RAG uses both.

## Hybrid retrieval shape

A realistic hybrid pipeline over a graph-RAG corpus:

1. **BM25 over the corpus** (e.g. Lucene index over the full vault, or the Hivemind chunk index)
2. **Dense vector search** over embeddings of the same chunks
3. **Intersect or RRF-merge** the two result sets (Reciprocal Rank Fusion gives robust combining without score calibration)
4. **Cross-encoder reranker** over the top ~100 merged results
5. **Graph expansion**: for each top chunk, follow wikilinks / frontmatter edges to pull in adjacent nodes
6. **Trim to the LLM's effective context budget** (see [[Context Window Sizes and Effective Range]])

BM25 gives precision on exact tokens. Embeddings give recall on paraphrase. The cross-encoder breaks ties with a model that actually reads both query and passage together. Graph expansion adds context the retriever didn't directly surface.

## Practical parameters

For personal vaults and technical corpora:

- `k1` around 1.2-1.5 works well; bump higher if your docs repeat key terms heavily
- `b` at 0.75 is a sane default; lower it toward 0.4 if your corpus has highly variable document lengths and you don't want to over-penalize longer notes
- Build a stopword list specific to your domain; generic English stopwords miss things like "to do", "FIXME", "lambda" that should probably be down-weighted for certain query types

## Where this shows up in the stack

L3 in the [[Memory Architecture L0-L4]] stack uses a BM25-ranked full-text index over `~/vault` via an MCP server. L4 Hivemind uses BM25 + Cohere embeddings + cross-encoder rerank over 12,125 Confluence chunks. Both are production hybrid setups, not pure semantic.

## Why the 1990s rank function still wins

Fast (no model inference on the hot path, just sparse vector dot products), interpretable (you can inspect exactly which terms scored where), no GPU required, works on laptops and on the Raspberry Pi, zero training data needed. Beating it on every query at once is hard; beating it on exact-match queries is effectively impossible without an ensemble that includes it.

## See also
[[Memory Architecture L0-L4]] · [[Context Window Sizes and Effective Range]] · [[Personal Digital Twin Architecture]] · [[Claude Data Export for Graph Ingestion]]
