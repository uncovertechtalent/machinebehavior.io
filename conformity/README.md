# Conformity, site tier

Continuous conformity of machinebehavior.io against the working draft "Continuous conformity for deployed AI systems" (draft 0.2, 35 requirements). Self-assessment, not a certification.

- `requirements.json`: the 35 requirements with mark (M mechanical, A assisted, H manual), metric, threshold, check ids, the crosswalk to AI Act, DORA, GDPR and NIST (`maps_to`), and the run 1 self-assessment per row.
- `site-tier.json`: site configuration: deploy gating, schedule, the vendored rule table and its sha256, rule tiers and the recorded false-positive test per blocking rule, placeholder pattern, retention.
- Engine: `.github/actions/conformity/` (composite action: `run.py`, `scan-runner.js`, `rules/vestige-patterns.js` vendored from the public vestige-kit, `fixtures-manual.jsonl`). Other sites use it with `uses: uncovertechtalent/machinebehavior.io/.github/actions/conformity@main`.
- `latest.json`: run history, open and closed findings, requirement states (committed by the workflow).
- `index.html`: the public page, rendered from the latest run (committed by the workflow).
- `runs/`: full run records; written by the workflow and uploaded as artifacts (90 days), not committed.

Rerun by hand, no network, no keys:

```bash
python3 .github/actions/conformity/run.py --root . --config conformity/site-tier.json --requirements conformity/requirements.json --out conformity --dry-run
```

Workflow: `.github/workflows/conformity.yml` runs on push to main, weekly (Mondays 06:17 UTC) and by hand. The Pages deploy job depends on the conformity job.
