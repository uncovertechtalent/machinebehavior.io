title: Zero trust
summary: Nothing is trusted because of where it comes from: each input, identity, dependency, and report is verified at the boundary where it is used, and each actor gets the least access its job needs. Here actions are pinned and allowlisted, every change goes through a pull request and the gate, keys and job permissions are scoped, and third-party text is quarantined; a shared account, a repository-wide bot key, and network-based access to internal dashboards remain.
parent: principles-in-practice
order: 150
labels: principle, sre, security, zero-trust, least-privilege, supply-chain
owner: Stefan Coetzee
reviewed: 2026-10-13
review_by: 2027-01-11
type: explanation
state: partial
source: [Pillar 8, security](doc:sre/security#zero-trust); [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final)
---
## The principle

Nothing is trusted because of where it comes from. An input, an identity, a dependency, and a report are each verified at the boundary where they are used, whether they arrive from the internet, from a colleague, from a vendor, or from an agent session. Each actor, whether a person, a job, or an agent, gets the least access its job needs, for the shortest time, and each use is recorded. Nobody gets access for being on the right network, and nobody accepts a result because it comes from a familiar name or shows a green status.

Source: the Zero Trust section of [Security](doc:sre/security#zero-trust) and [Defense in Depth and Trust Boundaries](doc:sre/defense-in-depth-and-trust-boundaries), pillar 8 of the framework. Reports are covered by [Truth, verified, working](doc:sre/principle-truth-verified-working). References: NIST's [Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final) (SP 800-207), Google's [BeyondCorp](https://research.google/pubs/beyondcorp-a-new-approach-to-enterprise-security/), and the [least privilege](https://google.github.io/building-secure-and-reliable-systems/raw/ch05.html) chapter of Building Secure and Reliable Systems.

## On this platform

Dependencies:

- **Actions pinned and allowlisted.** Every action from outside the repository is pinned to a full 40-character commit SHA, and its owner must be on the allowlist in `conformity/site-tier.json`, which holds one owner today, `actions`. The gate checks `actions.pinned` and `actions.owners` block the deploy on a tag or branch reference or an unlisted owner ([Conformity gate](doc:eng/conformity-gate); [#59](https://github.com/uncovertechtalent/machinebehavior.io/issues/59), [#61](https://github.com/uncovertechtalent/machinebehavior.io/issues/61), pins in [#56](https://github.com/uncovertechtalent/machinebehavior.io/pull/56)). Dependabot proposes new pins monthly, and a new owner needs its own reviewed pull request.
- **The workflow checked as code.** A zizmor job reads `.github/` for template injection, broad permissions, persisted credentials, and unpinned references on every run, installed from hash-pinned wheels ([#65](https://github.com/uncovertechtalent/machinebehavior.io/issues/65)). The deploy does not wait for it.
- **The other sites pin the gate.** tychat.io and uncovertechtalent.com run this gate pinned to a commit of `main`, so a change to the gate reaches them only when someone moves the pin.
- **No third party in the reader's browser.** Pages load no script, font, or style from another company ([ADR-0010](doc:eng/adr-0010-no-third-party-requests)).

Identities and access:

- **Every change through a pull request and the gate.** A ruleset on `main` requires a pull request and a passing Conformity checks job, and blocks force pushes and branch deletion; the repository allows squash merges only ([ADR-0029](doc:eng/adr-0029-changes-through-pull-requests)). A pull request run checks the merge result and commits and deploys nothing.
- **One key per writer.** The two automated writers that push to `main`, the gate's bot and the weekly probe record, each have their own deploy key, the only bypass the ruleset allows. The workflow passes the bot's key to the checkout only on runs from `main`, and the Pages environment accepts deployments from `main` and `gh-pages` only.
- **Permissions per job.** The workflow starts with no permissions (`permissions: {}`), and each job names what it needs: the checks job writes contents for the bot commit, the deploy job reads contents and writes to Pages, and the zizmor job reads contents.
- **Agent sessions within limits.** The shared agent settings deny reading or editing `.env` files and the `secrets/` folder, deny merges through `gh api`, and ask before every `gh pr merge` ([Agents in this repository](doc:eng/agents)).
- **Paths allowlisted at the front door.** The public Grafana sits behind a proxy that passes only the shared dashboard paths and answers everything else with 404 ([Access model](doc:eng/access-model)).

Inputs and reports:

- **Agent-written pages are inputs.** The gate checks every page an agent session writes before a reader sees it, by the same rules as the operator's pages.
- **Private terms kept out.** Names that must stay private (prospective employers or clients, internal shorthand, and private hosts) do not enter the public repository. A pre-push hook on the operator's machine stops a push that adds one ([CTO powersuit #2](https://github.com/uncovertechtalent/cto-powersuit/pull/2)), and the `private.terms` check scans the tree and the build output in a dry run ([#64](https://github.com/uncovertechtalent/machinebehavior.io/pull/64)). The term list stays outside every repository.
- **Third-party text quarantined.** Since 2026-10-13 the operator's agent harness keeps raw third-party text (posts, e-mails, web pages, and pasted text) in a store outside the knowledge base. A session reads an item only through a summarising model that has no tools and returns a fixed-shape summary, with measured fields computed in code and a flag for text aimed at an AI model; a hook denies every other read of the store. It runs on the operator's machine and is not part of this repository.
- **Reports are claims until probed.** A session's completion message, a review comment, or a status line is a claim until someone checks the artifact ([Truth, verified, working](doc:sre/principle-truth-verified-working)). The change review is input to the merge decision and never evidence of conformity, and no requirement of the gate may list it. The review job that reads pull request text gives the model no write token, no shell, and no network; until that job has its key, the review runs on the operator's machine ([Software delivery lifecycle](doc:eng/sdlc)).

## State

**Partial.** The supply chain, the change path, and the job permissions follow the principle, and the gate enforces most of it. Four parts are missing:

- One GitHub account carries the operator and every agent session, so GitHub cannot tell their actions apart or give a session less access than the operator ([#79](https://github.com/uncovertechtalent/machinebehavior.io/issues/79)).
- `CONFORMITY_PUSH_KEY` is a repository secret, so a workflow run on any branch can read it; the workflow's branch guard stops accidents only. Moving it to an environment limited to `main` is a settings change for the operator ([#76](https://github.com/uncovertechtalent/machinebehavior.io/issues/76)).
- A pull request that edits `.github/` or the gate configuration runs its own copy of the gate and can loosen it. For those paths, the person who merges is the only control ([ADR-0029](doc:eng/adr-0029-changes-through-pull-requests)).
- The internal dashboards, Prometheus, and Loki are reachable from the home network only, so the network location grants access. The identity-aware design on the [Access model](doc:eng/access-model) page is not built, and security headers wait on the hosting decision ([#26](https://github.com/uncovertechtalent/machinebehavior.io/issues/26)).

## Services that name it

<!-- principle-services -->

## In a company of 10 to 200 people

- Pin every third-party action, package, and image by digest, keep an allowlist of their owners, and let a bot propose the updates.
- Give every person, job, and agent its own identity, with permissions that start at none and are added per job. Never share an account between a person and an automation.
- Keep secrets in environments that only the protected branch can read, and prefer short-lived tokens from OIDC over stored keys.
- When an agent with tools reads text from outside (tickets, e-mails, pull request bodies, web pages), give it a summary made in a sandbox, and never let that text start an action.
- Replace network-based access to internal tools with an identity-aware proxy and a device check.

## Open work

- [#79 One GitHub account for the operator and every agent session](https://github.com/uncovertechtalent/machinebehavior.io/issues/79)
- [#76 Move CONFORMITY_PUSH_KEY to an environment limited to main](https://github.com/uncovertechtalent/machinebehavior.io/issues/76)
- [#77 Dependabot cannot open pull requests for the tool pins under .github/](https://github.com/uncovertechtalent/machinebehavior.io/issues/77)
- [#26 Security headers](https://github.com/uncovertechtalent/machinebehavior.io/issues/26)
