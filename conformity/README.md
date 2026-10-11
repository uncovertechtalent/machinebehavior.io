# Conformity, site tier

Continuous conformity of machinebehavior.io against the working draft "Continuous conformity for deployed AI systems" (draft 0.2, 35 requirements). Self-assessment, not a certification.

- `requirements.json`: the 35 requirements with mark (M mechanical, A assisted, H manual), metric, threshold, check ids, the crosswalk to AI Act, DORA, GDPR and NIST (`maps_to`), and the run 1 self-assessment per row.
- `site-tier.json`: site configuration: deploy gating, schedule, the vendored rule table and its sha256, rule tiers and the recorded false-positive test per blocking rule, placeholder pattern, retention.
- Engine: `.github/actions/conformity/` (composite action: `run.py`, `scan-runner.js`, `rules/vestige-patterns.js` vendored from the public vestige-kit, `fixtures-manual.jsonl`, `fixtures-actions-pinned.jsonl`, `fixtures-actions-owners.jsonl`). Other sites (tychat.io and uncovertechtalent.com) use it pinned to a commit of this repository's main, see "Pinned consumers" below.
- `latest.json`: run history, open and closed findings, requirement states (committed by the workflow).
- `index.html`: the public page, rendered from the latest run (committed by the workflow).
- `runs/`: full run records; written by the workflow and uploaded as artifacts (90 days), not committed.

Rerun by hand, no network, no keys:

```bash
python3 .github/actions/conformity/run.py --root . --config conformity/site-tier.json --requirements conformity/requirements.json --out conformity --dry-run
```

Workflow: `.github/workflows/conformity.yml` runs on push to main, weekly (Mondays 06:17 UTC) and by hand. The Pages deploy job depends on the conformity job.

## Pinned consumers

tychat.io (`.github/workflows/conformity.yml`) and uncovertechtalent.com (`.github/workflows/hugo.yml`) run this action pinned to a full commit SHA of main:

```yaml
uses: uncovertechtalent/machinebehavior.io/.github/actions/conformity@<40-hex sha> # machinebehavior.io conformity, main at <date>
```

A change to the gate reaches them only when the gate owner bumps that SHA on purpose. Dependabot does not bump it: this repository has no release tags, and each consumer's `.github/dependabot.yml` ignores it. Bump step, once per consumer:

1. Merge the gate change here and wait for its Conformity run on main to pass.
2. Read the new SHA: `gh api repos/uncovertechtalent/machinebehavior.io/commits/main --jq .sha`.
3. Dry-run the new `run.py` against the consumer (for uncovertechtalent.com, against its Hugo build output with `--git-dir .`) until it prints `overall=pass`.
4. In the consumer's workflow, replace the SHA and the date in the comment, then open a pull request.
5. After the merge, confirm the consumer's deploy run on main passes and the site serves.

Every other action in this repository and the consumers is pinned to a full commit SHA with its release in a comment. Dependabot (`.github/dependabot.yml`, monthly, one grouped pull request) moves those pins. The check `actions.pinned` (block tier, mapped to CC-5.2) fails a run when a workflow or composite action references an outside action by tag, branch or short SHA, or a Docker image by tag. It reads the `.github` folder of the repository named by `--git-dir` (default: the current directory), never `--root`, so the Hugo consumer's workflows are checked even though its root is the build output. Its known-fail and known-pass references are in `fixtures-actions-pinned.jsonl`, run by `grader.fixtures`. A pin stops a tag from moving and says nothing about who owns the action, so the check `actions.owners` (block tier; a supply-chain control outside draft 0.3, so no requirement row lists it; nearest framework clause NIST CSF 2.0 GV.SC) also fails a run when an outside action, reusable workflow or Docker image comes from an owner outside `actions_owners_allow` in the site config. An entry is an owner (`actions`), an owner/repo (`peaceiris/actions-hugo`) or `docker://<image>`; matching ignores case. Each site lists only the owners its workflows use. Its fixtures are in `fixtures-actions-owners.jsonl`.
