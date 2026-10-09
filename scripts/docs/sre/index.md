title: SRE Handbook
summary: Site reliability engineering from the knowledge vault: the manifesto, ten pillars, patterns, runbooks, tools and incident records.
created: 2026-04-25
updated: 2026-06-08
origin: SRE/Home.md
reviewed: no
labels: moc, sre
---
Practical SRE training material. Opinionated, experience-driven, 30+ years of operational reality.

## The Manifesto

**The substrate principle**: [[SRE as Truth Verified Working]] -- the discipline is about claims being true, verified, working. Parent of the ten pillars; same principle applied to LLM-substrate (Receipts Standard) and people-substrate (Three-Layer Position Model, real-emotional-maturity).


[SRE Manifesto](SRE/manifesto/README.md) -- SRE is a role, not a team. The concentric model. Standby is the differentiator.

**AI-era extensions:**
- [[AI Agents are Ops Work]] — agent SLOs, agent error budgets, agent paging
- [[Compaction is the New OOM]] — context exhaustion as the new operational hazard
- [[Graph-RAG over Flat RAG for Operational Knowledge]] — why ops knowledge needs graph retrieval
- [[The Disappearing Full-Stack Ops Engineer]] — team design when generalists are statistically absent


> GitHub-render mirror: [[SRE/README|SRE/README.md]]

## Published expressions

- [[2024-12-27_s-uper-r-elatable-e-xperience|(S)uper (R)elatable (E)xperience]] -- public front-door definition of SRE vs DevOps vs platform; the "Grossly oversimplified" framing of what this whole framework is.

## The Pillars

| # | Pillar | Focus |
|---|--------|-------|
| 1 | [Reliability](SRE/pillars/01-reliability/README.md) | SLIs, SLOs, SLAs, Error Budgets |
| 2 | [Scalability](SRE/pillars/02-scalability/README.md) | Horizontal/Vertical scaling, Capacity planning |
| 3 | [Observability](SRE/pillars/03-observability/README.md) | Monitoring, Logging, Tracing, Alerting |
| 4 | [Incident Management](SRE/pillars/04-incident-management/README.md) | On-call, Response, Postmortems |
| 5 | [Infrastructure as Code](SRE/pillars/05-infrastructure-as-code/README.md) | Terraform, GitOps, Immutable infrastructure |
| 6 | [CI/CD & Deployment](SRE/pillars/06-cicd-deployment/README.md) | Progressive delivery, Canary, Blue-green |
| 7 | [Performance](SRE/pillars/07-performance/README.md) | Latency, Throughput, Optimization |
| 8 | [Security](SRE/pillars/08-security/README.md) | Shift-left, Zero-trust, Secrets management |
| 9 | [Cost Optimization](SRE/pillars/09-cost-optimization/README.md) | FinOps, Right-sizing, Waste elimination |
| 10 | [Toil Reduction](SRE/pillars/10-toil-reduction/README.md) | Automation, Self-service, Elimination |

## Supporting Content

- [Patterns](SRE/patterns/README.md) -- reusable architecture patterns. 7 atoms covering memory architecture, retrieval, hardware/inference trade-offs.
- [Runbooks](SRE/runbooks/README.md) -- operational procedures. 5 canonical runbooks (outage response, DB failover, rollback deployment, cert rotation, credential rotation). 6 more planned.
- [Tools](SRE/tools/README.md) -- tool-specific guides. 3 atoms (Headscale, OpenCode, Dolt).

## Maturity Model

```
Level 0: Reactive     -- Fighting fires, manual everything
Level 1: Defined      -- Documented processes, basic monitoring
Level 2: Measured     -- SLOs defined, error budgets tracked
Level 3: Automated    -- Self-healing, auto-scaling, GitOps
Level 4: Optimized    -- Proactive capacity, chaos engineering, continuous improvement
```

## Compliance and regulatory frame

SRE work intersects with compliance frameworks and regulatory regimes. See [08-security](SRE/pillars/08-security/README.md) for full cluster index. Quick map:

- **InfoSec management**: [[ISO 27001 Cluster]] · [[SOC 2 Cluster]] · [[NIST CSF Cluster]] · [[BSI IT-Grundschutz Cluster]]
- **EU regulation**: [[GDPR Cluster]] · [[NIS2 Cluster]] · [[DORA Cluster]] · [[Cyber Resilience Act Cluster]] · [[EU AI Act Cluster]]
- **AI governance**: [[ISO 42001 Cluster]] · [[NIST AI RMF Cluster]] · [[OWASP LLM Top 10 Cluster]]
- **Service mgmt**: [[ITIL Cluster]] · [[COBIT Cluster]]
- **Continuity**: [[ISO 22301 Cluster]]
- **Supply chain**: [[SLSA SBOM Cluster]]
- **Threat intel**: [[MITRE Cluster]]
- **Automotive**: [[TISAX Cluster]] · [[ISO 21434 Cluster]] · [[UN R155 R156 Cluster]] · [[ASPICE Cluster]]
- **Sector**: [[PCI DSS Cluster]] · [[HITRUST Cluster]] · [[FedRAMP CMMC Cluster]]

## Cross-Project

- [[Home|Career Vault]] -- Outcome Engineering framework, [employer] accomplishments
  - Pillar 9 (Cost Optimization) connects to [FinOps Practice](../career/accomplishments/FinOps%20Practice.md)
  - Pillar 4 (Incident Management) connects to [Principle 7: Failures are System Data](../career/principles/07%20Failures%20are%20System%20Data.md)
  - Pillar 10 (Toil Reduction) connects to [Principle 5: Automate or Justify](../career/principles/05%20Automate%20or%20Justify.md)
- [[Home|UncoverTechTalent]] -- interview training, SRE hiring signals
- [[Home|ThatFinOpsGuy]] -- FinOps consulting (deep overlap with Pillar 9)
- [Video Summaries](../short-form-video-transcriber/summaries/Tags.md) -- tagged reference material
## People as SRE substrate

Same discipline applies to the human substrate the system runs on. Home network = office network = work network — one physical surface, all of it under the same operating frame. The psychology / developmental-position / competency corpora are the people-substrate layer of this SRE practice. The Receipts Standard (`~/.claude/projects/-Users-stefancoetzee/memory/feedback_receipts_standard.md`) is the LLM-substrate application of the same principles: probe before assert, snapshot before change, receipts not vibes.

- Bridge essay: [[interview-training-psychology-parallels|Interview Training as Applied Clinical Psychology]] -- hiring/interviewing as the substrate-observability tooling; 11 explicit parallels between clinical-craft and interview-craft
- Psychology cluster: [[pillars/psychology/Psychology Cluster|Psychology MOC]] -- substrate atoms (ownership-psychology axis, real-emotional-maturity, nervous-system-regulation, narcissism, fawning, hyper-independence, caretaker-syndrome, learned-helplessness, locus-of-control, amygdala-as-smoke-detector)
- Developmental-position cluster: [[pillars/developmental-position/_moc|Developmental Position and Distortion]] -- six-axis framework + Three-Layer Position Model (substrate / apparent / assigned) + Trauma Filter + Defense-Response Model
- Interview cycle + competency MOCs: [[Interview Cycle Cluster|Interview Cycle]] · [[Competencies Cluster|Competencies Home]] · [[PM Dimensions Cluster|PM Psychological Dimensions]]
- Per-pillar people-substrate cross-links live inside each pillar README's "People-substrate cross-cluster" section (pillars 01, 02, 03, 04, 07, 08, 09, 10). Pillars 05 (IaC) and 06 (CI/CD) skipped -- no defensible mapping.
