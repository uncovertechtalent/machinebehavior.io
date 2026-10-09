title: Truth, verified, working
summary: An operational claim must be true, backed by a probe in its time window, and about a system that works. The gate, the status page and the review labels apply it here; numbers written into the docs still go stale without a probe.
parent: principles-in-practice
order: 10
labels: principle, sre, verification, receipts
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
state: partial
source: [Manifesto](doc:sre/sre-as-truth-verified-working), the substrate principle
---
## The principle

Every operational claim has three properties to meet. It is true: it matches the real state of the system, which is often different from the documented or assumed state. It is verified: a probe run by the person making the claim, in the time window of the claim, backs it. It is working: the system does what it is for, as its users meet it. The ten pillars are mechanisms that deliver these three properties, one dimension each.

Source: [SRE as Truth Verified Working](doc:sre/sre-as-truth-verified-working), the substrate principle of the [manifesto](doc:sre/manifesto). The same idea as a method: [Generate-and-Test Over Reason-From-Model](doc:sre/generate-and-test-over-reason-from-model), where the operator probes the artifact before reasoning about it. Google's book has no chapter of its own for it; its [introduction](https://sre.google/sre-book/introduction/) describes SRE as engineering applied to operations, and every chapter of Part II depends on measured state.

## On this platform

- **Verified before it serves.** Every push to the three sites runs the [conformity gate](/inside/services/conformity-gate/) before the [deploy job](/inside/services/deploy-job/). A failed check stops the deploy, and readers keep the previous build ([ADR-0002](doc:eng/adr-0002-deploy-is-gated)). Every run is recorded at [/conformity/](/conformity/) (a self-assessment, not a certification). On 2026-10-09 at 13:36 UTC the record held 69 runs since 2026-10-07: 68 passed and 1 failed.
- **State only from records.** The [status page](/inside/status/) shows the state of a service only from records the site already publishes: the gate record, the deploy feed and the incident files. A service without a record shows "no live check from this page" in place of a green light ([ADR-0014](doc:eng/adr-0014-status-page-from-published-records)).
- **Unverified is labelled.** Every page imported from the knowledge vault carries the label "not reviewed against the source" ([ADR-0009](doc:eng/adr-0009-vault-notes-with-review-label)). Each hand-written page names an owner, the date it was last checked against the system and the date of the next check, and [Docs health](/inside/docs/health/) lists the pages past that date ([ADR-0015](doc:eng/adr-0015-owner-and-review-dates)).
- **Probe the artifact.** On 2026-10-09 Prometheus reported USD 1,970,946.62 of Claude Code spend for a week whose per-request events sum to USD 1,003.45. The counters were wrong and the events were the artifact, so spend is now summed from the events ([incident record](/inside/status/#2026-10-09-phantom-spend-counters), [The phantom two million](doc:fin/anomaly-the-phantom-two-million)). The vault holds the same move as a pattern: [Probe the artifact before reasoning from counts](doc:sre/probe-the-artifact-before-reasoning-from-counts).
- **Claims with a refutation.** The research programme's [claims ledger](/claims/) lists each claim with its receipts and the observation that would refute it.

## State

**Partial.** The gate verifies every page on every push, and the status page states nothing it has no record for. Two parts are missing. Review dates are shown and listed, but nothing enforces them; a gate check for them is an open decision ([#27](https://github.com/uncovertechtalent/machinebehavior.io/issues/27)). And numbers written into the docs go stale without a probe: during this review the [on-call page](doc:obs/on-call) still counted 13 alert rules after the rule file had grown to 17. The page now matches the rule file; nothing would have caught the difference.

## Services that name it

<!-- principle-services -->

## In a company of 10 to 200 people

- Make "how do you know?" a normal question in design reviews and incident calls, and write down "not checked" when that is the answer.
- Put a check between every change and the people it reaches: CI for code, a review date for runbooks and docs, a probe behind every status claim.
- Show state only from a measurement. A status page that someone updates by hand is the first page to be wrong during an outage.
- Label what is not verified, so readers can weigh it, and generate counts from their source where you can.

## Open work

- [#27 Gate check for docs owner and review dates](https://github.com/uncovertechtalent/machinebehavior.io/issues/27)
- [#40 CI check: generated pages match their sources](https://github.com/uncovertechtalent/machinebehavior.io/issues/40)
