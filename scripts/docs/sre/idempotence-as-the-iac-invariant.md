title: Idempotence as the IaC Invariant
summary: The property that makes Infrastructure as Code work is not "code that builds infrastructure." It is idempotence: applying the same configuration to the same target produces the same end-state, no matter how many times you run it or what the prior state was.
parent: infrastructure-as-code
order: 100
labels: concept, iac, idempotence, terraform
aliases: IaC Idempotence | Declarative Infrastructure | Convergence
type: concept
created: 2026-05-04
updated: 2026-05-04
origin: SRE/pillars/05-infrastructure-as-code/Idempotence as the IaC Invariant.md
reviewed: no
---
> The property that makes Infrastructure as Code work is not "code that builds infrastructure." It is **idempotence**: applying the same configuration to the same target produces the same end-state, no matter how many times you run it or what the prior state was.

## Why idempotence is the core

A non-idempotent script breaks the moment reality drifts from its assumption. Run it once on a clean target — works. Run it again — duplicates a resource, errors on a second creation, leaves partial state. Run it on a target that was hand-edited — silent corruption.

Idempotent tools (Terraform, Pulumi, Ansible in declarative mode) work differently:

1. Read **desired state** from code.
2. Read **actual state** from the target.
3. Compute the diff.
4. Apply only the diff.

The same `terraform apply` run 10 times produces 10 no-ops once the target matches. That property is what makes IaC safe to automate, because you can re-run on failure without compounding damage.

## Imperative scripts are not IaC

A bash script that calls `aws ec2 run-instances` is automation, not IaC. It encodes *how to reach* a state, not *what the state should be*. The distinction matters because:

- Imperative scripts cannot detect drift. The script either ran or didn't; the actual config is opaque.
- Imperative scripts cannot be re-run idempotently. The first run creates; the second run duplicates.
- Imperative scripts cannot diff. There is no "plan" stage that shows what will change.

The `terraform plan` step is the killer feature: it answers "what will this run change?" *before* it changes anything. Imperative scripts do not have an equivalent.

## State is the cost

Idempotence requires the tool to know actual-state. Terraform stores it in a state file (S3 backend with DynamoDB locking is the canonical pattern). The state file becomes the system of record. Treat it like production data:

- Encrypted at rest
- Locked during operations (never two `apply`s simultaneously)
- Versioned (S3 versioning or equivalent)
- Restricted access — read implies "knows every secret-arn in the infra"

State corruption is the worst class of IaC failure. There is no `terraform reset`; recovery is hand-editing the state file. Backup your state.

## Drift is the diagnostic

The signal that IaC discipline is healthy: `terraform plan` on main is a no-op. The signal that it is broken: `terraform plan` always wants to change something. Common causes:

| Drift cause | What it indicates |
|---|---|
| Console-edits on managed resources | The team is bypassing IaC under pressure |
| Resources created outside Terraform | Adoption gap; missing module |
| Provider auto-updates | Pin provider versions |
| External controllers modifying tagged resources | Add `lifecycle { ignore_changes }` for those fields specifically |

Persistent drift in `plan` output destroys trust in the tool. Engineers stop reading the plan, then stop noticing real changes.

## See also

[[README]] · [[06-cicd-deployment]] · [[10-toil-reduction]]
