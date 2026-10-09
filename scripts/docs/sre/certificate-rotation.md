title: Certificate Rotation
summary: Replace TLS certificates before expiry.
parent: runbooks
order: 100
labels: runbook, security, tls
aliases: TLS Cert Rotation | Certificate Expiry Response
type: runbook
created: 2026-04-25
updated: 2026-06-08
origin: SRE/runbooks/Certificate Rotation.md
reviewed: no
---
> Replace TLS certificates before expiry. Certificate-driven outages are entirely predictable, which makes them the most embarrassing kind. Automation is the right answer; this runbook is the manual fallback.

## Trigger

- Certificate expiry within 14 days (proactive)
- Certificate expiry within 24 hours (urgent)
- Expired certificate in production (emergency, see "Already expired" section)
- Compromised certificate (security event — different procedure, see [[Credential Rotation]])
- CA migration (planned)

## Prerequisites

- [ ] Inventory of all certificates owned by the team or service
- [ ] Access to the certificate management tool (cert-manager, ACM, Let's Encrypt account, internal PKI)
- [ ] Access to all places the certificate is consumed (load balancers, services, clients with pinning, mobile apps with pinning)
- [ ] Knowledge of which certificates are pinned (mobile apps, IoT devices, hardcoded clients)
- [ ] Certificate transparency monitoring confirmed working

## Steps

1. **Inventory the certificate's deployment surface.** Where is this exact certificate installed? Common locations: load balancer (cloud or NGINX), service mesh (Istio, Linkerd), reverse proxy, application TLS termination, internal service-to-service mTLS, mobile app pinning configuration, IoT device firmware. **Pinning is the trap.** A pinned cert cannot be rotated without a coordinated client update.
2. **Issue the new certificate.** Tool-specific:
   - cert-manager: ensure issuer is healthy, request renewal, watch certificate resource for "Ready"
   - ACM: request public certificate, complete domain validation, wait for ISSUED status
   - Let's Encrypt direct: `certbot renew --dry-run` first, then real run
   - Internal PKI: submit CSR with correct SAN list, retrieve issued cert
3. **Validate the new certificate.** Before deploying:
   - `openssl x509 -in cert.pem -text -noout` — verify dates, SANs, key usage
   - Check the SAN list includes every hostname currently served
   - Verify the chain (`openssl verify -CAfile chain.pem cert.pem`)
   - Confirm the private key matches (`openssl rsa -in key.pem -modulus -noout` matches `openssl x509 -in cert.pem -modulus -noout`)
4. **Deploy in a test environment first.** Even for "simple" rotations. The test catches misconfigured chains, missing intermediate certs, and SAN mismatches before they hit production.
5. **Deploy to production.** Method depends on the consumer:
   - Load balancer: hot-swap is usually safe (LB serves new cert on next handshake)
   - Service mesh: rolling update of the secret, watch for mTLS handshake errors during cutover
   - Application TLS termination: rolling restart of the application
   - Pinned clients: coordinated client release first, then cert rotation
6. **Verify externally.** Multiple methods:
   - Browser inspect: certificate details show new expiry
   - `openssl s_client -connect host:port -servername host < /dev/null` — from outside the network
   - Online tools: SSL Labs, hardenize, or your CT log monitor
7. **Update monitoring.** New certificate fingerprint goes into the monitoring system. Old certificate alerts should now silence (because the cert is replaced).
8. **Update documentation.** Certificate inventory, expiry tracker, runbook reference (last-rotated date).

## Verification

- All consumers show the new certificate fingerprint
- No TLS handshake errors in service logs since rotation
- Cert expiry alerts cleared
- External monitoring (SSL Labs etc.) reports healthy
- Pinning-affected clients (if any) received the coordinated update

## Rollback

If the new certificate fails (chain issue, wrong SAN, etc.), reinstall the old one ONLY if the old one is not yet expired. If the old one is expired, you cannot rollback; you must forward-fix.

This is why prerequisite verification (step 3) is non-negotiable.

## Already expired (emergency)

If you are reading this because production is down due to expired cert:

1. **Stop reading the proactive sections.** Issue the cert now.
2. **Skip non-critical SANs if it speeds issuance.** A cert with the primary domain is better than no cert.
3. **Deploy to the most critical consumer first.** Load balancer over service mesh, public over internal.
4. **Communicate as if it is a Sev-1 outage.** It is.
5. **Postmortem must include**: why the cert expiry was not caught, what monitoring failed, how renewal automation will be installed.

## Automation is the destination

Manual rotation should be the rare event. Goal state:

- cert-manager (or equivalent) handles all internal certs
- ACM/Let's Encrypt handle all public-facing certs
- Hardware/IoT/mobile pinning is justified per case and documented with rotation plan
- Cert-expiry monitoring pages 30 days, 14 days, 7 days, 24 hours
- Rotation drill runs at least quarterly to catch tooling rot

## Escalation

| Tier | Trigger |
|---|---|
| Security on-call | Compromised cert (different procedure, see [[Credential Rotation]]) |
| Mobile/client team | Pinning blocks rotation |
| External CA (paid support) | Issuance fails on the CA side |
| Incident commander | Production already impacted by expiry |

## Regulatory and control mappings

- [[ISO 27001 Annex A.8 Technological Controls]] A.8.24 Use of cryptography. A.5.17 Authentication information lifecycle.
- [[NIS2 Security Measures]] Art 21(h) cryptography policies and procedures.
- [[DORA ICT Risk Management]] Art 9 protection (cryptography for confidentiality and integrity).
- [[GDPR Controller and Processor]] Art 32 security of processing (encryption in transit).
- [[PCI DSS Twelve Requirements and Compliance]] Req 4 (strong cryptography in transit) + Req 3 (encryption at rest).

## See also

[[Credential Rotation]] · [[Service Outage Response]] · [[08-security]] · [[10-toil-reduction]] · [[ISO 27001 Annex A.8 Technological Controls]] · [[NIS2 Security Measures]] · [[README]] (runbooks)
