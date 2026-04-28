# Runbook — Add a new host to LAN v20

## 1. Pick an IP

- Static reservations live in `10.10.20.10–.99`.
- DHCP pool is `10.10.20.150–.250`.
- Update [`01-ip-plan.md`](../01-ip-plan.md) with the new entry **first** so the doc is the source of truth.

## 2. DHCP reservation (OPNsense)

**Services → DHCPv4 → [vlan20] → Static Mappings**:

- MAC: `xx:xx:xx:xx:xx:xx`
- IP: `10.10.20.NN`
- Hostname: `<name>` (becomes `<name>.d2.lol` via DHCP→DNS registration)
- Description: short note

## 3. DNS override (only if you need a different name)

**Services → AdGuard Home → DNS rewrites**: add `<name>.d2.lol` → `10.10.20.NN`.

## 4. Patch + label

- Patch into SG105E P3/P4 (or the future 10G core switch).
- Label both ends of the cable with the cable ID; add a row to the cable inventory in [`02-cabling.md`](../02-cabling.md).

## 5. Monitoring

- Add to **Uptime Kuma**: `https://<name>.d2.lol` (or ICMP if no web UI).
- Add to **Prometheus** scrape config if it exposes node_exporter.

## 6. Tailscale (if needed)

- Install Tailscale; tag as `tag:server` or `tag:user`.
- Confirm it shows in the admin and is reachable from a phone off-LAN.
