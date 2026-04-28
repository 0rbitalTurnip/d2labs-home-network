# 07 — Test / Sandbox VLAN (50)

A dedicated "break things" lab so experiments don't take down production.

## What lives here

- Nested Proxmox / nested ESXi
- Terraform + Ansible apply targets (fresh VMs spun up and torn down on demand)
- k3s / k8s clusters
- Untrusted ISO-of-the-day testing
- Network protocol experiments (mDNS, BGP via FRR, custom DHCP, etc.)
- Anything that should *not* be able to talk to v20 / v10

## Routing

- **Gateway:** OPNsense `vlan50` interface at `10.10.50.1` (so it has internet).
- **Optional standalone mode:** the **MikroTik hEX RB750Gr3** can take over routing for v50 entirely — useful when you're testing things that might break OPNsense rules. Move v50 from "trunked through the SG105E" to "hEX is the gateway" by changing `ether2` on the hEX from access to the v50 native segment and pointing test hosts at the hEX.

## Firewall rules (OPNsense `vlan50`)

1. Allow `vlan50` → `Internet` (any).
2. Block `vlan50` → `10.10.0.0/16` (everything internal).
3. Allow `vlan50` → `10.10.20.20:445` *only if* you opt into NAS sharing for a specific test (default off).
4. Allow established/related back.

## DHCP

- Pool: `10.10.50.50–10.10.50.200`.
- Lease time: 1 hour (test VMs come and go).
- Reservations live in `docs/configs/dhcp-vlan50-reservations.md` if you pin one.

## SSH / management

- Don't use your real SSH keys here. Generate a `~/.ssh/d2lab-test` keypair and use it only for v50.
- Ansible inventory lives in `docs/configs/ansible-inventory-test.yml` (template).

## Reset procedure

When v50 is FUBAR:

```bash
# Wipe all VMs/CTs tagged `lab` on MHV
qm list | awk '/lab/ {print $1}' | xargs -r -I{} qm destroy {} --purge
pct list | awk '/lab/ {print $1}' | xargs -r -I{} pct destroy {} --purge

# Re-apply DHCP/firewall via Ansible
ansible-playbook -i inventory-test.yml site.yml --tags v50_reset
```
