title: The Disappearing Full-Stack Ops Engineer
summary: The concentric Ops model produces engineers at every ring (SysAdmin, Cloud, Platform, SRE).
parent: manifesto
order: 100
labels: manifesto, position, team-design
aliases: Full-Stack Ops Rarity | T-Shaped Ops
type: position
created: 2026-04-25
updated: 2026-04-25
origin: SRE/manifesto/The Disappearing Full-Stack Ops Engineer.md
reviewed: no
---
> The concentric Ops model produces engineers at every ring (SysAdmin, Cloud, Platform, SRE). The engineer who actually holds all four rings simultaneously is the highest-leverage person on most teams and also one of the rarest. Designing teams as if you have one available is a planning error.

## Why the full-stack ops engineer is endangered

Each ring of the concentric model has matured into a specialty career path with its own certifications, conference circuit, and salary band. A network engineer who can also write Terraform and trace through Kubernetes networking is doing three jobs that hire separately.

Three forces compress the population:

1. **Cloud abstraction.** Modern engineers learn cloud primitives without ever managing physical hardware. The instinct for "which layer is broken" weakens when the lower layers were always abstracted.
2. **Hiring filters.** Job posts ask for either deep specialty or broad generalism, rarely both. Both extremes pay better than the middle for most candidates.
3. **Tooling fragmentation.** The number of tools per layer has grown faster than any single engineer can track. Specialization is the rational response to information density.

The result: a 200-person engineering org typically has zero or one engineer who can debug from "the customer can't load the page" through DNS, CDN, load balancer, container runtime, application code, database query plan, kernel network stack, and back. That person is usually overloaded and underpaid.

## What this means for team design

Most ops teams cannot operate on the assumption that someone in the rotation can hold the whole stack. Three implementation patterns work:

### Pattern 1: Pair the rings explicitly

When a sysadmin and a platform engineer are both on the incident bridge, the sysadmin probes lower layers while the platform engineer probes upper layers. They explicitly cover for each other's blind spots. The pairing is the redundancy.

### Pattern 2: Document the layer transitions

Most cross-ring debugging fails at the boundary (the cloud network layer, the container-to-host layer, the application-to-database layer). Runbooks that include explicit layer-handoff probes ("if you are seeing X, ask the cloud-engineer rotation; if you are seeing Y, ask the database-engineer rotation") replace the missing generalist.

### Pattern 3: Compound the rare individual

If you have a full-stack ops engineer, the question is not "what should they work on?" but "how do we amplify their pattern recognition?" They should be writing runbooks, not running them. They should be designing the alert taxonomy, not paging through it. Their leverage is in the asymmetry, not the labor.

## The hiring filter

When evaluating someone who claims breadth, the test is layer-transition fluency: can they explain why a TLS handshake failure looks like a 500 to the application, looks like a connection timeout to the LB, looks like nothing on the host metric dashboard? That is the diagnostic that filters the real generalists from the resume-padded ones.

## See also

[[README]] (manifesto) · [[AI Agents are Ops Work]] · [[Enabler Role Framing for Leadership Transitions]] · [[Body Language Literacy for Leaders]]
