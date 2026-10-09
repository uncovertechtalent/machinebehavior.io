title: Context Window Sizes and Effective Range
summary: Advertised context windows are marketing.
parent: patterns
order: 100
labels: context, llm, pattern, retrieval
aliases: Context Window | Effective Context | Context Window Sizes
type: pattern
created: 2026-04-25
updated: 2026-04-25
origin: SRE/patterns/Context Window Sizes and Effective Range.md
reviewed: no
---
> Advertised context windows are marketing. Effective context is typically 50-65% of the advertised figure per RULER benchmarks, with a 30%+ accuracy drop for content in the middle. Claude Sonnet 4.6 is the outlier for consistency. Retrieval-first architectures beat raw context stuffing on nearly every benchmark that matters.

## Advertised vs effective

State of play as of early 2026:

| Model | Advertised | Effective (approximate) |
|---|---|---|
| Magic LTM-2-Mini | 100M | unclear, experimental |
| Llama 4 Scout | 10M | degrades sharply past ~1M |
| Gemini 3 Pro / Grok 4 | 2M | ~1-1.3M |
| GPT-4.1 / GPT-5.x | 1M | ~500-650K |
| Claude Sonnet 4.6 | 200K standard / 1M beta | near-full at 200K, degrades past that |
| DeepSeek R1/V3 | 164K | ~100K |
| Llama 3.1 | 128K | ~80K |
| GPT-4o | 128K | ~80K |

Effective context is measured by RULER-class benchmarks: needle-in-haystack plus multi-hop reasoning across distances. Almost all models degrade well before their advertised limit.

## Lost in the middle

Content positioned mid-context suffers 30%+ accuracy drops compared to content at the start or end of the window. The model attends disproportionately to the beginning (the system prompt, the early user turn) and the end (the most recent turn). Anything buried in between gets deprioritized, even when it's the exact information needed.

Design implication: put the most important content at the top or the bottom of the context, never the middle.

## Claude Sonnet 4.6 is the outlier

Less than 5% accuracy degradation across the full 200K range. It's not the biggest window, it's the most consistent one. For workflows where you actually fill the window (long code reviews, multi-document synthesis, extended agentic sessions), consistency beats raw size.

## Cost cliffs

Some providers price-hike past a threshold. Gemini 3 Pro charges 2x for prompts over 200K. For high-throughput production use, the practical ceiling is usually around 100-200K before the cost curve bends sharply against you.

## Retrieval-first beats stuffing

For most production use cases, the practical ceiling is 100-200K. Bigger windows deliver diminishing returns and increasing costs beyond that. A retrieval-first architecture with BM25 plus embeddings plus a reranker (see [[BM25 Hybrid Retrieval for Graph-RAG]]) surfaces the 5-20 chunks that actually matter, rather than dumping 500K tokens of context into the model and hoping attention finds the needle.

Graph-RAG over a curated vault with typed entity links beats raw stuffing for two reasons: the retriever already filters by relevance, and the graph structure surfaces adjacent context that a flat retriever would miss.

## Implications for agent design

- Treat the context window as an expensive, degrading resource, not a free scratchpad
- Place system prompts and durable instructions at the top, latest user turn at the bottom
- Externalize durable state into [[Memory Architecture L0-L4]] layers rather than letting context grow
- Flush volatile state with `/sync` before compaction hits; see [[LLM as Software-Defined CPU]]
- When designing retrieval, target <50% window fill to stay in the effective range
- For long sessions, periodic summarization into L1 or L2 is better than hoping the model keeps tracking

## Why compaction is fundamental

Every context window has a hard limit. Compaction is silent, total erasure when the limit hits. This is not a bug to work around, it's the constraint that drives the whole durable-memory architecture. The effective range degradation makes it worse: by the time the window is 80% full, accuracy has already dropped noticeably. Aggressive externalization is the cheapest insurance.

## See also
[[Memory Architecture L0-L4]] · [[LLM as Software-Defined CPU]] · [[BM25 Hybrid Retrieval for Graph-RAG]] · [[OpenCode Self-Hosted LLM Configuration]] · [[Personal Digital Twin Architecture]]
