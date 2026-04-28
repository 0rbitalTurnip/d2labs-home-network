# Runbook — Bring up MHV (Proxmox)

Target state: Proxmox 8.x installed, `eno1` on MGMT v10, X540 (`enp1s0f0` + `enp1s0f1`) wired, all VLAN bridges defined, IPMI reachable on `10.10.10.110`.

## 1. Pre-install

- BIOS: enable VT-x/AMD-V, IOMMU, SR-IOV (if X540 supports it).
- IPMI: set static IP `10.10.10.110/24`, gw `10.10.10.1`, password manager.
- Patch `eno1` and IPMI to **SG105E P2** (mgmt VLAN 10).
- Patch `enp1s0f0` and `enp1s0f1` per [`02-cabling.md`](../02-cabling.md).

## 2. Install Proxmox

- Install onto NVMe; fs ZFS (mirror if dual-NVMe).
- Mgmt IP at install time: `10.10.10.10/24`, gw `10.10.10.1`, dns `10.10.10.1`.
- Hostname: `mhv.d2.lol`.

## 3. Network config (`/etc/network/interfaces`)

```ini
auto lo
iface lo inet loopback

# 1G management on eno1 (untagged v10)
auto eno1
iface eno1 inet manual

auto vmbr10
iface vmbr10 inet static
    address 10.10.10.10/24
    gateway 10.10.10.1
    bridge-ports eno1
    bridge-stp off
    bridge-fd 0
    # mgmt VLAN — Proxmox UI lives here

# 10G WAN failover / direct test (left as manual; bridge only when needed)
auto enp1s0f0
iface enp1s0f0 inet manual

# 10G LAN trunk
auto enp1s0f1
iface enp1s0f1 inet manual

# VLAN 20 — LAN/servers
auto enp1s0f1.20
iface enp1s0f1.20 inet manual
auto vmbr20
iface vmbr20 inet static
    address 10.10.20.10/24
    bridge-ports enp1s0f1.20
    bridge-stp off
    bridge-fd 0

# VLAN 30 — IoT (no IP on host; bridge only)
auto enp1s0f1.30
iface enp1s0f1.30 inet manual
auto vmbr30
iface vmbr30 inet manual
    bridge-ports enp1s0f1.30
    bridge-stp off
    bridge-fd 0

# VLAN 50 — TEST sandbox
auto enp1s0f1.50
iface enp1s0f1.50 inet manual
auto vmbr50
iface vmbr50 inet manual
    bridge-ports enp1s0f1.50
    bridge-stp off
    bridge-fd 0

# VLAN 60 — VPN-only (Gluetun lives here)
auto enp1s0f1.60
iface enp1s0f1.60 inet manual
auto vmbr60
iface vmbr60 inet manual
    bridge-ports enp1s0f1.60
    bridge-stp off
    bridge-fd 0
```

```bash
ifreload -a
ip -br addr     # vmbr10 should have 10.10.10.10
```

## 4. Repos + updates

```bash
# Switch off enterprise repo if no sub
sed -i 's/^/#/' /etc/apt/sources.list.d/pve-enterprise.list
echo "deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription" \
  > /etc/apt/sources.list.d/pve-no-subscription.list
apt update && apt -y dist-upgrade
```

## 5. Storage

- Add NFS storage → `nas.d2.lol:/mnt/tank/proxmox` mounted as `nas-vm`.
- Add NFS storage → `nas.d2.lol:/mnt/tank/backups` mounted as `nas-backup`, content = `Backups, ISO, Snippets`.

## 6. Tailscale + monitoring

```bash
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up --hostname=mhv --advertise-tags=tag:server
apt install -y prometheus-node-exporter
```

## 7. Smoke test

- [ ] Web UI reachable at `https://mhv.d2.lol:8006`
- [ ] `ping nas.d2.lol` from MHV shell works
- [ ] IPMI reachable at `10.10.10.110`
- [ ] `tailscale status` shows MHV with `tag:server`
- [ ] Backup job to `nas-backup` runs cleanly
