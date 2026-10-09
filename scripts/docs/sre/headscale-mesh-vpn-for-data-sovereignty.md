title: Headscale Mesh VPN for Data Sovereignty
summary: Self-hosted open-source Tailscale control plane with embedded DERP relay.
parent: tools
order: 100
labels: data-sovereignty, gdpr, networking, tool, vpn
aliases: Headscale | Self-hosted Tailscale
type: tool
created: 2026-04-25
updated: 2026-06-08
origin: SRE/tools/Headscale Mesh VPN for Data Sovereignty.md
reviewed: no
---
> Self-hosted open-source Tailscale control plane with embedded DERP relay. Single Go binary, SQLite backing store, runs on a Raspberry Pi. Gives you a WireGuard-based mesh VPN fully under EU jurisdiction, no US SaaS metadata leakage.

## Why self-host the control plane

Tailscale's managed control plane runs on AWS in US regions. Even though it only handles public keys and node metadata (no traffic data, which is P2P WireGuard), that metadata is personal data under GDPR: who connects when, from where, to what. Tailscale does not offer EU-only control plane hosting.

Headscale is the drop-in self-hosted alternative. You own the coordination server. Run it in `eu-central-1`, Hetzner Falkenstein, or on your own hardware. Add `OmitDefaultRegions: true` and run your own DERP relays, you get a fully EU-contained deployment. Clients are standard Tailscale clients, just pointed at your Headscale instance instead of `controlplane.tailscale.com`.

## Hardware and prerequisites

Headscale is extremely lightweight. A Raspberry Pi 4, a small NUC, or a EUR 4/month Hetzner CX22 VPS handles a home tailnet without breaking a sweat. Single Go binary, SQLite, negligible RAM.

Prerequisites:

- A domain name you control (for TLS certs)
- DNS A record or DDNS pointing at the Headscale host
- Router ports open on the host: TCP 443 (HTTPS + embedded DERP), UDP 3478 (STUN), TCP 80 (ACME HTTP-01 challenge)
- A Linux host, Debian or Ubuntu for least friction

## Minimal config

Install the `.deb`, config lives at `/etc/headscale/config.yaml`. Key sections:

```yaml
server_url: https://hs.yourdomain.com
listen_addr: 0.0.0.0:443

tls_letsencrypt_hostname: hs.yourdomain.com
tls_letsencrypt_listen: :80
tls_letsencrypt_challenge_type: HTTP-01

prefixes:
  v4: 100.64.0.0/10
  v6: fd7a:115c:a1e0::/48

derp:
  server:
    enabled: true
    region_id: 999
    region_code: home
    stun_listen_addr: 0.0.0.0:3478
    automatically_add_embedded_derp_region: true
  urls: []   # disable Tailscale's default DERP map for full isolation

database:
  type: sqlite
  sqlite:
    path: /var/lib/headscale/db.sqlite

dns:
  magic_dns: true
  base_domain: tail.yourdomain.com
```

Create a user, start the service:

```bash
sudo systemctl enable --now headscale
headscale users create stefan
```

## Node registration

Two paths. Manual (no OIDC): client runs `tailscale up --login-server https://hs.yourdomain.com`, prints a node key, operator runs `headscale nodes register --user stefan --key nodekey:...` on the server.

OIDC: wire in Authelia, Authentik, Keycloak, or Google Workspace. Clients authenticate via browser login, same UX as managed Tailscale.

```yaml
oidc:
  issuer: https://auth.yourdomain.com
  client_id: headscale
  client_secret: your-secret
  scope: [openid, profile, email]
  allowed_users:
    - [e-mail]
```

## ACLs as code

Policy file at `/etc/headscale/acl.json`, same format as Tailscale. Version-controllable in Git.

```json
{
  "acls": [
    {"action": "accept", "src": ["stefan"], "dst": ["*:*"]}
  ],
  "ssh": [
    {"action": "accept", "src": ["stefan"], "dst": ["tag:server"], "users": ["root", "stefan"]}
  ]
}
```

## DERP: why it exists

DERP is Designated Encrypted Relay for Packets, Tailscale's HTTPS-based relay for when direct P2P fails. Both peers maintain a persistent outbound HTTPS connection to their home DERP server. When A cannot reach B directly (double-NAT, CGNAT, symmetric NAT, restrictive hotel wifi), A sends the WireGuard-encrypted packet to DERP over HTTPS, DERP forwards to B.

HTTPS-based because anywhere you can load a website, you can run DERP. Corporate proxies, hotel captive portals, airport wifi, all traversable. The relay sees opaque encrypted blobs only. Tailscale keeps trying NAT traversal in the background and transparently upgrades to direct P2P the moment it succeeds.

Trade-off: TCP-over-TCP adds latency and head-of-line blocking under packet loss. Fallback only.

## Vodafone CGNAT pattern

German Vodafone consumer connections are typically DS-Lite / CGNAT with no real public IPv4. You cannot open ingress on the home side. Standard workaround: run Headscale + embedded DERP on a EUR 4/month Hetzner VPS in Falkenstein. Both home and roaming clients make outbound-only connections to the VPS for control plane registration and DERP relay. Direct P2P still happens whenever NAT traversal succeeds.

## Validation checklist

Minimum smoke tests after setup:

1. `tailscale ping <other-node>` reports `via <ip>:<port>` (direct P2P), not `via DERP`
2. From a mobile network where NAT traversal fails, traffic falls back to your embedded DERP
3. `tailscale up --advertise-routes=[private IP]` exposes home LAN, reachable from other tailnet nodes after `headscale routes enable`
4. Exit-node routing works from a roaming client
5. MagicDNS resolves `hostname.tail.yourdomain.com`
6. Prometheus metrics scrape from `metrics_listen_addr`

## What Headscale does not have

No Funnel (public edge exposure), limited Tailscale SSH session recording, no network flow logs, no device posture checks, no auto-approved routes, no polished admin web UI (headscale-ui is a community project). For a homelab or a data-sovereignty play, none of those matter.

## Regulatory and control mappings

- [[ISO 27001 Annex A.5 Organizational Controls]] A.5.14 Information transfer.
- [[ISO 27001 Annex A.8 Technological Controls]] A.8.20 Networks security. A.8.21 Security of network services. A.8.22 Segregation of networks. A.8.24 Use of cryptography.
- [[GDPR Cross-Border Transfers]] — VPN supports architectural elimination of cross-border data flow.
- [[Compliance Domain Architecture]] — VPN as boundary technology between domains.

## See also
[[Memory Architecture L0-L4]] · [[OpenCode Self-Hosted LLM Configuration]] · [[Apple Silicon vs Desktop GPU for Inference]] · [[Personal Digital Twin Architecture]] · [[Compliance Domain Architecture]] · [[ISO 27001 Annex A.8 Technological Controls]]
