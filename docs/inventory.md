**Inventory summary**

This file was generated from `docs/configs/inventory.csv` and provides a quick mapping of items and suggested roles.

- **CPUs**
  - Intel Core i5-13500 — good candidate for light server or NUC-class Proxmox node.
  - AMD Ryzen 7 5800X — strong candidate for a storage/NAS or heavier VM host.
  - Intel Core i3-12100 — useful for low-power nodes or test machines.

- **Motherboards / Builds**
  - JGinyue B760I Gaming WiFi (Mini-ITX) — compact Proxmox or media server build.
  - Gigabyte Aorus Ultra (ATX, AM4) — pair with Ryzen 7 for NAS or heavy VM workloads.
  - ASUS Prime H610 (mATX) — general-purpose host.

- **Memory**
  - 64GB / 32GB DDR4 kits — use for MHV or NAS hosts depending on workload.
  - SODIMM / UDIMM kits noted in CSV (HP ProDesk parts) — repurpose as lightweight nodes.

- **Networking**
  - Intel X540 Dual 10GbE NIC — primary 10G NIC for MHV (enp1s0f1) or NAS uplink.
  - Supermicro AOC-SG-i4 — quad 1GbE NIC for additional ports or low-profile hosts.

- **Cases**
  - Phanteks Evolv X2 / P500A — full / mid tower for rack or bench servers.

Suggested next steps

- Label each physical device and create a short `docs/hardware-selection.md` mapping items to roles (Proxmox host, NAS, test node).
- Decide which motherboard + CPU pair will be the primary MHV host (recommend: Intel X540-equipped board with 64GB RAM for Proxmox).

For the full CSV, see `docs/configs/inventory.csv`.
