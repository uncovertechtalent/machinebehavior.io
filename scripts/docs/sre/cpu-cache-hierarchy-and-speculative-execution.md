title: CPU Cache Hierarchy and Speculative Execution
summary: Main memory is the source of truth.
parent: observability
order: 100
labels: cpu, hardware, microarchitecture, observability, security
aliases: CPU Cache | Cache Hierarchy | Speculative Execution
type: hardware
created: 2026-04-25
updated: 2026-04-25
origin: SRE/pillars/03-observability/CPU Cache Hierarchy and Speculative Execution.md
reviewed: no
---
> Main memory is the source of truth. Caches mirror subsets of it progressively closer to the execution units. Registers are the only storage the CPU can actually compute on. Speculative execution runs ahead of permission checks, and the cache state it leaves behind is a side channel.

## The hierarchy

The cascade from authoritative storage to compute-adjacent storage:

| Level | Typical latency | Role |
|---|---|---|
| Registers | sub-cycle / 1 cycle | Only storage instructions execute against |
| L1 cache | ~4 cycles | Per-core, split I/D, ~32-64KB |
| L2 cache | ~12 cycles | Per-core, ~256KB-1MB |
| L3 cache | ~40 cycles | Shared across cores, tens of MB |
| DRAM | ~200 cycles | Authoritative store, GBs |

Each level is a subset of the one below it. A load walks up from L1; on a miss, the hardware fetches a cache line from the next level down, evicting something if needed. "Active context data" lives in DRAM; hot subsets are cached progressively closer to execution.

## Registers are compute-adjacent

Registers sit inside the execution units themselves. They're not part of the cache hierarchy, they sit above it. The CPU can only operate on data that's in a register; everything else is memory. They're referenced by name, not by address, and the count is tiny (16 general-purpose on x86-64). This is why compilers work hard on register allocation: spilling to stack memory is expensive.

Modern CPUs maintain 200-500+ *physical* registers against the 16 architectural ones visible to software. The Register Alias Table maps architectural names to physical registers dynamically, which enables out-of-order execution: multiple in-flight instructions can each "own" RAX by being assigned different physical registers.

## The Reorder Buffer

The ROB is a circular buffer holding all in-flight instructions in program order. Instructions enter in order, execute out of order, commit in order. In-order commit gives precise exceptions: if instruction 7 faults, the CPU can roll back to a clean state at instruction 6 because nothing after has committed.

Instruction windows of 200-600 in-flight instructions are normal. Speculative execution layers on top: instructions execute before the CPU knows if they should have, with the ROB holding results until speculation resolves.

## The Meltdown / Spectre side channel

The vulnerability class attacks the gap between speculative execution and commit visibility. The exploit mechanic is FLUSH+RELOAD:

1. Flush a range of memory from cache
2. Trigger speculation that loads a value dependent on a secret
3. Speculation aborts, architectural state rolls back
4. Time reads across the flushed range: warm lines reveal what the CPU touched

**Meltdown (CVE-2017-5754)** exploits Intel's late permission check. The faulting load completes speculatively before the fault fires; the cache line it warmed persists after rollback. Fix: Kernel Page Table Isolation (KPTI), stop mapping kernel memory into user-space page tables.

**Spectre (CVE-2017-5753)** trains the branch predictor to mispredict a bounds check, causing speculative out-of-bounds access. No fault required. Harder to fix because it's architectural, not an implementation bug: predictor, cache, timing are all shared. Mitigations (retpoline, IBRS, IBPB, STIBP) are partial and cost real performance, 30%+ on some workloads.

## Why this matters for observability and security

Meltdown is an Intel implementation bug. Spectre is a design tension between performance and isolation. Both reveal the same discipline: microarchitectural state (cache, TLB, execution ports, predictor tables) is *observable* even when architectural state is not. "We roll back the architectural state so it's fine" was a two-decade assumption nobody seriously challenged until 2017.

The performance counters on modern CPUs expose hundreds of microarchitectural signals: branch mispredicts, cache misses, TLB events, ROB stalls. Intended for profiling. Also the primary instrument for probing the gap between architectural spec and silicon behaviour.

## See also
[[LLM as Software-Defined CPU]] · [[Probing Microarchitecture for Vulnerability Discovery]] · [[Memory Architecture L0-L4]] · [[Apple Silicon vs Desktop GPU for Inference]]
