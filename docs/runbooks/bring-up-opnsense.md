# Runbook — Bring up OPNsense

Target state: OPNsense g3 build serving as edge router/firewall with all 6 VLANs, AdGuard Home, Tailscale subnet+exit node, and HAProxy reverse proxy on `*.d2.lol`.

## 1. Install

- USB installer → ZFS root, single disk fine for now.
- During install set:
  - WAN = `igb0` (DHCP)
  - LAN = `igb1` (`10.10.10.1/24`)
- Reboot, log in to `https://10.10.10.1` from a laptop on `eno1`/SG105E P3 (temporarily access v10).

## 2. VLANs

**Interfaces → Other Types → VLAN** — add for each:

| Tag | Parent | Description |
|---|---|---|
| 10 | `igb1` | MGMT |
| 20 | `igb1` | LAN |
| 30 | `igb1` | IoT |
| 40 | `igb1` | GUEST |
| 50 | `igb1` | TEST |
| 60 | `igb1` | VPN |

**Interfaces → Assignments** — map each VLAN to a logical interface (`vlan10`, `vlan20`, …). Enable each, set IPv4 = static, address `.1`, mask `/24`.

**Services → DHCPv4** — enable on v20/v30/v40/v50; set ranges per [`01-ip-plan.md`](../01-ip-plan.md).

## 3. Firewall rules (per interface)

Apply the matrix from [`01-ip-plan.md`](../01-ip-plan.md). At minimum on each non-MGMT interface:

1. Allow `<This Interface net>` → `<This Interface address>` UDP 53/853 (DNS).
2. Allow `<This Interface net>` → `Internet` (any) — except where the matrix says no.
3. Block `<This Interface net>` → `RFC1918`.

Floating rules: block all `RFC1918`-to-`RFC1918` by default; the per-interface allows above are the exceptions.

## 4. AdGuard Home

- **Plugins:** `os-adguardhome` (community) — install + enable.
- Listen on `10.10.10.1:53` (and the `.1` of every other VLAN).
- Upstream: `https://1.1.1.1/dns-query`, `https://9.9.9.9/dns-query` (DoH).
- Add the [d2.lol split-horizon overrides](../06-dns.md).

## 5. Tailscale

- **Plugins:** `os-tailscale` — install + enable.
- `tailscale up --advertise-routes=10.10.0.0/16 --advertise-exit-node --accept-dns=false`
- In the Tailscale admin → enable subnet routes + exit node for this device.
- Apply ACLs from [`04-tailscale.md`](../04-tailscale.md).

## 6. HAProxy + acme.sh

- **Plugins:** `os-haproxy`, `os-acme-client`.
- Configure `acme.sh` with Cloudflare API token; issue `*.d2.lol`.
- HAProxy frontends: 80 (redirect to 443) and 443 (SNI routing). Backends per [`06-dns.md`](../06-dns.md).

## 7. Monitoring

- Suricata on WAN (igb0): IDS mode initially, IPS once you've tuned signatures.
- Zenarmor + ntopng — light app/flow visibility.

## 8. Smoke test

- [ ] From a v20 host: `dig plex.d2.lol @10.10.20.1` → `10.10.20.11`
- [ ] From a v40 guest: cannot reach `10.10.20.20`
- [ ] From v60 host with `tun0` down: cannot reach `1.1.1.1`
- [ ] Tailscale: phone off-LAN reaches `nas.d2.lol`
- [ ] `https://plex.d2.lol` shows valid LE cert
