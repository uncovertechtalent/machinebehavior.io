title: Compaction is the New OOM
summary: LLM context exhaustion is the operational hazard of AI-era systems.
parent: manifesto
order: 100
labels: ai-era-ops, manifesto, position
aliases: Context Exhaustion as OOM | LLM OOM
type: position
created: 2026-04-25
updated: 2026-04-25
origin: SRE/manifesto/Compaction is the New OOM.md
reviewed: no
---
> LLM context exhaustion is the operational hazard of AI-era systems. Just as physical memory pressure forced runtime engineering (paging, swap, OOM killer, cgroups), context compaction forces operational engineering. The L0-L4 memory architecture is the userspace MMU we are currently building.

## The analogy is operational, not just technical

When a process runs out of memory, the kernel kills it. The user sees a service outage. The cause is invisible from the application layer. Operations engineers learned to treat OOM as a class of incident with its own runbook: detect via dmesg, identify the offender via cgroups accounting, decide between vertical scale, horizontal scale, or memory-leak fix.

Context compaction is the same shape of problem at the LLM layer. The agent runs out of usable attention budget. The model silently degrades or restarts. The user sees a regression. The cause is invisible from the application layer. Detecting it, attributing it, and fixing it is operational work.

## Why it lands on Ops

The architecture-level mitigation (build a hierarchical memory stack: L0 conversation context, L1 task tracker, L2 persistent memory, L3 personal vault, L4 shared knowledge service) is a runtime concern. See [[Memory Architecture L0-L4]] for the canonical layer spec.

The operational concerns map cleanly onto familiar ops categories:

| Memory analogue | LLM operational concern |
|---|---|
| Page faults | Cache misses on retrieval |
| OOM killer | Compaction event |
| Swap thrashing | Repeated retrieval-rewrite cycles in long sessions |
| Memory leak | Working set growing without prune |
| GC pause | Compaction stall before next response |
| Address space layout randomization | Prompt-cache invalidation as context shifts |

Ops teams already know how to think about these. The skill set transfers. The tooling does not, yet.

## The flush mechanism is the operational primitive

Each layer in the hierarchy needs a flush trigger and a recovery path. `bd prime` reloads L1 into L0 on session restart. `/sync` flushes L0 to L1. Vault commits flush L3 changes upstream. Hivemind sync runs every 6h. These are the cron jobs and signal handlers of the new runtime.

When a flush fails, the system degrades silently. That is the new class of incident.

## What this means in practice

- Context-window monitoring is a first-class metric. Track usage curves per agent, per session.
- Compaction events should generate operational telemetry, not just user-visible response degradation.
- The L1 task tracker is operational state with its own backup and restore story.
- Vault git history is the operational audit log for L3.
- Compaction-resilience is a non-functional requirement, not a "nice to have."

## See also

[[Memory Architecture L0-L4]] · [[LLM as Software-Defined CPU]] · [[AI Agents are Ops Work]] · [[Dolt Versioned Database for Task State]] · [[Context Window Sizes and Effective Range]]
