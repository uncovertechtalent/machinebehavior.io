title: Simplicity
summary: Every line of code and every moving part is a liability, so prefer boring technology, small interfaces and deleted code. Here three static sites, standard-library Python, no third-party requests on load and one navigation source keep the platform small enough for one operator.
parent: principles-in-practice
order: 100
labels: principle, sre, simplicity, architecture
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
state: in place
source: [Google SRE book ch. 9](https://sre.google/sre-book/simplicity/); [Idempotence](doc:sre/idempotence-as-the-iac-invariant) in pillar 5
---
## The principle

Software is easier to run when there is less of it. Prefer boring, well-known technology, keep interfaces small, delete dead code and unused features, and release in small steps so each change is easy to reason about. Complexity that the problem does not need becomes load on whoever is on call.

Source: Google's [Simplicity](https://sre.google/sre-book/simplicity/). Stefan Coetzee's framework has no simplicity pillar of its own; the nearest is [Idempotence as the IaC Invariant](doc:sre/idempotence-as-the-iac-invariant) under [Infrastructure as Code](doc:sre/infrastructure-as-code): the same input gives the same end state, which keeps a system easy to reason about.

## On this platform

- **Static files.** The three sites are files on GitHub Pages. Readers depend on no server, database or application runtime that the operator runs ([Site architecture](doc:eng/site-architecture)).
- **Standard library only.** The generators are Python with no packages to install; the YAML for services and incidents is read by a strict subset reader in `scripts/mini_yaml.py` ([Service catalog](doc:eng/service-catalog)).
- **No third-party requests on page load.** Fonts are self-hosted, and no analytics or CDN script loads in a reader's browser. The map moved its d3 library and fonts from public CDNs into the repository ([ADR-0010](doc:eng/adr-0010-no-third-party-requests), superseding [ADR-0003](doc:eng/adr-0003-map-loads-from-public-cdns)).
- **One of each.** One navigation source for the chrome of every page ([ADR-0021](doc:eng/adr-0021-one-navigation-source)), one gate for three sites, one workflow, one search index ([ADR-0012](doc:eng/adr-0012-one-top-bar-and-search)).
- **Data next to the code.** Services and incidents are YAML files in the repository, read at build time; there is no database for the portal ([ADR-0013](doc:eng/adr-0013-service-catalog-from-yaml), [ADR-0014](doc:eng/adr-0014-status-page-from-published-records)).

## State

**In place.** The platform runs on few moving parts, and the decision records show where a part was removed. It carries three costs of its own: generated HTML committed next to its sources, four build commands that must run in order ([Docs tree](doc:eng/docs-tree)), and a bot commit on `main` after every gate run ([#39](https://github.com/uncovertechtalent/machinebehavior.io/issues/39)).

## Services that name it

<!-- principle-services -->

## In a company of 10 to 200 people

- Choose the managed or boring option by default, and write a decision record when you choose something new.
- Count the moving parts a customer request passes through, and remove one each quarter.
- Delete features nobody uses, with the same ceremony as shipping one.
- Keep one way to do each common thing: one pipeline, one service template, one place for docs.

## Open work

- [#39 Toil: the bot commit on main forces a rebase before every push](https://github.com/uncovertechtalent/machinebehavior.io/issues/39)
