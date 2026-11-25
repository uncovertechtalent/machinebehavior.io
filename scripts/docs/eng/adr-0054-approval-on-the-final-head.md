title: ADR-0054: Stefan Coetzee approves on the final head, and the agent account pushes and merges
summary: The ruleset on main requires one approval, an approval of the last push, and an approval for changes pushed by someone else. Agents work under their own GitHub account, which opens, pushes and merges; Stefan Coetzee approves on the pull request's final head under his. Replaces the parts of ADR-0029 that rest on one account and no required approvals.
parent: decision-log
order: 54
adr: 54
status: accepted
created: 2026-11-25
labels: adr, decision, sdlc, review, agents
owner: Stefan Coetzee
reviewed: 2026-11-25
review_by: 2027-02-23
type: explanation
---
## Context

[ADR-0029](doc:eng/adr-0029-changes-through-pull-requests) recorded a ruleset on `main` that requires no approvals, because every commit came from one GitHub account and GitHub never counts an author's approval of their own pull request. Two things have changed since. Agent sessions work under their own account, uncovertechtalent, and Stefan Coetzee under his, skjoldar. And the ruleset on `main`, as read on 2026-11-25 (`gh api repos/uncovertechtalent/machinebehavior.io/rules/branches/main`), requires approvals:

- `required_approving_review_count: 1`;
- `require_last_push_approval: true`: the last push must be approved by someone other than the person who pushed it;
- `require_extra_approval_for_unattributed_changes: true`: as seen on 2026-11-25, a pull request holding commits pushed from the approver's own account stays blocked on his approval, even when the last push came from another account;
- `dismiss_stale_reviews_on_push: true`, squash merges only, and the required check "Conformity checks", as before.

The repository belongs to the user account uncovertechtalent, the agent account, and its token has administrator rights (`admin: true`, read 2026-11-25). When a merge was refused that day, GitHub offered that account `gh pr merge --admin`: a repository administrator can bypass the ruleset.

On 2026-11-25 the records and the practice came apart three ways ([#256](https://github.com/uncovertechtalent/machinebehavior.io/issues/256)). Three pull requests (#243, #246, #250) merged within a minute of their local review, before the session's review-fix commit reached GitHub, so each fix needed a follow-up pull request. A workflow change pushed from Stefan Coetzee's account because the agent token had no `workflow` scope could not be merged on his approval, and had to be closed and redone (#253, then #255).

## Decision

Stefan Coetzee, 2026-11-25: "it needs approvals", and "maybe we should stick with me just approving and you merging".

- **The ruleset stays as it is:** one approval, the last push approved by someone other than its pusher, approval for changes pushed by others, stale approvals dismissed on push.
- **Stefan Coetzee approves, the agent account merges.** He approves on GitHub as skjoldar. A session, under uncovertechtalent, merges only when an approval by skjoldar has a `commit_id` equal to the pull request's current head, and merges with that head pinned (`gh pr merge --squash --match-head-commit <sha>`). His approval on the final head is the explicit go that [ADR-0029](doc:eng/adr-0029-changes-through-pull-requests) and `CLAUDE.md` ask for.
- **The agent account pushes every commit of a pull request.** A commit pushed from the approver's account makes his approval not count, under both of the last two rules. The agent token has the `workflow` scope since 2026-11-25, so changes under `.github/workflows/` are pushed from it too.
- **The review comes last.** A session pushes every fix first, waits until the pull request shows the pushed head, runs the local reviewer on that head and posts its comment, and only then asks for the approval. The approval therefore lands on the head the posted review covers.
- **Never with administrator rights.** A session does not merge with `--admin`, does not change the ruleset, and does not merge without the approval. The shared settings (`.claude/settings.json`) ask before every `gh pr merge` and deny the merge endpoints of the API; they have no rule for `--admin` beyond that ask and none for the rulesets API. Closing that gap, by moving the ownership or by deny rules, is [#258](https://github.com/uncovertechtalent/machinebehavior.io/issues/258).
- **`.github/` changes:** the required approval is now the control ADR-0029 said a second account would allow. The person approving reads every change under `.github/` and `conformity/site-tier.json` first. CODEOWNERS names skjoldar for those paths; the ruleset does not require a code owner review, so the approval covers them.

## Consequences

- GitHub enforces the approval on every account except a repository administrator, and the agent account is the administrator. For the agent account the approval holds by this record, by the session settings, and by the pinned merge, until [#258](https://github.com/uncovertechtalent/machinebehavior.io/issues/258) closes the gap.
- GitHub now records who approved and who merged under two names, so a session's merge can be told from Stefan's.
- A late commit cannot slip past an approval: it dismisses the approval, and the merge pins the head.
- A pull request whose commits were pushed from skjoldar cannot be merged by approval; it is redone with the agent account's commits.
- A rollback is a revert pull request that waits for one more check run and for the approval ([Roll back a deploy](doc:eng/runbook-rollback)).
- The agent token can now change workflow files, gate code and deploy permissions in a branch. Each such change still needs his approval before it reaches `main`, and a pull request runs its own copy of the workflow ([ADR-0029](doc:eng/adr-0029-changes-through-pull-requests), consequences), so the approval read of `.github/` matters more than before.

## What this replaces

In ADR-0029: the premise that every commit uses one account, the ruleset clause "requires no approvals", the merge as the review step, the rule "Stefan Coetzee merges, or a session merges on his go", the consequences that GitHub cannot tell a session's merge from Stefan's and that a required review for `.github/` would need a second account, the rollback that waits for one check run only, and the deploy keys as the only bypass (a repository administrator can bypass too). ADR-0029 stays accepted for the rest: changes reach `main` through pull requests, the required Conformity checks, the deploy keys of the conformity bot and the probe record, and the manual-run guard.
