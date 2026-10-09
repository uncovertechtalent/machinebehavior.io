title: Dolt Versioned Database for Task State
summary: MySQL-compatible database with Git-like versioning.
parent: tools
order: 100
labels: task-tracking, tool
type: tool
created: 2026-04-25
updated: 2026-04-25
origin: SRE/tools/Dolt Versioned Database for Task State.md
reviewed: no
---
> MySQL-compatible database with Git-like versioning. Used in the Hivemind L1 layer (Beads, `bd` CLI) on `localhost:3307` for task state and notes that survive context compaction.

## What it is

Dolt is a relational database that speaks the MySQL wire protocol and adds Git semantics on top: commits, branches, diffs, merges, blame, history. Every row change is recorded as a versioned mutation. You can query the current state via standard SQL and you can query the history via Dolt-specific functions.

## Why Beads uses it

Beads is the L1 layer of the [[Memory Architecture L0-L4]]. Its job is to hold task state and working notes in a form that survives the volatile L0 conversation context. Specifically, when L0 hits compaction, the working set has already been flushed into L1, and `bd prime` reloads it on session restart.

Dolt fits this requirement because:

- **SQL interface.** Beads can query, update, and project task state with standard SQL, no special API.
- **Versioning.** Every flush from L0 to L1 produces a commit. The history of task state is preserved without explicit snapshotting.
- **Local and cheap.** Dolt runs as a single process on localhost. No cloud dependency, no auth surface, no sync state.
- **MySQL compatibility.** Existing MySQL clients, ORMs, and tooling all work unchanged.

## Operational details

Dolt runs on `localhost:3307`. The `bd` CLI talks to it directly. The database file lives on local disk in the user's home directory. There is no replication, no high-availability, no backup unless the user explicitly snapshots the data directory.

This means Dolt is **ephemeral between machine rebuilds** unless the volume is persistent or backed up. For a personal homelab where the laptop is the L1 substrate, this is acceptable: L1 is supposed to survive sessions, not survive hardware loss. Hardware loss falls to L3 (the vault, which is git-backed and pushed to a remote).

## Where Dolt sits in the layer stack

L0 → flush via `/sync` → L1 (Dolt commit) → archived references in L2 (`/rem`, persistent memories) → enriched notes in L3 (the vault).

The flush is one-directional: L0 does not read directly from L1, it reads via `bd prime` at session start, which reloads the working set into context. During a session, Dolt is write-mostly from L0's perspective.

## Alternatives considered

**SQLite.** Lighter and simpler. Used if Git-style versioning is not required. Beads chose Dolt over SQLite because the diff and history features are operationally useful for replaying decisions across sessions.

**Plain Markdown files.** L3 territory. Too slow for high-frequency task updates, but the right shape for durable notes. Dolt and the vault are complementary, not substitutes.

**Postgres.** Overkill for personal-scale state. Heavier setup, no built-in versioning.

## See also

[[Memory Architecture L0-L4]] · [[LLM as Software-Defined CPU]] · [[Personal Digital Twin Architecture]] · [[Claude Data Export for Graph Ingestion]]
