title: legacy-restoration-as-sre-craft
summary: A man walks you through the one and only airworthy Lockheed C-121 Constellation, 10,000 horsepower, "not a straight line on her," MacArthur's bar in the aft lounge, a veteran of the Berlin Airlift and NASA.
parent: manifesto
order: 100
labels: craft, metaphor, sre-manifesto
aliases: Legacy Restoration as SRE | Keeping the Old Machine Airworthy | Constellation SRE Metaphor | Maintenance as Craft
type: metaphor
created: 2026-08-07
updated: 2026-08-07
origin: SRE/manifesto/legacy-restoration-as-sre-craft.md
reviewed: no
---
# Legacy restoration as SRE craft

> A man walks you through the one and only airworthy Lockheed C-121 Constellation, 10,000 horsepower, "not a straight line on her," MacArthur's bar in the aft lounge, a veteran of the Berlin Airlift and NASA. Two survive worldwide. Keeping a complex legacy machine of that age actually flying, not in a museum, is the physical representation of the SRE and sysadmin ethos.

## The metaphor

The corpus's SRE stance is [[SRE as Truth Verified Working]]: the claim is only real when the system runs and you have proven it runs. Restoring and maintaining a 70-year-old four-engine airliner to airworthy condition is that stance made physical:

- **Truth is verified working.** A grounded Constellation in a museum is a claim. An airworthy one that pushes 10,000 horsepower down the runway is verified working. The whole discipline is the gap between those two.
- **Deep knowledge of a legacy system nobody else understands anymore.** The navigator climbing to the astrodome with tables and books is the pre-abstraction operator who knows the machine at the level required to keep it alive. That is the disappearing-full-stack-ops-engineer, the person who holds the whole stack in their head because the system predates the tooling that would hide it.
- **Maintenance as craft, not cost.** The airframe survives because someone chose to keep the invisible, unglamorous work funded and skilled, the same underfunded-maintenance failure mode the [[rome-infrastructure-vs-vibes-agrippa]] atom names on the civilizational scale. Restoration is the opposite choice: treat the old working system as worth the craft.

## The distinction the video draws by accident

Stefan's read: this is SRE, "or sysadmin, maybe, SREs build stuff." The seam is real. The sysadmin keeps the existing machine running; the SRE also builds the systems and automation that make running it reliable at scale. The Constellation restorer is closer to the pure-maintenance pole (keep this specific irreplaceable machine airworthy), while SRE adds the build-the-scaffolding half. Both share the core: the machine has to actually work, verified, not asserted, and that requires holding knowledge of the full stack when the abstractions that would hide it don't exist yet or have rotted away.

## See also

[[SRE as Truth Verified Working]] · [[The Disappearing Full-Stack Ops Engineer]] · [[rome-infrastructure-vs-vibes-agrippa]]
