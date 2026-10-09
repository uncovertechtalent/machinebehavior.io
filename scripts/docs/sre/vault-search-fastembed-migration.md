title: vault-search-fastembed-migration
summary: How to move a vault-search install off Ollama-based embeddings onto in-process fastembed, and how to replicate the change on another machine.
parent: runbooks
order: 100
labels: runbook, vault-search
aliases: vault-search fastembed migration | vault-search embedding runbook | vsearch fastembed
type: runbook
created: 2026-05-16
updated: 2026-06-08
origin: SRE/runbooks/vault-search-fastembed-migration.md
reviewed: no
---
# vault-search — fastembed Migration Runbook

> How to move a vault-search install off Ollama-based embeddings onto in-process `fastembed`, and how to replicate the change on another machine. Migration done on the primary Mac 2026-05-16; this runbook is for the second Mac and any future install.

## Why

vault-search (`vsearch.py`) computes embeddings for the semantic half of hybrid search. The original code called **Ollama** over the network (`OLLAMA_HOST`, default `http://localhost:11434`). On a machine with no Ollama running, every embed call fails and hybrid search **silently** degrades to keyword-only (FTS). The degradation is invisible — results still return, just without semantic matching.

The fix replaces the embedding backend with **`fastembed`**: the same model (`nomic-embed-text`, 768-dim) running as ONNX on CPU, **in-process**. No daemon, no network, nothing to be unreachable. A loud-fallback guard was added so any future embedder failure is visible (`via='fts-fallback'` on result rows + a stderr warning) rather than silent.

`nomic-embed-text` is an embedding model, not a generative LLM — it does not load a chat model into RAM and does not bog the machine. The Ollama process that historically bogged the Mac was a generative model; this is a different weight class.

## Prerequisites

- **`uv` installed.** `vsearch.py`'s shebang is `#!/usr/bin/env -S uv run --script`. `uv` reads the inline PEP-723 dependency block and installs everything — including `fastembed` and `onnxruntime` — automatically on first run. No manual `pip install`.
- **Internet, once.** First run: `uv` fetches deps; the first `embed` downloads the `nomic-ai/nomic-embed-text-v1.5` ONNX model (~a few hundred MB, cached after).
- The vault itself (the source of truth). The vault-search DB is pure regenerable cache.

## Replication — simple path

The tool is one self-contained file. If the target machine's `vsearch.py` is the same version as the migrated one:

```sh
# from the migrated machine:
scp ~/code/vault-search/vsearch.py  TARGET:~/code/vault-search/vsearch.py

# on the target machine:
cd ~/code/vault-search
./vsearch.py index            # rebuild FTS index from the vault
./vsearch.py embed --verbose  # embed all sections (fastembed, in-process)
./vsearch.py search "a conceptual query with no exact keyword match" --mode vec
```

The `vec`-mode search at the end is the verification: it must return results `via vec`. If it does, semantic search works.

## Gotchas

- **The CLI command is `index`, not `reindex`.** `reindex` errors with "No such command"; if the DB was just deleted, that leaves the index empty.
- **Vault location.** `vsearch.py` defaults `VAULT` to `~/vault` and the DB to `~/.cache/vault-search.db`. If the target vault is elsewhere, set `VAULT_PATH=/path/to/vault` as an env var for the CLI runs **and** in the MCP server config.
- **MCP server config.** If the target already runs vault-search as a stdio MCP server, no config change is needed — the new code uses no `OLLAMA_HOST`; `"env": {}` is fine. The running MCP server picks up the new code on the next Claude Code restart (stdio servers reload `vsearch.py` on respawn).
- **Latent bug on the target.** If the target's `vsearch.py` is the old Ollama version and no Ollama runs there, its semantic search has been silently degraded too. This migration fixes it.
- **First `embed` run is the slow one** (model download). Subsequent runs are fast.

## Replication — if the target's `vsearch.py` has diverged

Do not blind-copy. Apply the six changes by hand:

1. **PEP-723 deps** (the `# /// script` block): add `#   "fastembed>=0.4",`.
2. **Config constants:** drop the `OLLAMA_HOST = ...` line; set `EMBED_MODEL` default to `"nomic-ai/nomic-embed-text-v1.5"`. `EMBED_DIM` stays 768.
3. **Replace `_ollama_embed`** with two functions: `_get_embedder()` (lazy module-global `fastembed.TextEmbedding(model_name=EMBED_MODEL)`), and `_embed(text, is_query=False)` — uses `model.query_embed(text)` when `is_query` else `model.embed([text])`, returns `list[float] | None`.
4. **`_vec_rows`:** call `_embed(query, is_query=True)`; return `None` (not `[]`) when the embedder fails — `None` means "embedder down", `[]` means "genuine empty result". Update the return annotation to `list[tuple] | None`.
5. **`embed_missing`:** call `_embed("ping")` for the availability check and `_embed(text, is_query=False)` in the loop.
6. **`search()` loud-fallback:** capture `requested_mode = mode`; after `vec = _vec_rows(...)`, set `vec_degraded = vec is None`, then `if vec is None: vec = []`; if degraded and hybrid/vec requested, print a warning to stderr; compute `fts_via = "fts-fallback" if (requested_mode == "hybrid" and vec_degraded) else "fts"` and use `fts_via` for the `via` field of FTS-mode result rows.

Steps 4 and 6 together are the loud-fallback hardening; steps 1-3 and 5 are the Ollama→fastembed swap. The swap alone restores semantic search; the hardening makes future failures visible.

## Verification

```sh
./vsearch.py search "<paraphrased query, no shared keywords with target docs>" --mode vec
# expect: result rows tagged "via vec"

# forced-degradation check (confirms the loud fallback works):
VSEARCH_EMBED_MODEL="nonexistent-model-xyz" ./vsearch.py search "test" --mode hybrid
# expect: stderr warning "embedder unavailable — semantic search degraded"
#         and result rows tagged "via fts-fallback"
```

Also check DB coverage:

```sh
python3 -c "import sqlite3; c=sqlite3.connect('$HOME/.cache/vault-search.db'); \
print('sections', c.execute('select count(*) from sections_fts').fetchone()[0]); \
print('embedded', c.execute('select count(*) from section_vecs_rowids').fetchone()[0])"
# embedded should equal sections (100% coverage)
```

## Rollback

`vsearch.py` is a single file under version control / easily restored; the DB is pure cache. To roll back: restore the prior `vsearch.py`, `rm ~/.cache/vault-search.db`, run `./vsearch.py index` (and `embed` if Ollama is available again). No data is at risk — the vault is the source of truth.

## See also

[[Infrastructure Cluster]] · [[local-llm-setup]] · primary tool: `~/code/vault-search/vsearch.py`
