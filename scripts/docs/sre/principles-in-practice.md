title: Principles in practice
summary: Fourteen SRE principles, from Stefan Coetzee's framework with Google's SRE book as the reference, each tied to where this platform applies it, with its state (in place, partial or gap) and the open work.
parent: index
order: 15
labels: principles, sre, practice
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
This section ties the SRE framework of this handbook to the platform it runs on. Each page states one principle and its source, shows how the platform behind machinebehavior.io applies it with links to the live records, gives the state of that practice, and says what a company of 10 to 200 people would do with it. Each gap has an issue on the [board](/inside/board/).

Stefan Coetzee's framework comes first. His [manifesto](doc:sre/manifesto) defines SRE as a role inside Ops, with standby as its test, and puts the [substrate principle](doc:sre/sre-as-truth-verified-working) under the [ten pillars](doc:sre/pillars). Part II of Google's [Site Reliability Engineering](https://sre.google/sre-book/part-II-principles/) book is the reference the framework extends: embracing risk, service level objectives, eliminating toil, monitoring distributed systems, automation, release engineering and simplicity.

## The principles

<!-- principle-index -->

## How to read the state

| State | Meaning |
|---|---|
| in place | The platform applies the principle, and a reader can check it on a live page or record |
| partial | Some of it runs; the missing part is named on the page and on the board |
| gap | The platform does not apply it yet; the page says why and links the work |

The state is set by hand at each review, against the live pages. The build stops when the state in a page's front matter and the state in its text disagree. Each service page lists the principles it applies, under "SRE principles applied", from the `principles:` field of its [YAML file](https://github.com/uncovertechtalent/machinebehavior.io/tree/main/services); the table under The principles reads the same field.

## The platform these pages describe

One operator, Stefan Coetzee, and Claude Code sessions that write most of the code and the pages. Three static sites on GitHub Pages behind one [conformity gate](/inside/services/conformity-gate/); an [observability stack](/inside/services/observability-stack/) and a [local LLM](/inside/services/local-llm/) on a home server; a [search instance](/inside/services/searxng/) on a laptop; a small cloud proxy. Twelve services in the [catalog](/inside/services/), four incident records on the [status page](/inside/status/), the cost side in the [FinOps space](doc:fin/index). At this size some principles cost little and some do not pay yet; each page says which.

The five-minute [founder tour](/inside/tour/) walks the same evidence in six stops.
