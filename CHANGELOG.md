# Changelog

All notable changes to the d2lab network architecture get logged here. Date format: YYYY-MM-DD.

## [Unreleased] — 2026-10-11
### Changed
- Full inventory reconciliation against the owner's component spreadsheet
  (`docs/configs/inventory.csv`, `docs/inventory.md`): every item now carries a
  build assignment; corrected Evolv X (not X2), Thermaltake Tower 300 (not
  Thermalright), Aorus Ultra x570, DDR4 on both Intel boards, EVGA FTW3 3080.
- Host roles reworked (`docs/03-hosts.md`): ai-box (Ubuntu 24.04, Strata +
  gaming), nas-01 (TrueNAS Scale, media stack), compute-01 (Proxmox, main
  hypervisor), edge-01 (OPNsense on G3 SFF), utility tier (G4 Minis + NUC).
  Retired: standalone WGR and media-server hosts (merged into ai-box/nas-01).
- README: hypervisor renamed to compute-01; 10GbE switch note now calls out the
  copper X540 requirement.

## [0.1.0] — 2026-04-28
### Added
- Initial repo scaffolded.
- Master topology diagram (`diagrams/d2lab-network.drawio`).
- 4-page PDF overview (`diagrams/d2lab-network-overview.pdf`).
- Docs: IP plan, cabling, hosts, Tailscale, VPN-torrent, DNS, test VLAN.
- Runbooks: MHV bring-up, OPNsense bring-up, SG105E + hEX config, add-host-to-v20, 10G migration, VPN key rotation, disaster recovery.
- Sample configs: AdGuard rewrites, Gluetun Compose, Tailscale ACL, MHV `/etc/network/interfaces`, OPNsense VLANs snippet, hEX RouterOS export.
