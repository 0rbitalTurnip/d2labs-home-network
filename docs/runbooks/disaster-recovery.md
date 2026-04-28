# Runbook — Disaster Recovery

The lab is dark. Restore in this order.

## 0. Prerequisites you should have off-site

- [ ] OPNsense config XML (encrypted, in 1Password / Bitwarden / Cloudflare R2).
- [ ] hEX RouterOS export (`.rsc`).
- [ ] SG105E config (a screenshot of the VLAN page is fine — it's a tiny config).
- [ ] Tailscale recovery codes.
- [ ] Cloudflare API token (for DNS-01 cert renewal).
- [ ] NAS pool: at least one cold backup (external disk or B2/wasabi).

## 1. Power-on order

1. ISP modem → wait for sync.
2. **OPNsense** → wait until WAN is up and DHCP/DNS respond.
3. **SG105E** + **hEX** + (future) **10G core** → check link lights.
4. **i3 NAS** → wait for ZFS pool import + NFS exports.
5. **MHV** → wait for Proxmox UI.
6. **Media Server, NUC, G4** → start in any order.
7. **WGR** when you actually want to game.

## 2. If OPNsense won't boot

- Boot the OPNsense USB installer.
- Restore config from the off-site XML on the import screen — no need to redo VLANs/firewall by hand.
- `tailscale up` again; the same machine name re-auths into the tailnet.

## 3. If MHV won't boot

- Boot Proxmox installer (USB), reinstall.
- Re-add NFS storage from the NAS.
- `qm/pct restore` from the latest backup on `nas-backup` — VMs come back as-is.

## 4. If the NAS pool is gone

- Replace failed disks.
- `zpool import` from the surviving disks if at all possible.
- If unrecoverable: rebuild empty, then `restic restore` from off-site backup into `tank/media` and `tank/proxmox`.

## 5. Smoke test after recovery

Same as the [bring-up-opnsense smoke test](bring-up-opnsense.md#8-smoke-test) and [bring-up-mhv smoke test](bring-up-mhv.md#7-smoke-test). Don't trust silence — run them all.
