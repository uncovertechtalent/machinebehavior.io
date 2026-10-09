title: blind-search-ratchet-minecraft-beats-itself
summary: A simulation of Minecraft with no player let random mob behaviour kill the Ender Dragon after about 1.975 billion simulated years.
parent: patterns
order: 100
labels: agents, pattern, probability, search
aliases: Minecraft Beats Itself | Blind Search Ratchet | Hitting Time Of Rare Events | Progress Retention In Search | RedLogic Simulation
type: pattern
created: 2026-10-01
updated: 2026-10-01
origin: SRE/patterns/blind-search-ratchet-minecraft-beats-itself.md
reviewed: no
---
# Blind search finishes only if progress is retained

> A simulation of Minecraft with no player let random mob behaviour kill the Ender Dragon after about 1.975 billion simulated years. It finished because each destroyed crystal stayed destroyed, so luck accumulated. Most of the time went to the last stage, a long run of independent rare hits. Take away the retention and the same random process does not finish at all.

## What was simulated

- **Method.** A Monte Carlo simulation. It does not tick the game. It samples waiting times for the rare events that could start the next step and skips the empty time between them. Mob behaviour and block interactions were modelled by the creator. A single run, and the code has not been independently verified or peer-reviewed. How ticks map to years is not stated.
- **The thought experiment.** From another YouTuber: Endermen carry carved pumpkins onto snow to make snow golems, the golems' snowballs provoke Creepers, Creeper blasts open routes, and golem snowballs and Creeper explosions destroy the End crystals and hurt the dragon.
- **A precondition the TikTok drops.** The seed starts with a completed twelve-eye End portal buried beneath an ice-spikes biome, because mobs cannot reach the End unless a player placed the eyes. So the run answers "given a finished portal, can the mobs finish the game", not "can Minecraft beat itself from nothing". Stefan's question about how long success took belongs to the first, narrower claim.

## The timeline

| Milestone | Simulated years | Gap from the last |
|---|---|---|
| First pumpkin moved | about 33,500 to 34,800, the two articles differ by a digit | start |
| Route to the portal opened | a few thousand years later | thousands |
| First crystal destroyed | nearly 3 million | millions |
| Ninth crystal destroyed | about 181 million | about 180 million |
| Tenth and last crystal | about 18 million after the ninth, so about 200 million | 18 million |
| First damage to the dragon, 4 points, about 2% | about 250 million, 28 million after the last crystal | 28 million |
| Dragon at 3 health | after almost 2 billion | about 1.7 billion |
| Dragon dead | about 1.975 billion | |

The gaps grow by roughly a factor of a hundred at each stage: thousands of years, then millions, then hundreds of millions, then billions.

## The structure that matters

1. **Progress is a ratchet.** A destroyed crystal stays destroyed. Once the last one is gone the dragon can no longer heal, so every explosion that hits it counts permanently. Before that point its regeneration would undo any damage, and the chance of dealing the whole health bar between one regeneration and the next is effectively zero. The ratchet turns a process that never finishes into one that finishes in a long, predictable time.
2. **Retained progress adds, lost progress multiplies.** Where progress is kept, expected total time is the sum of the stage times, here about 2 billion years. Where a failure resets the run, the time grows like the product of the per-stage odds. That is the gap between 2 billion years and never.
3. **The last stage dominates.** About 1.7 billion of the 1.975 billion years, roughly 90%, went to the dragon's damage stage. The portal stage is under 0.01% of the total.
4. **Many small events are predictable, one big event is not.** A waiting time for a single rare event has a spread as wide as its mean. A stage made of many independent rare hits averages out, with relative spread about one over the square root of the hit count. If each hit did about the 4 points of the first one, that is roughly 50 hits and a spread near 14%, my estimate. So the dragon stage is fairly predictable once healing stops, and the early single-event stages are not. A single run cannot say what the typical total would be.
5. **There is a deadline.** The chain needs pumpkins, and the creator says the supply is finite, so the run is a race between completion and resource exhaustion. His other end state is a heat-death equilibrium where movable blocks are spread evenly and nothing more can change. With a different draw the world could have gone quiet first.
6. **Looks hopeless, is on schedule.** At 250 million years the dragon had lost 2%, about 13% of the way through the elapsed time. A hit rate that looks hopeless early is the steady rate, and the remaining time is the remaining hits times the gap between them.

## Why it is here

It is the cleanest small example of the point behind [[Generate-and-Test Over Reason-From-Model]]: blind generation works when a test locks in what it finds. For agent operations the mapping, mine and not the creator's, is that a long task finishes in the sum of its stage times only if progress survives between attempts. Checkpointed state is the ratchet. A loop that loses its progress at every restart, or a context that forgets what was done, is the version that never finishes. That is the compaction question in its simplest form: what must cross the boundary so that earlier luck is not thrown away. See [[self-generated-prompt-injection-in-compaction-summaries]] for the summary acting as the carried state.

## See also

[[Generate-and-Test Over Reason-From-Model]] · [[Compaction is the New OOM]] · [[self-generated-prompt-injection-in-compaction-summaries]] · [[LLM as Software-Defined CPU]]
