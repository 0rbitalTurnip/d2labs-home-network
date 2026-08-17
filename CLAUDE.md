# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **d2lab** homelab network architecture repository. It contains:

- **Network diagrams** (draw.io source + PDF exports)
- **Documentation** (IP plan, cabling, hosts, tailscale, DNS, test VLAN)
- **Runbooks** (operational procedures)
- **Sample configs** (sanitized configurations)
- **Build script** to regenerate the PDF overview

The network architecture features:
- OPNsense g3 as edge firewall, router, and Tailscale exit node
- Proxmox VE (MHV) as main hypervisor
- VLAN segmentation (MGMT, LAN, IoT, Guest, TEST, VPN)
- Tailscale mesh with tag-based ACLs
- Future 10G core switch planned

## Common Commands

### Rebuild the PDF Overview
```bash
python3 scripts/build_pdf.py
```
Regenerates `diagrams/d2lab-network-overview.pdf` from the draw.io source. Requires `reportlab` and `pypdf`.

### Edit Diagrams
- Open `diagrams/d2lab-network.drawio` in [draw.io](https://app.diagrams.net) (browser) or VS Code with Draw.io Integration extension.
- Export to `.vsdx` (Visio format) via **File → Export as → VSDX**.

### View Documentation
```bash
# Read IP plan, host assignments, tailscale config, etc.
start docs/01-ip-plan.md
start docs/03-hosts.md
start docs/04-tailscale.md
```

## File Structure

```
d2lab-net/
├── diagrams/
│   ├── d2lab-network.drawio     ← editable Visio-style source
│   └── d2lab-network-overview.pdf ← rendered PDF (commit this)
├── docs/
│   ├── 01-ip-plan.md            ← VLANs + IP/subnet plan
│   ├── 02-cabling.md            ← physical cabling map
│   ├── 03-hosts.md              ← host assignments & roles
│   ├── 04-tailscale.md          ← tailnet ACLs + setup
│   ├── 05-vpn-torrent.md        ← torrent egress path
│   ├── 06-dns.md                ← DNS (AdGuard + split-horizon)
│   ├── 07-test-vlan.md          ← sandbox / break-things lab
│   ├── runbooks/                ← step-by-step ops procedures
│   └── configs/                 ← sample configs (sanitized)
└── scripts/
    └── build_pdf.py             ← PDF generator (ReportLab)
```

## Development Workflow

1. **Update diagrams**: Edit `diagrams/d2lab-network.drawio` to reflect network changes.
2. **Regenerate PDF**: Run `python3 scripts/build_pdf.py` after any diagram changes.
3. **Update docs**: Modify relevant Markdown files in `docs/` to document changes.
4. **Add runbooks**: For new operational procedures, add a file to `docs/runbooks/`.
5. **Commit**: Include both the updated `.drawio` and the regenerated `.pdf`.

## Important Notes

- **PDF generation**: The build script uses ReportLab with Google Fonts (DMSans + JetBrainsMono). Fonts are cached locally; if missing, they're downloaded automatically.
- **Diagrams**: The `.drawio` file is the source of truth. The PDF is a vector-rendered snapshot.
- **Configs**: Sample configs in `docs/configs/` are sanitized. Real secrets belong in `secrets/` (gitignored) or a password manager.
- **Tailscale**: ACLs are tag-based. See `docs/04-tailscale.md` for the current tag design.

## Testing Changes

After updating diagrams and regenerating the PDF:
```bash
# Verify PDF renders correctly
start diagrams/d2lab-network-overview.pdf

# Check for broken links or formatting issues in docs
# (No formal linter, but manually review)
```

## Operational Procedures

Refer to the runbooks in `docs/runbooks/` for:
- First-boot config of MHV (Proxmox) and OPNsense
- Switch configuration (TP-Link SG105E, MikroTik hEX)
- Adding hosts to VLAN 20
- Disaster recovery
- VPN key rotation

## Architecture Decisions

- **VLAN scheme**: 10 MGMT, 20 LAN, 30 IoT, 40 Guest, 50 TEST, 60 VPN, plus Tailscale overlay (100.64.0.0/10)
- **Inter-VLAN routing**: OPNsense (except TEST VLAN, which is hEX-routed for isolation)
- **Remote access**: Tailscale subnet router + exit node (OPNsense)
- **DNS**: AdGuard Home with split-horizon for `*.d2.lol`
- **Future**: 10G core switch to replace TP-Link SG105E

## Troubleshooting

- **PDF build fails**: Ensure `reportlab` and `pypdf` are installed (`pip install reportlab pypdf`).
- **Fonts missing**: The script downloads fonts automatically; ensure internet access.
- **Diagram editing**: Use draw.io browser version or VS Code extension; avoid Visio unless exporting to `.vsdx`.

## License

MIT (see LICENSE). Contributions welcome for homelab documentation and runbooks.