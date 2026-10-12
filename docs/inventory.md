**Inventory summary**

Reconciled 2026-10-11 against the owner's component spreadsheet (ground truth).
Every item below has a build assignment — nothing is "loose" anymore.
Corrections from the old sheet: the case is the original **Phanteks Evolv X**
(not X2), the Tower 300 is **Thermaltake** (not Thermalright), the Aorus board
is the **x570** variant, both Intel boards are **DDR4**, and the 3080 is the
**EVGA FTW3 Ultra**.

- **Box 1 — ai-box (AI/gaming, Ubuntu 24.04):** Ryzen 7 5800X · Gigabyte Aorus
  Ultra x570 · 64GB DDR4 (2×32) · EVGA FTW3 RTX 3080 10GB (+ Tesla P40 24GB
  pending) · Phanteks Evolv X · Corsair RM850 · 1× Intel X540 single-port.
  32GB RAM kit returns here when the P40 lands.
- **Box 2 — nas-01 (TrueNAS Scale):** i3-12100 · ASUS Prime H610 (DDR4) ·
  Phanteks P500A · Powerman 500W · Inspur LSI 9300-8i · dual-port X540 (via
  M.2-to-PCIe adapter — verify type) · 4× WD Red 1TB (RAIDZ1) + WD Blue 3TB +
  4TB EMC SAS · SATA breakout cable. Needs: 2×8GB DDR4 kit, miniSAS→SFF-8482
  cable for the SAS drive.
- **Box 3 — compute-01 (Proxmox VE):** i5-13500 · JGinyue B760I (DDR4) ·
  32GB DDR4 (2×16) · Lian Li TU-150 · ESGaming 500W SFX · 1× Intel X540
  single-port.
- **Edge — edge-01 (OPNsense):** HP ProDesk 600 G3 SFF (i5-7500/16GB) +
  Supermicro AOC-SG-i4 quad-port GbE.
- **Utility:** 2× HP ProDesk 600 G4 Mini (i5-8500T/32GB) + Intel NUC i3FNHN
  (i3-10110U/12GB) — DNS, monitoring, Tailscale.
- **Spare:** Thermaltake Tower 300 (+ PCIe riser w/ M.2 adapter), 4-bay NAS case.

**Networking note:** the X540s are copper 10GBase-T, not SFP+. The planned 10GbE
core must have RJ45 10G ports or SFP+-to-RJ45 transceivers.

For the full CSV (with Ansible groups/tags), see `docs/configs/inventory.csv`.
`scripts/inventory_to_ansible.py` generates the Ansible inventory from it.
