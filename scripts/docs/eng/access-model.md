title: Access model
summary: Inside is a public demo of an intranet. In production it sits behind single sign-on with public, internal and restricted spaces, access granted per person and device, and no network perimeter.
order: 68
labels: inside, security, access, sso, zero-trust
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: explanation
---
Inside, its docs, the service catalog, the status page and the board are open to read on purpose: they show how an intranet for a small company is built. Nothing on this site has a login, and nothing asks for credentials. This page states what is public today and how access works when the same build runs inside a company.

> [!info] Public demo. Every page under `/inside/` is public. Private addresses, host names, e-mail addresses, personal details and employer names are removed before a page is published; the vault import lists each removal in `scripts/docs/IMPORT-REPORT.md`.

## Today

| Content | Who can read it | Why |
|---|---|---|
| Research pages, claims, experiments, the map | Anyone | Published work |
| Inside, docs, services, status, board | Anyone | The demo |
| Grafana public dashboards | Anyone, through a reverse proxy that passes only the shared paths | Aggregates with identifying labels removed; see [Public dashboards](doc:obs/public-dashboards) |
| Internal Grafana dashboards, Prometheus, Loki | The home network only | Raw series and logs |
| Repository write access, the deploy | The owner and the agent sessions, through the [gate](doc:eng/conformity-gate) | A push deploys only after the checks pass |

The Grafana front door is the one place where the production pattern already runs: an allowlist of paths in front of a service, everything else answered with 404.

## In production

The same static build deploys behind an identity-aware proxy. Every request carries a user identity from the company's identity provider and a device check; there is no VPN and no trusted network. This follows the BeyondCorp model: access depends on who the user is and on the state of the device; the network a request comes from grants nothing.

### Spaces

| Class | Examples | Who reads | Who grants |
|---|---|---|---|
| Public | Research pages, published docs, the public status page | Anyone | Nobody; publishing goes through review and the gate |
| Internal | Inside, most docs spaces, the service catalog, the board, internal dashboards | Every employee and contractor, signed in on a managed device | Automatic from the identity provider: joining the company grants it, leaving revokes it |
| Restricted | FinOps with invoices and contracts, security runbooks, incident records that name customers, HR | Named groups | The space owner approves group membership; access is reviewed every quarter |

A space's class sits in its configuration next to its owner, so the build can route each space to the right proxy policy.

### Per user and per device

- **Identity.** Single sign-on through the company's identity provider (SAML or OpenID Connect), with a second factor. Groups come from the identity provider; the intranet keeps no user list of its own.
- **Device.** A managed device with disk encryption, a supported operating system version and screen lock. A device that fails the check gets the public content only.
- **Session.** Short sessions; restricted spaces ask for a fresh sign-in.
- **Lifecycle.** Joiner, mover and leaver events from the HR system change group membership on the same day.
- **Audit.** The proxy logs every request with user, device and path; access to restricted spaces is reviewed with the space owner.

### What changes in the build

- Each docs space and each Inside page carries a class: public, internal or restricted.
- The search index splits by class, so a reader is never offered a page they cannot open.
- The demo banner on every page goes away.
- The deploy target changes. GitHub Pages serves public sites only; an identity-aware proxy needs a host it can sit in front of. This demo stays on GitHub Pages.

## Related

- [Service catalog](doc:eng/service-catalog): who owns each service.
- [Site architecture](doc:eng/site-architecture): where each site is hosted.
