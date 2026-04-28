# 05 — VPN Torrent Path (VLAN 60)

Goal: every byte of torrent traffic exits through a commercial WireGuard VPN, with a hard kill-switch so a tunnel drop never leaks to the ISP.

## Topology

```
   ┌───────────── MHV (Proxmox) ──────────────┐
   │                                          │
   │   Gluetun LXC                            │
   │     ├─ eth0 → vmbr60 (VLAN 60, .60)      │
   │     └─ tun0 → WireGuard to Mullvad/Proton │
   │                                          │
   │   qBittorrent  ── bind: tun0 only        │
   │   Prowlarr     ── routes via Gluetun     │
   │                                          │
   │   Sonarr / Radarr (v20)                  │
   │     └─ talk to Prowlarr/qBit via          │
   │        Gluetun's exposed RPC port         │
   │                                          │
   └──────────────────────────────────────────┘
                 │                ▲
                 │ tun0 egress    │ completed media (SMB)
                 ▼                │
         ┌────── OPNsense ──────┐ │
         │  Policy route:       │ │
         │   src 10.10.60.0/24  │ │
         │   → only via tun0    │ │
         │  Drop everything else│ │
         └──────────────────────┘ │
                 │                │
                 ▼                │
              Internet           NAS (v20, /tank/media)
                                  │
                                  ▼
                         Plex / Jellyfin (v20)
```

## Why a separate VLAN

Putting Gluetun and the torrent clients on **VLAN 60** means OPNsense can enforce the kill-switch with a single firewall rule on the v60 interface — there's no way for a misconfigured app or escaped container to reach `10.10.20.x` (or the ISP) directly.

## OPNsense rules on `vlan60`

In order:

1. **Allow** UDP from `10.10.60.0/24` to your VPN provider's WireGuard endpoint(s) (port 51820 typical).
2. **Allow** TCP from `10.10.60.0/24` to `10.10.20.20:445` (NAS SMB) and `:2049` (NFS) — completed downloads.
3. **Allow** TCP from `10.10.60.0/24` to MHV/Media on the *arr API ports (so Prowlarr/qBit can be polled).
4. **Block** all other from `10.10.60.0/24` to `10.10.0.0/16`.
5. **Block** all other from `10.10.60.0/24` to `any` (kill-switch — only the WG endpoint allow above survives).

## Gluetun LXC hints

- Use the **`qmcgaw/gluetun`** Docker image inside a privileged LXC (or as a Docker host VM if you prefer).
- Mount only what's needed; bind-mount `/dev/net/tun`.
- Env vars (Mullvad example):
  ```
  VPN_SERVICE_PROVIDER=mullvad
  VPN_TYPE=wireguard
  WIREGUARD_PRIVATE_KEY=...
  WIREGUARD_ADDRESSES=10.x.x.x/32
  SERVER_CITIES=Stockholm
  FIREWALL_OUTBOUND_SUBNETS=10.10.20.0/24
  ```
- Run qBittorrent and Prowlarr **in the same network namespace** as Gluetun (`network_mode: "service:gluetun"`) so they have no other path.
- Expose qBit/Prowlarr web UI via Gluetun's `HTTP_CONTROL_SERVER` ports — not direct.

## Sonarr / Radarr layout

- Live on **v20** (LAN). They're orchestrators, not the actual leech path.
- Talk to Prowlarr/qBit via the API port published by Gluetun (allow rule #3 above).
- Move-completed-files goes from Gluetun's namespace **to the NAS via SMB/NFS** (allow rule #2). Sonarr/Radarr then trigger Plex library refresh.

## Verification

```bash
# From inside the qBittorrent container:
curl https://ifconfig.me                  # should return Mullvad IP, NOT your WAN IP
curl --connect-timeout 3 https://1.1.1.1  # should still work (egress via tun0)

# Kill the WireGuard tunnel: traffic must stop entirely.
ip link set tun0 down
curl --connect-timeout 3 https://ifconfig.me   # should TIMEOUT (kill-switch)
```

If the second curl returns *anything*, the kill-switch is broken — fix rule #5 before continuing.
