# 03 — Hosts & Roles

## OPNsense g3 — Edge firewall + router

- **Role:** WAN edge, inter-VLAN routing, IDS/IPS, DNS, reverse proxy, Tailscale subnet router + exit node.
- **Hardware:** g3 build (whatever the current CPU/NIC combo is — log it here when next opened up).
- **WAN:** `igb0` — DHCP (or static if ISP supports).
- **LAN:** `igb1` — 802.1Q trunk to SG105E P1, all VLANs tagged, v10 native.
- **Plugins / packages:**
  - **AdGuard Home** (DNS resolver + ad/tracker block + split-horizon for `d2.lol`)
  - **Tailscale** (subnet router advertising `10.10.0.0/16`, exit node enabled)
  - **WireGuard server** (remote admin tunnel for emergencies if Tailscale is down)
  - **HAProxy** (reverse proxy for `*.d2.lol` LAN services)
  - **Suricata** (IDS on WAN)
  - **Zenarmor** + **ntopng** (flow / app monitoring)
  - **acme.sh** (Cloudflare DNS-01 wildcard cert for `*.d2.lol`)

## MHV — Main hypervisor (Proxmox VE)

- **NICs:**
  - `eno1` 1G  →  MGMT v10 (`10.10.10.10`); IPMI shares this VLAN at `.110`.
  - `enp1s0f0` 10G  →  WAN failover / direct test link to OPNsense.
  - `enp1s0f1` 10G  →  LAN trunk (v10/20/30/50/60 tagged); Linux bridges `vmbr10/20/30/50/60`.
- **Bridges:** one Linux bridge per VLAN, all rooted on `enp1s0f1.X` sub-interfaces.
- **Cluster:** standalone for now; NUC i5 + G4 Mini join later as voting members.
- **Storage:** local NVMe for fast VMs + NFS mount from the i3 NAS for bulk VM disks.
- **Workloads (LXC + VM):**
  - AdGuard Home secondary
  - **Gluetun-VPN-CT** (torrent egress, see [`05-vpn-torrent.md`](05-vpn-torrent.md))
  - Sonarr / Radarr / Prowlarr / qBittorrent (qBit bound to `tun0` only)
  - Uptime Kuma, Grafana + Prometheus, Loki
  - Tailscale containerized exit-only client
  - Dev / sandbox VMs (treat anything experimental as a v50 TEST guest)

## Main Media Server

- **Role:** Plex / Jellyfin + media transcode.
- **VLAN:** v20 — `10.10.20.11` — `plex.d2.lol`.
- **IPMI:** v10 — `10.10.10.111`.
- **Storage:** NFS to NAS at `nas.d2.lol:/mnt/tank/media`; library scan triggered post-import by Sonarr/Radarr.
- **NIC plan:** 1 GbE today; bump to 10G NIC once 10G core lands.

## NUC i5 build

- **Role:** Proxmox node — quorum + lite VMs (HomeAssistant, dashboards, light services).
- **VLAN:** v20 — `10.10.20.12` — `nuc.d2.lol`.
- **NIC:** 1 GbE.

## G4 Mini

- **Role:** Proxmox node — edge services (low-power: Pi-hole secondary, MQTT, small bots).
- **VLAN:** v20 — `10.10.20.13` — `g4.d2.lol`.
- **NIC:** 1 GbE.

## i3 NAS build

- **Role:** Bulk storage, ZFS, NFS/SMB/iSCSI.
- **OS:** TrueNAS Scale or Unraid.
- **VLAN:** v20 — `10.10.20.20` — `nas.d2.lol`.
- **Datasets (suggested):**
  - `tank/media` — Plex library, exported NFS to media server.
  - `tank/proxmox` — VM/CT disk store (NFS to MHV).
  - `tank/backups` — Proxmox backups + restic destination.
  - `tank/scratch` — temp / downloads landing pad (snapshots disabled).
- **NIC plan:** 1 GbE today; 10G after core lands.

## WGR — Windows Gaming Rig

- **VLAN:** v20 — `10.10.20.50` — `wgr.d2.lol`.
- **Tailscale:** native client; no exit-node route by default.
- **Reaches:** NAS via SMB, Plex via LAN; can RDP from tailnet if needed.

## TV / Hue Bridge

- **VLAN:** v30 IoT.
- **Reachability:** **no inbound** to v10/v20; HomeAssistant on v20 reaches the Hue API outbound to v30 via a single allow rule.

## Guest devices

- **VLAN:** v40.
- **Internet only.** No mDNS/SSDP leak between v40 and other VLANs.

## Test / sandbox guests

- **VLAN:** v50.
- **Routed by:** hEX RB750Gr3 (so blowing it up doesn't take OPNsense with it).
- See [`07-test-vlan.md`](07-test-vlan.md).
