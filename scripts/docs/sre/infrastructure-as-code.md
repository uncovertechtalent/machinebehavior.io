title: 5. Infrastructure as Code
summary: "If it's not in Git, it doesn't.
parent: pillars
order: 50
aliases: Infrastructure as Code Cluster | IaC Cluster | SRE IaC Cluster | 05-infrastructure-as-code
created: 2026-04-25
updated: 2026-06-08
origin: SRE/pillars/05-infrastructure-as-code/README.md
reviewed: no
---
> "If it's not in Git, it doesn't exist."

## What is Infrastructure as Code?

Managing and provisioning infrastructure through machine-readable definition files rather than manual processes.

## Core Principles

### Declarative > Imperative
- **Declarative** — Describe desired state, tool figures out how
- **Imperative** — Describe steps to achieve state

### Immutable Infrastructure
- Never modify running infrastructure
- Replace instead of update
- Every change is a new deployment

### Version Control
- All infrastructure code in Git
- Pull requests for changes
- Audit trail of who changed what when

## Key Concepts

### State Management
- **Local state** — Simple but dangerous (drift, conflicts)
- **Remote state** — Shared, locked, versioned (S3, GCS, Terraform Cloud)
- **State locking** — Prevent concurrent modifications

### Drift Detection
- Actual infrastructure diverges from code
- Causes: manual changes, failed applies, external systems
- Solutions: regular plan/diff, automated remediation

### Modules and Reusability
```
modules/
├── vpc/           # Reusable VPC module
├── eks-cluster/   # Reusable EKS module
└── rds/           # Reusable RDS module

environments/
├── dev/           # Uses modules
├── staging/       # Uses modules
└── prod/          # Uses modules
```

## Topics

- [ ] Terraform fundamentals
- [ ] State management strategies
- [ ] Module design patterns
- [ ] Environment promotion
- [ ] Secret management in IaC
- [ ] Testing infrastructure code
- [ ] Policy as code (OPA, Sentinel)
- [ ] GitOps workflows
- [ ] Drift detection and remediation
- [ ] Cost estimation in IaC

## GitOps

### Pull-Based Deployment
```
Git Repo → GitOps Operator → Kubernetes
         (ArgoCD/Flux)
```

### Benefits
- Single source of truth
- Audit log built-in
- Easy rollback (git revert)
- Self-healing (reconciliation loop)

## Tools

| Tool | Purpose |
|------|---------|
| Terraform | Multi-cloud IaC |
| Pulumi | IaC with real programming languages |
| CloudFormation | AWS-native IaC |
| Ansible | Configuration management |
| ArgoCD | Kubernetes GitOps |
| Flux | Kubernetes GitOps |
| Crossplane | Kubernetes-native IaC |

## Directory Structure

```
infrastructure/
├── modules/           # Reusable components
│   ├── networking/
│   ├── compute/
│   └── database/
├── environments/      # Environment-specific
│   ├── dev/
│   ├── staging/
│   └── prod/
├── policies/          # OPA/Sentinel policies
└── .github/workflows/ # CI/CD for infrastructure
```

## Anti-Patterns

- ClickOps (manual console changes)
- Monolithic configurations
- Hardcoded values
- No state locking
- Secrets in code
- No environment separation

## CI/CD for Infrastructure

```yaml
# Example GitHub Actions workflow
on: pull_request
jobs:
  terraform:
    steps:
      - terraform fmt -check
      - terraform init
      - terraform validate
      - terraform plan
      - # Apply only on merge to main
```

## Reading

- Terraform: Up & Running (O'Reilly)
- Infrastructure as Code (O'Reilly)
- Google SRE Book: Chapter 8 (Release Engineering)

## Regulatory and control mappings

- [[ISO 27001 Annex A.8 Technological Controls]] A.8.9 Configuration management. A.8.32 Change management. A.8.31 Separation of dev/test/prod environments.
- [[NIS2 Security Measures]] Art 21(e) secure development.
- [[DORA ICT Risk Management]] Art 9 protection (configuration).
- [[ITIL 4 Practices]] Service Configuration Management + Deployment Management + Change Enablement.
- [[SLSA SBOM Cluster]] — supply chain integrity for IaC modules and dependencies.

## Atoms

- [[Idempotence as the IaC Invariant]]
