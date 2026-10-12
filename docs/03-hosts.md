# 03 — Hosts & Roles

Reconciled 2026-10-11 with the physical inventory (`docs/inventory.md`).
Build assignments are final; hostnames below are the Ansible names.

## edge-01 — OPNsense (G3 SFF)

- **Role:** WAN edge, inter-VLAN routing, IDS/IPS, DNS, reverse proxy, Tailscale subnet router + exit node.
- **Hardware:** HP ProDesk 600 G3 SFF (i5-7500, 16GB) + Supermicro AOC-SG-i4 quad-port GbE.
- **WAN:** `igb0` — DHCP (or static if ISP supports).
- **LAN:** `igb1` — 802.1Q trunk to the switch, all VLANs tagged, v10 native.
- **Plugins / packages:**
  - **AdGuard Home** (DNS resolver + ad/tracker block + split-horizon for `d2.lol`)
  - **Tailscale** (subnet router advertising `10.10.0.0/16`, exit node enabled)
  - **WireGuard server** (remote admin tunnel for emergencies if Tailscale is down)
  - **HAProxy** (reverse proxy for `*.d2.lol` LAN services)
  - **Suricata** (IDS on WAN)
  - **Zenarmor** + **ntopng** (flow / app monitoring)
  - **acme.sh** (Cloudflare DNS-01 wildcard cert for `*.d2.lol`)
- **Undo:** XML config backup to NAS + git after every change.

## ai-box — AI + gaming (Ubuntu 24.04)

- **Role:** Local AI inference (Strata) + gaming + game streaming.
- **Hardware:** Ryzen 7 5800X · Gigabyte Aorus Ultra x570 · 64GB DDR4 (2×32) ·
  EVGA FTW3 RTX 3080 10GB (+ Tesla P40 24GB pending) · Phanteks Evolv X ·
  Corsair RM850 · 1× Intel X540 single-port 10GbE.
- **OS:** Bare-metal Ubuntu LTS 24.04 — CUDA/Docker first-class; Steam + Proton
  (Proton GE) for gaming, X11 session for games. Sunshine streams the 3080 to
  Moonlight clients when away from the desk.
- **GPU split (when the P40 lands):** P40 has no display outputs — inference-only
  by hardware. P40 = Strata, 3080 = display + gaming. The 32GB RAM kit moves
  back here at that point.
- **VLAN:** v20 LAN. **Tailscale:** native client.
- **Undo:** OS on its own disk; weights/data on separate storage.

## nas-01 — NAS / media (TrueNAS Scale)

- **Role:** Bulk storage (ZFS), Plex + media transcode, *arr stack, torrent client.
- **Hardware:** i3-12100 · ASUS Prime H610 (DDR4) · Phanteks P500A ·
  Powerman 500W · Inspur LSI 9300-8i · dual-port X540 via M.2-to-PCIe adapter
  (verify adapter type; fallback is onboard 1GbE) · 4× WD Red 1TB + WD Blue 3TB
  + 4TB EMC SAS 12G. Needs: 2×8GB DDR4 kit, miniSAS→SFF-8482 cable for the SAS drive.
- **OS:** TrueNAS Scale (Debian-based, Docker-native apps, HBA-friendly).
- **Pools:**
  - `tank/media` — 4× WD Red 1TB RAIDZ1 (~2.7TB usable), Plex library.
  - `tank/fast` — 4TB EMC SAS, app data + *arr working space.
  - 3TB WD Blue — scratch / backup staging (no redundancy assumed).
- **Apps:** Plex (with /dev/dri passthrough — 12100 QuickSync handles 4K
  transcodes), Sonarr / Radarr / Prowlarr, qBittorrent behind Gluetun (VPN).
  Torrents land on `tank/fast`, *arr hardlinks into `tank/media`.
- **VLAN:** v20 — `nas.d2.lol`. Torrent traffic on v60 (VPN-routed).
- **NIC plan:** 10GbE via M.2 adapter once verified; 1GbE onboard until then.
- **Undo:** TrueNAS config backup after every change; pools portable with the HBA.

## compute-01 — Proxmox VE (main hypervisor)

- **Role:** VM/dev host, Tailscale services, IaC playground (Terraform + Ansible —
  the "idempotent" goal gets proven here first).
- **Hardware:** i5-13500 (14C/20T) · JGinyue B760I (DDR4) · 32GB DDR4 (2×16) ·
  Lian Li TU-150 · ESGaming 500W SFX · 1× Intel X540 single-port 10GbE.
- **NICs:** X540 → LAN trunk (VLANs tagged); Linux bridges per VLAN.
- **Storage:** local ZFS for VM disks (add SSDs when the first VM lands) and/or
  NFS from nas-01 over 10GbE.
- **Workloads:** dev/sandbox VMs, Tailscale subnet router, Ansible control node.
- **VLAN:** v20 mgmt; guests on v50 test.
- **Undo:** Proxmox Backup Server target on nas-01; node re-installs from Ansible.

## Utility tier — G4 Minis + NUC

- **util-01 / util-02 (HP ProDesk 600 G4 Mini, i5-8500T/32GB):** Pi-hole/AdGuard
  Home (LAN DNS), Uptime Kuma + monitoring.
- **util-03 (Intel NUC i3FNHN, i3-10110U/12GB):** Tailscale exit node, spare sandbox.
- All 1GbE, all Ansible-managed, all replaceable.

## Spare

- Thermaltake Tower 300 (+ PCIe 3.0 x16 riser w/ M.2 adapter), 4-bay NAS case.
- Future: second Proxmox node or next GPU home.

## Retired from the old plan

- **WGR (Windows Gaming Rig)** — gaming moved onto ai-box (Steam/Proton on Ubuntu).
- **Standalone media server** — merged into nas-01 (TrueNAS apps).
- **NUC/G4 as Proxmox cluster members** — repurposed to utility tier; compute-01
  is standalone for now.

## TV / Hue Bridge

- **VLAN:** v30 IoT.
- **Reachability:** **no inbound** to v10/v20; HomeAssistant (if deployed on
  compute-01) reaches the Hue API outbound to v30 via a single allow rule.

## Guest devices

- **VLAN:** v40.
- **Internet only.** No mDNS/SSDP leak between v40 and other VLANs.

## Test / sandbox guests

- **VLAN:** v50.
- See [`07-test-vlan.md`](07-test-vlan.md).
