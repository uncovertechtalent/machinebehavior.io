title: Eliminate toil
summary: Toil is manual, repetitive, automatable work that grows with load and leaves nothing behind; SRE caps it so engineering time remains. Here generators and the deploy job removed most of it; a rebase before every push, hand deploys of the observability stack and the screenshot retakes remain, and nobody measures the share.
parent: principles-in-practice
order: 80
labels: principle, sre, toil, automation
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
state: partial
source: [Pillar 10, toil reduction](doc:sre/toil-reduction); [Google SRE book ch. 5](https://sre.google/sre-book/eliminating-toil/)
---
## The principle

Toil is operational work that is manual, repetitive, automatable, tactical, without lasting value, and that grows in step with the service. If a person does something a computer could do, that is a bug. Google caps toil at half of each SRE's time; above the cap, SRE turns back into an operations team that grows with the load.

Source: [Toil Reduction](doc:sre/toil-reduction) and [Toil vs Engineering and the 50 Percent Rule](doc:sre/toil-vs-engineering-and-the-50-percent-rule); Google's [Eliminating Toil](https://sre.google/sre-book/eliminating-toil/).

## On this platform

Removed:

- **Pages nobody edits by hand.** The catalog, the status page, the docs tree, the board, the changelog and the page chrome are generated from sources in git ([Operations work done as software](doc:sre/principle-ops-as-software)).
- **Refreshes in the deploy job.** Every deploy re-crawls the map, rebuilds the search index and snapshots the deploy feed and the issues, without a commit ([Deploy pipeline](doc:eng/deploy-pipeline)).
- **Checks nobody runs by hand.** On every push the gate checks the form of every internal link, the canonical tag of every page and each page's sitemap entry ([Conformity gate](doc:eng/conformity-gate)).
- **Redaction as code.** The vault import replaces private addresses, e-mail addresses and an employer name, and lists every change in a report ([Docs tree](doc:eng/docs-tree)).
- **Rules at the output boundary.** Hooks in the agent harness block banned phrasing before anyone reads the text; the [slips log](doc:res/slips-log) records three such blocks, from three different hooks.

Left, by the definition above:

- **A rebase before every push.** The gate commits its record to `main` after each run, so every writer pulls before each push; a [runbook](doc:eng/runbook-push-rejected) documents the workaround ([#39](https://github.com/uncovertechtalent/machinebehavior.io/issues/39)).
- **Hand deploys of the observability stack.** The repository is copied to the home server and started with `docker compose up -d --build` ([Architecture](doc:obs/architecture)). Making a dashboard public needs an API call on that server ([Share a dashboard](doc:obs/runbook-share-a-dashboard)).
- **Builds on one machine.** The vault import and the generators run on the author's machine, and their output is committed ([#40](https://github.com/uncovertechtalent/machinebehavior.io/issues/40)).
- **Screenshots.** The [founder tour](/inside/tour/) shows screenshots of live pages, retaken by a script run by hand when a page changes ([ADR-0020](doc:eng/adr-0020-founder-tour)).

## State

**Partial.** Most repeated work runs as code. Four kinds of toil remain, each named above, and nobody records how much of the operator's or the sessions' time goes into it, so the 50% cap cannot be checked. Most of the hands-on work is done by agent sessions; the operator's share is steering and review, which is engineering time by the definition and is not measured either.

## Services that name it

<!-- principle-services -->

## In a company of 10 to 200 people

- Keep a toil log for one month: task, how often, minutes each. Automate the top three, then repeat.
- Report the toil share per team each quarter. Above half, the team's next quarter goes to removing toil.
- Count a runbook step that someone runs by hand more than twice a week as a bug, with an owner.
- Count toil removed in the team's goals, next to features shipped.

## Open work

- [#39 Toil: the bot commit on main forces a rebase before every push](https://github.com/uncovertechtalent/machinebehavior.io/issues/39)
- [#40 CI check: generated pages match their sources](https://github.com/uncovertechtalent/machinebehavior.io/issues/40)
