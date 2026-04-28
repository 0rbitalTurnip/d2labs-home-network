# 06 — DNS & d2.lol

## Public zone — Cloudflare

- Registrar / DNS: **Cloudflare** for `d2.lol`.
- Public records resolve only what you choose to expose:
  - `@` / `www` → Cloudflare Pages or a static landing
  - selected services via **Cloudflare Tunnel** (`*.d2.lol` → tunnel → HAProxy on OPNsense)
- API token (zone-scoped, **DNS:Edit** only) is used by `acme.sh` for DNS-01.

## Internal split-horizon — AdGuard Home on OPNsense

AdGuard Home is the LAN resolver. It overrides selected `*.d2.lol` names to LAN IPs so the same DNS works locally and remotely (over Tailscale).

| Hostname | LAN IP | Public? |
|---|---|---|
| `fw.d2.lol` | `10.10.10.1` | no |
| `mhv.d2.lol` | `10.10.20.10` | no |
| `nuc.d2.lol` | `10.10.20.12` | no |
| `g4.d2.lol` | `10.10.20.13` | no |
| `nas.d2.lol` | `10.10.20.20` | no |
| `plex.d2.lol` | `10.10.20.11` | optional via Cloudflare Tunnel |
| `wgr.d2.lol` | `10.10.20.50` | no |
| `hex.d2.lol` | `10.10.10.3` | no |
| `sw1.d2.lol` | `10.10.10.2` | no |
| `sw10g.d2.lol` | `10.10.10.4` | no |
| `vpn-ct.d2.lol` | `10.10.60.60` | no |

## DHCP integration

In OPNsense, enable **Register DHCP leases in DNS resolver** so dynamic VLAN 20 hosts get auto-registered as `<hostname>.d2.lol`. Static reservations above always win.

## TLS — wildcard cert for `*.d2.lol`

`acme.sh` running on OPNsense fetches a Let's Encrypt wildcard cert via Cloudflare DNS-01 every 60 days:

```bash
acme.sh --issue --dns dns_cf -d 'd2.lol' -d '*.d2.lol' \
        --keylength ec-256 --server letsencrypt
```

Required env:

```bash
export CF_Token="cloudflare-zone-edit-token"
export CF_Account_ID="..."
export CF_Zone_ID="..."
```

Cert is then loaded by **HAProxy** (and pushed to other services that need it via a small post-renew hook).

## HAProxy reverse proxy

HAProxy on OPNsense terminates TLS and routes by SNI:

| Hostname | Backend |
|---|---|
| `plex.d2.lol` | `10.10.20.11:32400` |
| `nas.d2.lol` | `10.10.20.20:443` |
| `mhv.d2.lol` | `10.10.20.10:8006` |
| `grafana.d2.lol` | LXC on MHV |
| `uptime.d2.lol` | LXC on MHV |

Anything not listed → `404` so unknown hostnames don't probe internal services.

## Tailscale MagicDNS

MagicDNS gives every node a `*.tail-XXXX.ts.net` name automatically. The split-horizon `*.d2.lol` records resolve to **LAN IPs that are routable through the Tailscale subnet route** — so `plex.d2.lol` works from a coffee shop without touching the public DNS at all.
