title: SRE as Truth Verified Working
summary: The acronym is incidental.
parent: manifesto
order: 100
labels: position, sre-manifesto
aliases: SRE as Truth Verified Working | The SRE Substrate Principle | Truth Verified Working
created: 2026-06-08
updated: 2026-06-08
origin: SRE/manifesto/SRE as Truth Verified Working.md
reviewed: no
---
# SRE as Truth, Verified, Working

> The acronym is incidental. The discipline is about three properties: claims are **true**, claims are **verified**, the system is **working**. The ten pillars are downstream mechanisms; this is the substrate.

## The principle

SRE discipline is a position on three properties of any operational claim:

1. **True** — the claim corresponds to the real state of the system. Not the assumed state, not the documented state, not the state someone said yesterday.
2. **Verified** — the truth-claim is backed by a probe run by the operator making the claim, in the time window of the claim. Not by memory, not by intuition, not by deferred trust.
3. **Working** — the system performs its intended function. Documented-but-broken is not working. Configured-but-untested is not verified. The working property is the one the user experiences.

A claim fails the discipline when any of the three is missing:
- True but unverified: "I'm pretty sure X is set up" — possibly correct, no receipt.
- Verified but stale: "I tested X last month" — the probe is outside the validity window.
- Working but undocumented: "It works on my machine" — non-reproducible, doesn't survive operator change.

## Why this is upstream of the pillars

The ten pillars (Reliability, Scalability, Observability, Incident Management, IaC, CI/CD, Performance, Security, Cost Optimization, Toil Reduction) are each a mechanism for delivering truth + verified + working in one dimension:

- **Reliability** = working under load + verified by SLO measurement
- **Observability** = the apparatus for converting system state into verified truth-claims
- **Incident Management** = restoring working state + producing verified postmortems
- **IaC** = the system's truth-claim about itself is the code that built it
- **CI/CD** = every change passes verification before it ships
- **Security** = the working-property survives adversarial pressure
- **Cost Optimization** = working-per-spend is itself a verified property
- **Toil Reduction** = the verification work is automated; the operator's attention goes to non-routine truth-claims

Pillars 02 (Scalability) and 07 (Performance) are reliability extended into capacity and latency dimensions. Same substrate.

## Worked examples in this vault

The principle shows up structurally across the corpus:

- **`[probed]` / `[user]` / `[vault]` / `[unknown]` tagging** in [[work-kb/infrastructure/home-network-topology|home-network-topology]] — every claim in the atom carries its verification source inline. The `[unknown]` tag is the structural escape valve: when verification is absent, the absence is named, not hidden. This is the discipline written into a runbook.
- **Receipts Standard** (`~/.claude/projects/-Users-stefancoetzee/memory/feedback_receipts_standard.md`, memory not vault) — the LLM-substrate application. "Probe before assert. Receipts not vibes. Memory is a hint, not a fact. Unverified gets labelled unverified." Same three properties: truth + verified (in this session) + working.
- **Three-Layer Position Model** ([[pillars/developmental-position/Three-Layer Position Model|substrate / apparent / assigned]]) — the people-substrate application. Most human-system observation lives on the apparent layer, never reaches substrate. The discipline of distinguishing the three IS the truth + verified work applied to human substrate.
- **Interview probing technique** ([[diving-deep-follow-up-questions|Module 06]]'s peel-the-onion sequence) — the structured probe that takes a candidate's rehearsed apparent-claim and either verifies it against substrate or names the verification gap.

## Failure mode the principle is designed against

Treating "I haven't checked" as equivalent to "I don't have access" or "it's not there". The 2026-05-15 case (recorded in the Receipts Standard atom): the LLM claimed no access to `[host]` and to AWS credentials, twice in one session, without running the 5-second probe. Both turned out to be full access. Pattern: the *absence of a probe* was treated as the *absence of access*. That conflation is the substrate failure mode.

A second case from the same session this atom was drafted in (2026-05-25): the LLM wrote three operations in parallel — patch MOC A, patch MOC B, create the target atom. MOC patches were verified to have landed; the atom-create rejected on a parameter-schema mismatch (`file_path` vs `path` across two different write tools). Result: both MOCs pointed at a non-existent file for the round-trip. Same failure shape: an unverified assumption about a dependency, parallelised in a way that hid the dependency.

The same pattern at human-substrate scale: a manager who reads a quiet report as "they're fine" rather than "I haven't probed". A debrief that concludes "no concerns" without anyone naming what would constitute a concern. A psychological-safety dimension where the team has stopped speaking up and the leader hasn't noticed because there's no probe in place.

## Structural controls

The principle is degradation-resistant only when load-bearing controls exist:

1. **Probe before assert** — every claim runs a probe at claim-time, not at recall-time.
2. **Snapshot before change** — current state is captured before any modification, so the verification window is well-defined.
3. **Receipts in the claim** — verification source named inline (`[probed]`, `[user]`, etc.), not in a footnote.
4. **Unverified gets labelled unverified** — absence-of-verification is named in-line, never silently dropped.
5. **External scrutiny** — base-rate checks and peer review, because the operator's own filter degrades under extraction pressure.
6. **Sequencing across dependencies** — when operation B references operation A, do not parallelise. Verify A landed, then run B. The 2026-05-25 MOC-dangling case was a sequencing failure dressed up as a parameter mistake.
7. **Probe the toolspace before defaulting to the familiar tool** — listing the available commands / inspecting parameter schemas costs one cheap probe; defaulting to the tool already in muscle memory skips that probe and is the same act-before-probe failure as items 1 and 4 applied to tools rather than claims. The 2026-05-31 vault-wikilink-rewrite case is the worked example: defaulted to sed for a bulk wikilink rewrite without first running `command_list` on the Obsidian REST API to see what link-aware operations existed. No single Obsidian-native command would have replaced sed for the multi-target case, but the probe would have surfaced `find-unresolved-link` (which would have found the dangling refs upstream of grep), `find-empty-files` (which would have forced the cleanup pre-step), and `obsidian-git:commit` (snapshot-before-change at vault granularity). The failure was not the tool choice; it was acting before checking.

## See also

- [[README|SRE Manifesto MOC]] — the role-shape + concentric model
- [[AI Agents are Ops Work]] — the same discipline applied to the agent layer
- [[Compaction is the New OOM]] — context-exhaustion as a degradation mode for the truth + verified properties
- [[pillars/psychology/Psychology Cluster|Psychology cluster]] — people-substrate corpus, where probe-vs-assume is documented as `[real-emotional-maturity vs the performance of it]`
- [[pillars/developmental-position/_moc|Developmental Position and Distortion]] — substrate / apparent / assigned is the typology this principle reads off
- [[work-kb/internal/interview-training-psychology-parallels|Interview Training as Applied Clinical Psychology]] — the discipline applied to hiring
- [[work-kb/infrastructure/home-network-topology|home-network-topology]] — the discipline applied to the home LAN
- [[../Home|SRE Framework MOC]] — pillar index; each pillar is a downstream mechanism
