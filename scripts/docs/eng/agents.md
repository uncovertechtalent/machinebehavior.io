title: Agents in this repository
summary: Which coding agents work on machinebehavior.io, with which plugins, permissions, hooks and MCP servers, how a change reaches main, how their spend is metered, and who owns the setup.
order: 16
labels: agents, ai-ops, harness
owner: Stefan Coetzee
created: 2026-10-11
updated: 2026-11-25
reviewed: 2026-10-11
review_by: 2027-01-09
type: reference
---
Every agent session in this repository starts from the same shared setup in git. Personal changes go into `.claude/settings.local.json`, which `.gitignore` keeps out of git. All human and agent commits use one GitHub account.

## Harness

| Part | Where | What it holds |
|---|---|---|
| Shared settings | `.claude/settings.json` | Permissions: allow, ask, deny |
| Instructions | `CLAUDE.md` | The pull request flow, the deploy gate and its dry run, records and ownership |
| Pull request template | `.github/pull_request_template.md` | Change, ticket or decision, checklist, the change review, rollback |
| Plugins | Local marketplace `cto-powersuit` | Modules fitted here: `sdlc`, `reliability`, `finops`, `aieo`, `fit`, `ai-ops` |
| MCP servers | None shared | Sessions bring their own user-level setup; there is no `.mcp.json` |
| Hooks | None shared | Sessions bring their own user-level hooks |

## Permissions

- Allowed without asking: the gate dry run as written in `CLAUDE.md`, `git status`, `git diff`, `git log`, `gh pr view`, `gh pr diff`, `gh pr checks`, `gh run view`.
- Asked every time: `gh pr merge`, the review step. Claude Code asks on a matching ask rule in every permission mode, the bypass mode included. Pushing a branch and opening a pull request have no rule in the shared settings and follow the session's permission mode; the branch rules on `main` reject a direct push.
- Denied: reading or editing `.env` files and the `secrets/` folder, and merging a pull request through `gh api` (the REST merge endpoint and the GraphQL merge and auto-merge mutations), so `gh pr merge` with its ask rule is the only merge path a session has.
- Never in the shared settings: a rule that allows every shell command or every fetch, or the bypass mode.

These settings load only in a session started in this folder. A session started elsewhere that works here does not get them.

## How a change reaches main

Through a pull request ([ADR-0029](doc:eng/adr-0029-changes-through-pull-requests)). A branch ruleset on `main` requires a pull request and a passing Conformity checks job ([Conformity gate](doc:eng/conformity-gate)); it goes on once the conformity bot pushes with its deploy key. One approval is required ([ADR-0054](doc:eng/adr-0054-approval-on-the-final-head)): Stefan Coetzee approves on GitHub as skjoldar, on the pull request's final head, and the session, under the agent account uncovertechtalent, pushes every commit and merges with that head pinned. A commit pushed from his account makes his approval not count.

1. Branch from `origin/main`, run the gate dry run until it prints `overall=pass`, push the branch, open the pull request with the template.
2. Wait for the Conformity checks job on the pull request.
3. Push every fix, wait until the pull request shows the pushed head, then run the local reviewer (`~/.config/powersuit/review-pr.sh`) on that head and post its comment.
4. Stefan Coetzee approves on that head as skjoldar; the session merges with the head pinned (`gh pr merge --squash --match-head-commit <sha>`). A newer commit dismisses the approval and needs a new one.

Two automated writers push to `main` directly, each through its own deploy key that the protection lets through: conformity-bot, which commits the gate result after every run, and the weekly decision-layer probe record. The lifecycle around this flow is in [Software delivery lifecycle](doc:eng/sdlc).

## Spend

Agent spend is metered per API request. Budgets and alerts are in [Budgets and alerts](doc:fin/budgets-and-alerts), the cost model in [Cost model](doc:fin/cost-model), and the service in the catalog at [Agent sessions](/inside/services/agent-sessions/).

## Owner

Stefan Coetzee owns this setup. A change to the shared settings, the plugin list, `CLAUDE.md` or the pull request template goes through a pull request.
