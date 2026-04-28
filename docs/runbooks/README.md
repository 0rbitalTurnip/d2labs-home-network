# Runbooks

Step-by-step operational procedures. Keep them short, command-first, and idempotent.

| File | What it covers |
|---|---|
| [`bring-up-mhv.md`](bring-up-mhv.md) | First-boot config of MHV (Proxmox) — bridges, VLANs, IPMI |
| [`bring-up-opnsense.md`](bring-up-opnsense.md) | Fresh OPNsense install through working firewall + VLANs |
| [`switch-config-sg105e.md`](switch-config-sg105e.md) | Configure SG105E VLAN trunks via Easy Smart UI |
| [`switch-config-hex.md`](switch-config-hex.md) | hEX RB750Gr3 RouterOS config for v30/40/50 |
| [`add-host-to-v20.md`](add-host-to-v20.md) | Adding a new server to LAN — DHCP reservation, DNS, monitoring |
| [`migrate-to-10g-core.md`](migrate-to-10g-core.md) | Cutover plan when the 10G switch arrives |
| [`vpn-torrent-rotate-keys.md`](vpn-torrent-rotate-keys.md) | Rotate Mullvad/Proton WireGuard keys + verify kill-switch |
| [`disaster-recovery.md`](disaster-recovery.md) | Rebuild order if the rack goes dark |
