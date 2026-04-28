# 01 — VLAN & IP Plan

Master subnet plan for d2lab. All VLANs are L3-routed by **OPNsense** (`10.10.X.1` is always the gateway). The MikroTik hEX takes over routing for VLAN 50 (test) when used standalone.

## Address scheme

Use the 2nd octet `10` to mark "this is d2lab" so it's distinct from work and ISP-default `192.168.x` ranges.

| VLAN | Name | Subnet | Gateway | DHCP range | Purpose |
|---:|---|---|---|---|---|
| 10 | MGMT | `10.10.10.0/24` | `.1` | static-only | Proxmox `eno1`, IPMI/BMC, switch admin, OPNsense mgmt |
| 20 | LAN | `10.10.20.0/24` | `.1` | `.150–.250` | Servers, NAS, gaming rig, *arr stack consumers |
| 30 | IoT | `10.10.30.0/24` | `.1` | `.50–.250` | TV, Hue Bridge, smart plugs — no LAN reach |
| 40 | GUEST | `10.10.40.0/24` | `.1` | `.100–.200` | Visitor SSID — internet only, fully isolated |
| 50 | TEST | `10.10.50.0/24` | `.1` | `.50–.200` | Sandbox / break-things lab routed via hEX |
| 60 | VPN | `10.10.60.0/24` | `.1` | static-only | Gluetun torrent egress — policy-routed, kill-switched |
| — | TS overlay | `100.64.0.0/10` | — | (Tailscale CGNAT) | Tailscale mesh — MagicDNS + split-horizon `d2.lol` |

> The `10.10.0.0/16` supernet is what OPNsense advertises into Tailscale, so a single subnet route covers all home traffic from any tailnet client.

## Static host assignments

(VLAN 20 unless otherwise noted — see [`03-hosts.md`](03-hosts.md) for full host details.)

| Host | VLAN(s) | IP(s) | DNS (`d2.lol`) | Notes |
|---|---|---|---|---|
| OPNsense g3 | 10/20/30/40/50/60 trunk | all `.1` + ISP WAN | `fw.d2.lol` | Edge FW, Tailscale exit, AdGuard |
| TP-Link SG105E | 10 mgmt | `10.10.10.2` | `sw1.d2.lol` | Easy-Smart, 802.1Q trunks |
| MikroTik hEX RB750Gr3 | 10 mgmt + 30/40/50 | `10.10.10.3` | `hex.d2.lol` | Test-net router, IoT/Guest gw |
| Future 10G core sw | 10 mgmt | `10.10.10.4` | `sw10g.d2.lol` | CRS305/CRS309 or QSW-M2108 |
| MHV (Proxmox) | 10 + 20 + IPMI | `eno1 .10`  •  `enp1s0f1 .10`  •  `IPMI .110` | `mhv.d2.lol` | X540 dual 10G, eno1 mgmt |
| Main Media Server | 20 (IPMI on 10) | `10.10.20.11`  •  IPMI `.111` | `plex.d2.lol` | Plex/Jellyfin + *arr |
| NUC i5 | 20 | `10.10.20.12` | `nuc.d2.lol` | Proxmox node, quorum |
| G4 Mini | 20 | `10.10.20.13` | `g4.d2.lol` | Proxmox node, edge svcs |
| i3 NAS Build | 20 | `10.10.20.20` | `nas.d2.lol` | TrueNAS/Unraid, ZFS |
| WGR (Windows) | 20 | `10.10.20.50` | `wgr.d2.lol` | Tailscale client |
| TV / Hue Bridge | 30 | `10.10.30.30 / .31` | — | IoT — no v10/v20 reach |
| Visitor SSID pool | 40 | `10.10.40.100–.200` DHCP | — | Captive portal optional |
| Gluetun-VPN-CT | 60 | `10.10.60.60` | `vpn-ct.d2.lol` | LXC on MHV, kill-switched |

## Inter-VLAN policy (high level)

| Source ↓ \ Dest → | v10 MGMT | v20 LAN | v30 IoT | v40 Guest | v50 TEST | v60 VPN | Internet |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **v10 MGMT** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **v20 LAN** | ✗ (Tailscale `tag:admin` only) | ✓ | ✓ (Hue API) | ✗ | ✓ | ✗ | ✓ |
| **v30 IoT** | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✓ (allowlist optional) |
| **v40 Guest** | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | ✓ |
| **v50 TEST** | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✓ |
| **v60 VPN** | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | only via tun0 (kill-switch) |

Edit the matrix in OPNsense → **Firewall → Rules** per interface.

## Reserved blocks (don't squat)

- `10.10.99.0/24` reserved for a future **DMZ / public-facing** segment.
- `10.10.200.0/24` reserved for a future **storage-only** VLAN (NFS/iSCSI on the 10G core).
