title: 6. CI/CD & Deployment
summary: "If it hurts, do it more.
parent: pillars
order: 60
aliases: CICD Deployment Cluster | SRE CICD Cluster | 06-cicd-deployment
created: 2026-04-25
updated: 2026-06-08
origin: SRE/pillars/06-cicd-deployment/README.md
reviewed: no
---
> "If it hurts, do it more often."

## What is CI/CD?

- **Continuous Integration** — Merge code frequently, validate automatically
- **Continuous Delivery** — Code is always deployable
- **Continuous Deployment** — Every change goes to production automatically

## Deployment Strategies

### Big Bang
- All at once
- Simple but risky
- Use only for dev/test

### Rolling Update
- Gradual replacement of instances
- Zero downtime
- Mixed versions during rollout

### Blue-Green
- Two identical environments
- Instant switchover
- Easy rollback
- 2x infrastructure cost

### Canary
- Small % of traffic to new version
- Monitor for errors
- Gradually increase if healthy
- Best for catching real-world issues

### Feature Flags
- Deploy code without enabling feature
- Enable for specific users/% of traffic
- Decouple deployment from release

## Key Concepts

### Pipeline Stages
```
Commit → Build → Test → Security Scan → Deploy Dev → Deploy Staging → Deploy Prod
```

### Artifact Management
- Build once, deploy everywhere
- Immutable artifacts (Docker images, binaries)
- Versioned and tagged
- Signed and verified

### Environment Promotion
```
Dev → Staging → Production
     (same artifact)
```

## Topics

- [ ] Pipeline design patterns
- [ ] Build optimization (caching, parallelization)
- [ ] Test strategies (unit, integration, e2e)
- [ ] Security scanning (SAST, DAST, SCA)
- [ ] Deployment automation
- [ ] Rollback strategies
- [ ] Feature flags implementation
- [ ] Database migrations
- [ ] Configuration management
- [ ] Secrets in pipelines

## Progressive Delivery

### Canary Analysis
```
Deploy canary (5% traffic)
  → Monitor metrics (errors, latency)
    → Compare to baseline
      → Pass: Increase traffic
      → Fail: Automatic rollback
```

### Metrics to Watch During Rollout
- Error rate (4xx, 5xx)
- Latency (p50, p95, p99)
- Resource usage
- Business metrics (conversions, revenue)

## Tools

| Tool | Purpose |
|------|---------|
| GitHub Actions | CI/CD pipelines |
| GitLab CI | CI/CD pipelines |
| ArgoCD | Kubernetes GitOps |
| Flux | Kubernetes GitOps |
| Spinnaker | Advanced deployment strategies |
| Flagger | Progressive delivery for Kubernetes |
| LaunchDarkly | Feature flags |
| Argo Rollouts | Canary/Blue-green for Kubernetes |

## Pipeline Best Practices

### Fast Feedback
- Fail fast (run quick tests first)
- Parallelize where possible
- Cache dependencies
- Target: < 10 minutes for CI

### Secure Pipelines
- No secrets in code
- Use OIDC for cloud auth
- Scan dependencies
- Sign artifacts
- Audit pipeline changes

## Anti-Patterns

- Long-running pipelines (> 30 min)
- Manual approval gates everywhere
- No rollback plan
- Deploying on Fridays
- Snowflake environments
- Testing in production (without feature flags)

## Reading

- Accelerate (Forsgren, Humble, Kim)
- Continuous Delivery (Humble, Farley)
- Google SRE Book: Chapter 8 (Release Engineering)

## Regulatory and control mappings

- [[ISO 27001 Annex A.8 Technological Controls]] A.8.32 Change management. A.8.25-A.8.30 secure development lifecycle. A.8.31 Separation of dev/test/prod environments.
- [[NIS2 Security Measures]] Art 21(e) secure development + change management + vulnerability handling.
- [[DORA Resilience Testing]] Art 24-25 testing programme. TLPT for significant entities.
- [[ITIL 4 Practices]] Change Enablement + Release Management + Deployment Management.
- [[SLSA SBOM Cluster]] — build provenance + SBOM at CI/CD gates.
- [[Cyber Resilience Act Cluster]] — for software products: vulnerability handling + security updates.

## Atoms

- [[Progressive Delivery Patterns]]

## Published expressions

- [[2024-12-30_ci-cd-pipelines-how-do-they-work-part-1-prod-is-burning|CI/CD Pipelines, how do they work? — Part 1: prod is burning]] -- why an unguarded pipeline lets prod burn.
- [[2024-12-30_ci-cd-pipelines-how-do-they-work-part-2-preventing-prod-fires|CI/CD Pipelines, how do they work? — Part 2: preventing prod fires]] -- the build/test/deploy gates that prevent prod fires.
