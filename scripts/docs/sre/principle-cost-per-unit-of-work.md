title: Cost per unit of work
summary: Cost is an operational signal read per unit of output, metered like latency and alerted like errors. Here a FinOps space meters each component, prices spend per call, commit and deploy, and sets alert thresholds from data; only the AWS budget e-mail reaches a person.
parent: principles-in-practice
order: 130
labels: principle, sre, finops, cost, unit-economics
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
state: partial
source: [Pillar 9, unit economics](doc:sre/unit-economics-of-infrastructure); [FinOps Foundation framework](https://www.finops.org/framework/)
---
## The principle

Measure cost per unit of work: per request, per customer, per deploy. A rise in total spend can mean waste or growth, and the unit cost separates the two. Cost is metered with the same care as latency, alerted on like errors, and owned by the people who cause it. FinOps is the overlap of Finance and Ops in the manifesto's model, and it runs through the phases inform, optimise and operate.

Source: [Cost Optimization](doc:sre/cost-optimization) and [Unit Economics of Infrastructure](doc:sre/unit-economics-of-infrastructure); the FinOps overlap in the [manifesto](doc:sre/manifesto); the [FinOps Foundation framework](https://www.finops.org/framework/). Google's Part II covers cost only inside capacity and risk.

## On this platform

- **Every component metered or marked.** The [cost model](doc:fin/cost-model) lists each cost of the platform with its billing model and its meter, and says so where a component has none.
- **Unit costs from the meters.** Claude Code made 5,505 API calls with a list-price value of USD 1,021.01 between 2026-10-01 15:21 UTC and 2026-10-09 00:00 UTC; [Unit economics](doc:fin/unit-economics) breaks that down per day, model, call, million tokens and commit, with runner time per deploy and cost per eval run. [Showback](doc:fin/showback) sets list-price value against what is billed.
- **Thresholds from data.** The spend alert fires above USD 40 in the trailing hour, set from a week of per-request events: the earlier USD 20 threshold sat below 16 of that week's clock hours ([Budgets and alerts](doc:fin/budgets-and-alerts)).
- **An anomaly with a record.** [The phantom two million](doc:fin/anomaly-the-phantom-two-million) is the case where the meter was wrong and the spend was normal, with its [incident record](/inside/status/#2026-10-09-phantom-spend-counters).
- **Cloud spend in the stack.** An exporter reads AWS Cost Explorer and AWS Budgets, and four alert rules watch month-to-date spend and the forecast against the budget, daily spikes and a stale exporter. A [FOCUS export](doc:fin/focus-export) puts the metered costs in the FinOps Open Cost and Usage Specification format.

## State

**Partial.** Inform and optimise run on real data. Operate is weaker: of the cost alerts, only the AWS Budgets e-mail reaches a person, because no Alertmanager runs ([#36](https://github.com/uncovertechtalent/machinebehavior.io/issues/36)); the Claude Code counters behind the wrong total still land in Prometheus ([#29](https://github.com/uncovertechtalent/machinebehavior.io/issues/29)); and some costs have no meter, as the cost model lists.

## Services that name it

<!-- principle-services -->

## In a company of 10 to 200 people

- Pick one unit that matches how the business earns (per customer, per order, per seat) and report infrastructure cost per that unit each month.
- Tag every resource with an owner and a service, and show each team its own spend.
- Set budget alerts from a month of data, route them to the owning team, and review the false alarms.
- Treat a cost anomaly like an incident, with a record and a follow-up.

## Open work

- [#36 Alert routing](https://github.com/uncovertechtalent/machinebehavior.io/issues/36)
- [#29 Cost counters: drop them or alert on their resets](https://github.com/uncovertechtalent/machinebehavior.io/issues/29)
