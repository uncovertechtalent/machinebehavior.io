title: Generate-and-Test Over Reason-From-Model
summary: When a system has enough internal constraint, reasoning about which change should work reliably loses to generating many changes and testing which ones do.
parent: manifesto
order: 100
labels: position, sre-manifesto
aliases: Generate-and-Test Over Reason-From-Model | Bottom-Up Beats Rational Design | Probe the Artifact Not the Model | Empirical Search Over Component Optimization
created: 2026-08-08
updated: 2026-08-12
origin: SRE/manifesto/Generate-and-Test Over Reason-From-Model.md
reviewed: no
---
> When a system has enough internal constraint, reasoning about which change *should* work reliably loses to generating many changes and testing which ones *do*. The AI-phage result is the cleanest recent demonstration.

Second reading of the same source as [[AI-Generated Phage Genomes and Systems-Level Design]]. That atom is about what was built; this one is about how, because the method is the transferable part.

## What actually happened, read as method

Researchers wanted to swap a DNA packaging protein into ΦX174 from a distantly related phage. They had **tried this deliberately, by rational design, and it did not work**. They understood the components, reasoned about what should substitute for what, and were wrong.

The approach that worked contained no such reasoning. Fine-tune a model on 14,466 related genomes, generate candidates in bulk, filter computationally, then physically build and test what survives.

The funnel is the argument, so keep the numbers: **700,000 generated → 302 through the filters → 285 built → 16 viable**. That is a 0.002% hit rate from generation, and roughly 5% from the set actually built. One of those sixteen contained the swap that rational design had failed to produce.

Two things follow from the shape of that funnel. The generation step has to be nearly free, or the ratio is unaffordable. And the filter between 700,000 and 302 is doing enormous work, so this is not blind search; it is cheap generation plus cheap screening, with the expensive wet-lab step reserved for a set small enough to exhaust.

Nobody predicted it. Nothing in the process explained why the shorter protein would work. Cryo-electron microscopy came **afterwards** and showed it sitting at a different orientation in the capsid, which is the explanation the method never needed and did not supply.

## Why reason-from-model loses here

ΦX174's genes overlap: the same stretch of DNA encodes parts of multiple proteins. Change one letter to improve one thing and something else silently breaks. That is a system where every component sits inside constraints imposed by every other component.

Component-wise reasoning optimizes the part and breaks the context, because the mental model holds the part clearly and the context approximately. Whole-artifact generation does not have that failure mode: each candidate is evaluated as a whole thing that either lives or dies, so satisfying all constraints at once is the only way to score.

The general form: **the more the constraints interact, the worse a model of the parts predicts the behaviour of the whole, and the better brute empiricism does.**

## The stronger result: the answer was not in the candidate set

Against E. coli lines that had evolved resistance, none of the original 16 designs won. The phages that broke through were **mosaic recombinants**, genomes formed by recombination between multiple AI designs, and they cleared resistance in 1 to 5 passages.

So the winning solution existed in no individual design and in nobody's head. It came out of letting a population of tested artifacts interact under selection pressure.

This is the part with the most operational carry. Generating candidates is only half the method; the other half is putting them in contact with each other and with the real adversary, then reading what survives.

## The local doctrine this instantiates

Same substrate as [[SRE as Truth Verified Working]]: a claim is worth what its probe is worth, and a probe beats a model of the system every time. Restated as method rather than as verification:

- **Probe the artifact, do not reason from the model of the artifact.** One real fetch settles what a week of inference from counts cannot.
- **Cheap tests at volume beat expensive reasoning at low volume**, whenever the tests are genuinely cheap and the constraints genuinely interact.
- **Understanding is not a prerequisite for a correct result, and a correct result does not confer understanding.** Both directions matter. The swap worked without being understood; understanding it required a separate instrument afterwards. Do not withhold action pending a model, and do not claim a model because the action worked.
- **Do not discard the failed candidates.** 286 of 302 were not viable, and the population they belonged to is what produced the recombinants that won.

## Worked example, same day, opposite outcome

This session produced a live instance of the failure mode. A scrape reported 46 videos where the collection held 48. Rather than probing the boring explanation, I reasoned from a model (publish date implies time-in-collection), concluded the enumeration was defective, and filed a bug. The actual cause was that Stefan was saving videos while the scrape ran. One question would have settled it; a model produced a confident wrong answer instead.

Recorded in `~/.claude/skills/bulk/_handover.md` under trap 4. The method atom and the counterexample were generated within an hour of each other, which is the useful part.

## See also

[[SRE as Truth Verified Working]] · [[AI-Generated Phage Genomes and Systems-Level Design]] · [[Protein Folding - Sequence to Native Fold]] · [[process-engineering-before-agentic-automation]] · [[Objections and Falsification Register]]
