title: Credential Rotation
summary: Replace secrets used by services and humans.
parent: runbooks
order: 100
labels: runbook, secrets, security
aliases: Secrets Rotation | Credential Rollover
type: runbook
created: 2026-04-25
updated: 2026-06-08
origin: SRE/runbooks/Credential Rotation.md
reviewed: no
---
> Replace secrets used by services and humans. Distinguish between scheduled rotation (low pressure) and compromise rotation (Sev-1). The procedure is similar; the speed and blast radius are not.

## Trigger

| Event | Severity | Time pressure |
|---|---|---|
| Scheduled rotation per policy | Low | Days |
| Employee departure | Medium | Same business day |
| Suspected compromise | High | Hours |
| Confirmed leak (in commit, log, screenshot) | Sev-1 | Minutes |
| Vendor-side breach (provider notifies you) | High | Hours |
| Audit finding requiring rotation | Medium | Per audit deadline |

## Prerequisites

- [ ] Inventory of where this credential is used (services, humans, third-party integrations)
- [ ] Access to the secret management system (Vault, AWS SM, GCP SM, Azure KV, 1Password Connect, etc.)
- [ ] Permission to rotate at the source-of-truth system (the IdP, the API provider, the database admin)
- [ ] Knowledge of the credential's TTL and rotation pattern (some secrets need overlap, some don't)
- [ ] Rollback escape hatch (break-glass access path that does not depend on this credential)

## Steps

1. **Generate the new credential at the source.** API provider, IdP, database — wherever the credential is authoritative. Confirm the new credential works (test call, login, or explicit verification step in the provider's UI).
2. **Decide on overlap window.** Two patterns:
   - **Atomic swap** (preferred when supported): old credential becomes invalid the moment the new one is created. Required for compromise rotation.
   - **Overlap window** (when atomic is unsafe): old credential remains valid for N hours/days while consumers cut over. Required when consumers cannot all be updated simultaneously.
3. **Push the new credential to the secret store.** Update the secret in Vault/AWS SM/etc. Tag with rotation timestamp and rotation reason. If the system supports versioning, increment the version explicitly.
4. **Trigger consumer reload.** Services using the secret must reload. Methods:
   - Vault Agent / external-secrets-operator: automatic reload via watcher
   - Manual injection: rolling restart of the service
   - Init-only consumers: rolling restart required, no other option
   - Human users: notify them and confirm they updated their local cache (1Password, ~/.aws/credentials, etc.)
5. **Verify consumers now use the new credential.** Tail provider-side logs for auth events; the new credential should be authenticating, the old one should not. If both are authenticating after the overlap window, you have a missed consumer; find it.
6. **Invalidate the old credential at the source.** Once consumers are confirmed cut over, revoke the old credential at the provider. **This is the actual rotation moment** in the overlap-window pattern. Atomic swap pattern revoked it in step 1.
7. **Verify failed authentication for the old credential.** Test that the old credential now fails. If it still works, you did not actually revoke it; find out why before declaring done.
8. **Audit trail.** Log: who rotated, when, why, what credential, what services were affected, what overlap pattern was used. This goes into the security audit log, not into the secret itself.
9. **Update inventory.** New rotation timestamp, next scheduled rotation date.

## Verification

- Provider-side audit log shows new credential in use, old credential revoked
- All consumer services authenticated with new credential successfully
- Old credential fails authentication when tested
- No service errors correlated with the rotation timestamp
- Secret store reflects the new value

## Rollback

If rotation breaks consumers and the old credential is still valid (overlap window pattern), revert the secret store to the old value and resume operations. Open a defect on the consumer that broke.

If the old credential is already revoked (atomic swap), you cannot rollback. Forward-fix only:
- Identify the broken consumer
- Provision a temporary credential (different scope, time-limited) for that consumer
- Repeat the rotation cleanly

This is why overlap windows are the default for non-compromise rotations.

## Compromise rotation specifics

When you suspect or confirm compromise, the rules change:

- **No overlap.** Atomic swap. The compromised credential must be invalid immediately.
- **All credentials with the same scope.** If one DB password leaked, rotate the other DB passwords on adjacent services if they could plausibly be the same or guessable.
- **Hunt for usage.** Provider audit logs since the suspected leak time. Identify any unexpected source IPs, user agents, or query patterns.
- **Document the blast radius.** What did this credential have access to? Did the attacker exfiltrate? Coordinate with security incident response.
- **Sev-1 communication.** Incident channel, not a quiet rotation. The disclosure timeline matters legally and reputationally.

## Service account hygiene

Most rotation pain comes from credentials shared across many consumers. Avoid the pain at design time:

- One credential per consumer where possible (rotation blast radius = one consumer)
- Short-lived credentials (token rotation as the default, minutes to hours TTL)
- Workload identity (cloud-provider IAM) over static keys wherever supported
- Personal credentials NEVER shared; use service accounts for shared access

Long-lived shared credentials are the maintenance debt that compound interest on every rotation.

## Escalation

| Tier | Trigger |
|---|---|
| Security on-call | Suspected or confirmed compromise |
| Engineering manager | Rotation breaks production |
| Compliance officer | Rotation crossed an audit boundary |
| Legal | Compromise involved customer data |

## Regulatory and control mappings

- [[ISO 27001 Annex A.5 Organizational Controls]] A.5.16 Identity management. A.5.17 Authentication information. A.5.18 Access rights.
- [[ISO 27001 Annex A.8 Technological Controls]] A.8.2 Privileged access rights. A.8.5 Secure authentication. A.8.18 Use of privileged utility programs.
- [[NIS2 Security Measures]] Art 21(i) HR security, access control, asset management. Art 21(j) MFA + secured comms.
- [[DORA ICT Risk Management]] Art 9 access control.
- [[GDPR Controller and Processor]] Art 32 security of processing.
- [[PCI DSS Twelve Requirements and Compliance]] Req 7 (least privilege), Req 8 (identify + authenticate), Req 3 (key management).

## See also

[[Certificate Rotation]] · [[Service Outage Response]] · [[08-security]] · [[10-toil-reduction]] · [[ISO 27001 Annex A.5 Organizational Controls]] · [[NIS2 Security Measures]] · [[README]] (runbooks)
