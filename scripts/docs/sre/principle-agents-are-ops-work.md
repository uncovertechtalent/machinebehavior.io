title: Agents in production are ops work
summary: An AI agent in production is a service and needs what services need: owners, SLOs, paging, runbooks, cost control and canaries. Here the agent sessions are a catalogued service that pushes through the same gate, with metered spend and an incident record; they have no SLOs and no canary set.
parent: principles-in-practice
order: 140
labels: principle, sre, ai-agents, llm, ai-era
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
state: partial
source: [Manifesto](doc:sre/ai-agents-are-ops-work), AI-era extensions
---
## The principle

Once an agent runs in production it stops being a developer's feature and becomes a service, and services need operations. Agents get SLOs at several layers (latency, availability, response quality on a canary set, cost per request, tool-call success), a person who is paged for provider outages, tool outages, quality regressions and cost spikes, and runbooks and postmortems like any other service. The compaction note maps context exhaustion to an out-of-memory failure; the agents note maps a prompt regression to a dependency upgrade.

Source: [AI Agents are Ops Work](doc:sre/ai-agents-are-ops-work) and [Compaction is the New OOM](doc:sre/compaction-is-the-new-oom), two of the AI-era extensions in the [manifesto](doc:sre/manifesto). Google's book predates the question.

## On this platform

- **A service in the catalog.** The [agent sessions](/inside/services/agent-sessions/) are a tier-2 service with an owner, docs, a runbook and their dependencies: the gate, the [observability stack](/inside/services/observability-stack/), the [search instance](/inside/services/searxng/) and the [local LLM](/inside/services/local-llm/).
- **The same gate as everyone.** Each session owns one track of work and pushes through the [conformity gate](/inside/services/conformity-gate/), which checks the text the agents write before any reader sees it. The gate owner is itself an agent session; tier changes stay with the operator ([On-call and escalation](doc:obs/on-call)).
- **Cost metered per request.** Spend and tokens are summed from per-request events, and an alert fires above USD 40 in the trailing hour ([Cost per unit of work](doc:sre/principle-cost-per-unit-of-work)).
- **Agent-layer incidents.** The [phantom spend](/inside/status/#2026-10-09-phantom-spend-counters) incident came from parallel sessions writing one counter series. The [SearXNG](/inside/status/#2026-10-09-searxng-engine-suspensions) incident is a tool dependency outage, one of the paging cases in the manifesto note, and now has six alert rules.
- **Behaviour measured as research.** In the research programme, Stefan Coetzee measures the assembly of model, harness, tools and memory: the [slips log](doc:res/slips-log) records each register slip and who caught it, and the [fawn-opener benchmark](doc:res/fawn-opener-benchmark) is a pre-registered measure of one behaviour across models.

## State

**Partial.** The agents run as a service with an owner, a gate, metered cost and incident records. They have no SLOs: no target for tool-call success, response quality or cost per session ([#37](https://github.com/uncovertechtalent/machinebehavior.io/issues/37)). No canary set runs when the harness or a model changes, and no alert about them reaches anyone ([#36](https://github.com/uncovertechtalent/machinebehavior.io/issues/36)).

## Services that name it

<!-- principle-services -->

## In a company of 10 to 200 people

- Put every production agent in the service catalog with an owner on standby, and treat its prompts, tools and model version as deployable config.
- Keep a small canary set of real tasks with graded answers, and run it before every model, prompt or tool change.
- Meter cost per request and per session from day one, and alert on spend per hour with a threshold set from data.
- Gate what agents publish or change with the same checks as human work, and log each agent action with the session that took it.

## Open work

- [#37 SLOs for the tier-1 services and the agent sessions](https://github.com/uncovertechtalent/machinebehavior.io/issues/37)
- [#36 Alert routing](https://github.com/uncovertechtalent/machinebehavior.io/issues/36)
