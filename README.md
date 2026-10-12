# d2lab — Homelab Network Architecture

Master documentation, diagrams, and runbooks for the **d2lab** homelab.

- **Domain:** `d2.lol`
- **Main hypervisor:** `compute-01` (Proxmox VE, i5-13500)
- **Cabling:** Cat6A RJ45 throughout
- **Edge:** OPNsense on HP ProDesk 600 G3 SFF (firewall + Tailscale + monitoring)
- **Core (now):** TP-Link SG105E (1 GbE, 802.1Q)
- **Core (planned):** 10 GbE switch — MikroTik CRS305 / CRS309 or QNAP QSW-M2108
  (must have RJ45 10GBase-T ports or SFP+-to-RJ45 transceivers — the X540 NICs are copper)
- **Aux router:** MikroTik hEX RB750Gr3 (test-net + IoT/Guest gateway)

## Quick links

| What | Where |
|---|---|
| Master topology diagram (editable) | [`diagrams/d2lab-network.drawio`](diagrams/d2lab-network.drawio) |
| PDF overview (4 pages) | [`diagrams/d2lab-network-overview.pdf`](diagrams/d2lab-network-overview.pdf) |
| VLAN + IP plan | [`docs/01-ip-plan.md`](docs/01-ip-plan.md) |
| Cabling + port map | [`docs/02-cabling.md`](docs/02-cabling.md) |
| Hosts & roles | [`docs/03-hosts.md`](docs/03-hosts.md) |
| Tailscale tailnet | [`docs/04-tailscale.md`](docs/04-tailscale.md) |
| VPN torrent path | [`docs/05-vpn-torrent.md`](docs/05-vpn-torrent.md) |
| DNS & d2.lol | [`docs/06-dns.md`](docs/06-dns.md) |
| Test VLAN / sandbox | [`docs/07-test-vlan.md`](docs/07-test-vlan.md) |
| Runbooks | [`docs/runbooks/`](docs/runbooks/) |
| Sample configs | [`docs/configs/`](docs/configs/) |

## How to edit the diagram

The `.drawio` file is the source of truth. Open it any of these ways:

- **Free, browser:** drag the file onto [https://app.diagrams.net](https://app.diagrams.net)
- **Visio:** use the [draw.io plugin for Visio](https://www.drawio.com/blog/import-from-visio) or import via Lucidchart
- **VS Code:** install the `Draw.io Integration` extension and double-click the file

Export to `.vsdx` (true Visio format) directly from app.diagrams.net: **File → Export as → VSDX**.

## Rebuilding the PDF

```bash
python3 scripts/build_pdf.py
```

Re-renders `diagrams/d2lab-network-overview.pdf` from `scripts/build_pdf.py`. Requires `reportlab` and `pypdf`.

## Repo layout

```
d2lab-net/
├── README.md                       ← you are here
├── LICENSE
├── .gitignore
├── diagrams/
│   ├── d2lab-network.drawio        ← editable Visio-style source
│   └── d2lab-network-overview.pdf  ← rendered overview
├── docs/
│   ├── 01-ip-plan.md
│   ├── 02-cabling.md
│   ├── 03-hosts.md
│   ├── 04-tailscale.md
│   ├── 05-vpn-torrent.md
│   ├── 06-dns.md
│   ├── 07-test-vlan.md
│   ├── runbooks/                   ← step-by-step ops procedures
│   └── configs/                    ← sample configs (sanitized)
└── scripts/
    └── build_pdf.py
```

## License

MIT — see [`LICENSE`](LICENSE).
