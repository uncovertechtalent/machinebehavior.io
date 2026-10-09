title: LLM as Software-Defined CPU
summary: An LLM is a CPU that shipped without a memory management unit.
parent: patterns
order: 100
labels: ai-agents, architecture, computer-history, pattern
aliases: LLM-as-SDCPU | Software Defined CPU | SDCPU
type: pattern
created: 2026-04-25
updated: 2026-04-25
origin: SRE/patterns/LLM as Software-Defined CPU.md
reviewed: no
---
> An LLM is a CPU that shipped without a memory management unit. The agent stack is the operating system we build around it in userspace: context is RAM, attention heads are registers, tokens are instructions, compaction is cold boot, beads is swap.

## The mapping

| Silicon concept | Agent stack equivalent |
|---|---|
| CPU | LLM (execution engine) |
| Registers | Attention heads |
| Instructions | Tokens |
| L1/L2/L3 cache | Recent context window tokens |
| RAM | Full context window |
| Extended memory manager | Beads (HIMEM.SYS) |
| Swap / paging | `bd` paging tasks to Dolt |
| fsync() | `/sync` |
| Bootloader / AUTOEXEC.BAT | `bd prime` |
| CONFIG.SYS | `AGENTS.md` |
| TSRs | `bd remember` entries |
| Registry + pagefile | L2 persistent memories |
| Personal filesystem | L3 vault at `~/vault` |
| NAS mount | L4 Hivemind |
| OOM killer | Compaction |
| Cold boot | Compaction event, state lost |

## The 640K parallel

640K of RAM was "enough for anybody" until it wasn't. 200K tokens is the new 640K. You will fill it. You will hit the wall. When you do, compaction fires and the process dies cold. Everything not written to durable storage is gone.

Industry solved the 640K problem with HIMEM.SYS and EMS/XMS: drivers that paged extended memory in and out of the working set. Beads plays that role for the LLM. When context cannot hold the working set, `bd` pages it to Dolt on localhost (SSD with a MySQL wire protocol). On restart, `bd prime` runs like AUTOEXEC.BAT, pulls active tasks back, reestablishes state.

## The MMU gap

Silicon CPUs have MMUs, TLBs, page tables, and cache coherence baked into hardware. Intel solved this in 1985. The LLM has none of it. It is a CPU with no memory controller.

So the memory controller gets built in userspace, one shell script at a time. Every primitive the stack adds (swap, paging, persistence, shared memory, process tables) is something silicon solved in hardware decades ago. We are reimplementing it in Python and markdown because the compute substrate changed.

## Why the metaphor holds

Speed decreases and durability increases as you move down the stack, exactly matching silicon's register-to-HDD pyramid. Registers → L1 cache → L2 → L3 → RAM → SSD → HDD → network maps cleanly onto attention → recent tokens → full context → beads → memories → vault → Hivemind.

The volatile layer (context, RAM) is fast but expendable. The durable layers (filesystem, NAS) are slow but survive power cycles. The engineer's job is the same job OS authors had in 1985: build habits and APIs that move information from volatile to durable storage before the power goes out.

## The punchline

AssemblyLine is an operating system for a CPU that forgot to ship with one. The 640K barrier taught the industry to build memory managers. We just learned the same lesson with tokens.

## See also
[[Memory Architecture L0-L4]] · [[CPU Cache Hierarchy and Speculative Execution]] · [[Dolt Versioned Database for Task State]] · [[Context Window Sizes and Effective Range]] · [[Probing Microarchitecture for Vulnerability Discovery]]
