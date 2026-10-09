title: Claude Data Export for Graph Ingestion
summary: Pipeline for pulling Claude conversation history into a graph-RAG vault.
parent: patterns
order: 100
labels: claude, graph-rag, ingestion, pattern, vault
aliases: Claude Data Export | Chat Export Pipeline
type: pattern
created: 2026-04-25
updated: 2026-04-25
origin: SRE/patterns/Claude Data Export for Graph Ingestion.md
reviewed: no
---
> Pipeline for pulling Claude conversation history into a graph-RAG vault. Request export via Settings > Privacy > Export Data, receive emailed JSON link, parse and filter, transform to markdown with frontmatter, then enrich with entity extraction and wikilink resolution.

## The export mechanism

Settings > Privacy > Export Data, web or Claude Desktop only (not mobile). Anthropic emails a download link valid ~24 hours. The ZIP contains JSON with full conversation history: messages, metadata, timestamps, attachments, tool calls.

All-or-nothing, no partial selection. The format is machine-parseable but not human-friendly; you transform it into your vault's markdown+frontmatter shape yourself.

Typical contents:
- `conversations.json`: array of conversation objects
- `users.json`: account metadata

Each conversation has a `uuid`, `name`, `created_at`, `updated_at`, and a `chat_messages` array with `sender`, `text`, `created_at`, and sometimes attachments. Exact schema shifts between export versions, so inspect one record before coding against it.

## Why in-session tools are the wrong mechanism for bulk

`conversation_search` and `recent_chats` return snippets, not transcripts. They paginate slowly (~20 results per call, ~5 call soft limit), and are built for runtime retrieval during active chats. Fine for "pull anything relevant to X" mid-session. Useless for systematic extraction of years of history.

## Pipeline shape

```
claude-export.zip (JSON)
  -> parse: conversations[].messages[]
  -> filter: drop trivial chats, empty sessions
  -> chunk: message pairs or topic-bounded turns
  -> extract: entities, decisions, code artifacts, links
  -> transform: markdown + frontmatter
     (tags, date, conv_id, participants, topic cluster)
  -> crosslink: wikilinks to existing vault nodes
  -> embed: your existing embedding pipeline
```

## Parser skeleton (Python)

```python
import json, pathlib, re

RAW = pathlib.Path("conversations.json")
OUT = pathlib.Path("vault/claude-chats")
OUT.mkdir(parents=True, exist_ok=True)

def slug(s, n=60):
    s = re.sub(r"[^\w\s-]", "", s or "untitled").strip().lower()
    return re.sub(r"[\s-]+", "-", s)[:n]

def frontmatter(meta):
    lines = ["---"]
    for k, v in meta.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---\n")
    return "\n".join(lines)

data = json.loads(RAW.read_text())
for conv in data:
    title = conv.get("name") or "untitled"
    created = conv.get("created_at", "")
    date = created[:10] if created else "unknown"
    meta = {
        "source": "claude-export",
        "conversation_id": conv.get("uuid", ""),
        "title": title,
        "created": created,
        "tags": ["claude-chat"],
    }
    body = [frontmatter(meta), f"# {title}\n"]
    for msg in conv.get("chat_messages", []):
        role = msg.get("sender", "unknown")
        text = msg.get("text") or ""
        ts = msg.get("created_at", "")
        body.append(f"\n## {role} [{ts}]\n\n{text}\n")
    fname = f"{date}-{slug(title)}.md"
    (OUT / fname).write_text("\n".join(body))
```

## Filter heuristics

Before ingestion, drop noise:

- Conversations with <4 messages (mostly failed starts)
- Conversations where total user text is <200 chars
- Conversations tagged as ephemeral tests or duplicates

Flag for special handling:

- Conversations containing code blocks (chunk differently, preserve fences)
- Conversations with attachments (link to asset store, don't inline)
- Project-scoped chats (preserve project metadata as a tag)

## Graph enrichment (second stage)

Run as a separate job so extraction logic iterates without re-parsing the raw export:

1. **Entity extraction.** Pass each chat through the local inference stack (e.g. Mac Studio M4 Max or a 7500F CPU node, see [[Apple Silicon vs Desktop GPU for Inference]]). Pull people, tools, projects, decisions. Prompt shape: "List every named entity with type and a one-sentence description."
2. **Entity resolution.** Match extracted entities against existing vault nodes by basename. Add `[[Wikilinks]]` where matches exist; surface unmatched entities as candidates for new atoms.
3. **Topic clustering.** Run embeddings over conversations, cluster with HDBSCAN or k-means, assign each conversation to one or more parent topic MOC nodes.
4. **Decision extraction.** Separate pass: prompt the model to find "decisions made, deferred, or reversed" and emit as structured items with backlinks to the source conversation.

## Granularity decision: one node per conversation, or per turn cluster

For graph-RAG, turn-cluster splitting gives better retrieval granularity but explodes node count. With a frontmatter-crosslink vault pattern, one file per conversation with internal headers for turn clusters is the cleaner starting point. Re-chunk at embed time using heading boundaries as chunk delimiters. See [[BM25 Hybrid Retrieval for Graph-RAG]].

## Caveats

- Deleted chats are gone from the export. Stop deleting going forward if history matters.
- Incognito chats are never recorded and never exported.
- Project-scoped chats are included but segregated in the export. Preserve that metadata as frontmatter `project:` field.
- Tool call payloads can be huge; truncate or hash them before writing if size matters.

## See also
[[Memory Architecture L0-L4]] · [[BM25 Hybrid Retrieval for Graph-RAG]] · [[Personal Digital Twin Architecture]] · [[Context Window Sizes and Effective Range]]
