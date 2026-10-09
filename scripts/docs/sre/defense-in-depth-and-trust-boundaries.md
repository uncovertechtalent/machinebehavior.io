title: Defense in Depth and Trust Boundaries
summary: No single security control holds against a determined adversary.
parent: security
order: 100
labels: concept, security, threat-modeling
aliases: Defense in Depth | Trust Boundary | Layered Security
type: concept
created: 2026-05-04
updated: 2026-05-04
origin: SRE/pillars/08-security/Defense in Depth and Trust Boundaries.md
reviewed: no
---
> No single security control holds against a determined adversary. Defense in depth assumes each layer will eventually fail and arranges them so that breaching one layer does not deliver the kingdom. The discipline lives in **identifying where trust changes**, because that is where controls go.

## A trust boundary is where data crosses jurisdictions

Trust boundaries are the points in your system where data, code, or identity crosses from one trust domain to another:

- Internet → load balancer (untrusted → DMZ)
- API gateway → service (DMZ → application)
- Service → database (application → data)
- Pod → pod across namespace (tenant → tenant)
- Developer laptop → CI runner (developer → build)
- CI runner → production (build → runtime)

Every boundary is a place where authentication, authorization, validation, and rate-limiting must happen. **Controls that only exist far from the boundary do not protect the boundary.** Input validation in the database layer does not save you from SQL injection at the API layer.

## The layers (illustrative, request path)

A request from the internet to a database row crosses many layers. Each must hold *independently*:

| Layer | Control | Failure if absent |
|---|---|---|
| Edge | WAF, DDoS scrubbing, TLS termination | Volumetric attacks, plaintext on the wire |
| Network | VPC, security groups, private subnets | Lateral movement after one host falls |
| Identity | OAuth/OIDC, mTLS, service accounts | Caller identity unverifiable |
| Application | Authn middleware, input validation, output encoding | Auth bypass, injection, XSS |
| Data | Row-level security, column encryption, query auditing | Bulk exfiltration after app compromise |
| Secret | Vault/KMS, rotation, scoped access | One leaked credential = full access |
| Audit | Centralized, write-once logs | Compromise without detection |

The test: **if you assume layer N is bypassed, do the remaining layers contain the blast radius?** If the answer is no for any layer, defense-in-depth is incomplete.

## The principle of least privilege is the lever

Trust boundaries imply credentials. Credentials imply scope. The discipline is to grant the **minimum scope needed for the work**, scoped to **the shortest viable lifetime**, and **audited at every use**.

- A CI job needs deploy permission to one cluster, not all clusters.
- A service account needs read on one table, not all tables.
- A developer needs prod read for one debug session, not standing prod write.
- A vendor integration needs one API endpoint, not the API key for everything.

Standing access is the enemy. Ephemeral, scoped, audited credentials are the goal.

## Shift-left is a layer, not the strategy

Catching vulnerabilities in the developer's editor (SAST), in CI (SCA, secret scan), and in the registry (image scan) is cheaper than catching them in production. But shift-left does not replace runtime defenses — it complements them. A shift-left-only posture assumes:

- The build is the only path to production. (Direct console-edits exist.)
- The scanners catch the bug. (Zero-days don't appear in scanners.)
- The fix lands before the next compromise. (Vulnerable windows exist.)

Runtime defenses (network policy, runtime threat detection, audit logging) are what catch what shift-left missed.

## Where this fails in practice

- **Boundary identified, control attached at the wrong layer.** "We do auth at the API gateway" is fine until a service-to-service call inside the cluster bypasses it.
- **One layer doing the work of many.** WAF as the only injection defense; SG as the only auth.
- **Defense in breadth, not depth.** Twenty controls all at one layer, none at the others.
- **Auditing after the fact.** Logs are evidence, not prevention. They count toward defense in depth only if they are reviewed.

## See also

[[Probing Microarchitecture for Vulnerability Discovery]] · [[Credential Rotation]] · [[Certificate Rotation]] · [[05-infrastructure-as-code]]
