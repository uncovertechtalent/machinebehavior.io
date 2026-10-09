title: SRE is a role inside Ops
summary: SRE is Ops with software engineering applied, the outer ring of a concentric model, with FinOps, SecOps and DevOps as overlaps. Here one operator holds every ring, agent sessions do the work, and the catalog names an owner for each service.
parent: principles-in-practice
order: 20
labels: principle, sre, ops, roles, ownership
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
state: partial
source: [Manifesto](doc:sre/manifesto), the concentric model
---
## The principle

SRE is a specialisation within Ops, the outer ring of a concentric model: system and network admins at the core, then cloud engineers, platform engineers and SRE, each ring holding the skills of the rings inside it. DevOps, FinOps, SecOps and DataOps are overlaps between Ops and another domain. An SRE team cut off from Ops ends up as a second platform team or as developers who no longer run anything.

Source: the [manifesto](doc:sre/manifesto), with the team-design side in [The Disappearing Full-Stack Ops Engineer](doc:sre/the-disappearing-full-stack-ops-engineer). Google's [introduction](https://sre.google/sre-book/introduction/) starts from the other side, with software engineers asked to design an operations function. In the manifesto, Ops comes first and the engineering is added to it.

## On this platform

- **One operator, every ring.** Stefan Coetzee owns all twelve services in the [catalog](/inside/services/). Each ring has work on the platform: the home server and its network (core), the small cloud proxy (cloud), the gate, the deploy job and the generators (platform), the SLOs, alert rules and incident records (SRE).
- **Owner and operator are separate fields.** A service can name who runs it day to day apart from who answers for it. The [conformity gate](/inside/services/conformity-gate/) names an operator, the legislation-track agent session. The [agent sessions](/inside/services/agent-sessions/) are the responders, one per track of work, under the operator ([On-call and escalation](doc:obs/on-call)).
- **The overlaps run as practice.** FinOps has its own [space](doc:fin/index) with a cost model, showback and budgets. SecOps shows in the [access model](doc:eng/access-model), the rule against third-party requests on page load ([ADR-0010](doc:eng/adr-0010-no-third-party-requests)) and the redaction step of the vault import ([Docs tree](doc:eng/docs-tree)). DevOps is the gate inside the [deploy pipeline](doc:eng/deploy-pipeline).
- **Tiers order the work.** Tier 1 first, tier 2 the same day, tier 3 in the next working session ([Service catalog](doc:eng/service-catalog)).

## State

**Partial.** The roles are named and every ring is covered, by one person. No second person can take a ring, a page or a review, so the model is visible in the work and a team does not exist yet. Two security items are blocked: security headers on the hosting decision ([#26](https://github.com/uncovertechtalent/machinebehavior.io/issues/26)) and security.txt on a contact route for vulnerability reports ([#12](https://github.com/uncovertechtalent/machinebehavior.io/issues/12)).

## Services that name it

<!-- principle-services -->

## In a company of 10 to 200 people

- Map the people you have to the rings before you hire. A company of 30 often has developers doing platform work and nobody at the core ring; that ring is missed in the first outage that needs it.
- Hire SRE into Ops, with standby in the job description, and pair each SRE with the developers of the services they run.
- Give every service an owner and, where it differs, an operator, in a catalog the build checks.
- Name FinOps and SecOps as duties of named people early. They become teams later.

## Open work

- [#26 Security headers](https://github.com/uncovertechtalent/machinebehavior.io/issues/26)
- [#12 security.txt](https://github.com/uncovertechtalent/machinebehavior.io/issues/12)
