Quickstart — Minimal reproducible path (20 minutes)

Prereqs

- A machine to act as the initial controller (Windows with WSL, Linux, or macOS). For automation, use WSL/Ubuntu or an Ubuntu host.
- Proxmox-ready host (recommended MHV candidate from `docs/inventory.md`).
- OPNsense appliance image/VM for the edge router.
- Docker / docker-compose (for example services) on a host or LXC.

Steps

1. Clone the repo and prepare Python deps

```bash
git clone <repo-url>
cd d2labs-home-network
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

2. Regenerate the diagrams PDF to verify the repo is working

```bash
# default: writes to repo's diagrams/ directory
python3 scripts/build_pdf.py
# or specify output file
python3 scripts/build_pdf.py --out ./diagrams/d2lab-network-overview.pdf
```

3. Bring up OPNsense (VM or physical)

- Boot OPNsense and follow the web UI for initial setup.
- Import VLAN snippets from `docs/configs/opnsense-vlans.example.xml` if desired (Backup → Restore → choose import).

4. Provision a minimal Proxmox node (MHV)

- Use `docs/configs/mhv-interfaces.example` as `/etc/network/interfaces` reference.
- Ensure `eno1` is on MGMT VLAN (v10) so you can SSH from your management network.

5. Run the Gluetun Docker example (optional quick demo)

```bash
cd examples/gluetun
cp .env.example .env        # fill in VPN credentials
docker-compose up -d
```

6. Verify basic connectivity

- Confirm the diagram PDF exists and reflects topology: open `diagrams/d2lab-network-overview.pdf`.
- From MHV, confirm VLAN tagging on `enp1s0f1` (ip link, ip -d link show).

Where to go next

- Follow `docs/runbooks/bring-up-mhv.md` and `docs/runbooks/bring-up-opnsense.md` for in-depth provisioning.
- To automate the above, see the planned `ansible/` skeleton (coming soon).

If you want, I can now implement the Ansible skeleton and add the `examples/gluetun` folder with `.env.example` and a tested compose file—shall I proceed?