# Runbook — TP-Link SG105E VLAN config

The SG105E is "Easy Smart" — config is via the TP-Link Easy Smart Configuration Utility (Win/macOS) or the device's built-in web UI at its mgmt IP.

## 1. Set mgmt IP

Default is `192.168.0.1` from a fresh boot. Either reach it on a laptop with a `192.168.0.0/24` IP, or run the Easy Smart Utility on the same broadcast domain.

Set:

- IP: `10.10.10.2/24`
- Gateway: `10.10.10.1`
- VLAN for mgmt: 10 (configure **after** you set the trunks below — otherwise you lock yourself out).

## 2. 802.1Q VLAN config

**VLAN → 802.1Q VLAN:** enable.

| VLAN ID | Name | Tagged ports | Untagged ports |
|---|---|---|---|
| 10 | MGMT | 1, 2 | (none — native) |
| 20 | LAN | 1, 2 | 3, 4 |
| 30 | IoT | 1, 2, 5 | — |
| 40 | GUEST | 1, 5 | — |
| 50 | TEST | 1, 2, 5 | — |
| 60 | VPN | 1, 2 | — |

> Ports 3 and 4 stay untagged on v20 for the media server / downstream sub-switch. Port 5 carries the IoT/Guest/Test trunk to the hEX.

## 3. PVID (port default VLAN)

| Port | PVID |
|---|---|
| 1 | 10 |
| 2 | 10 |
| 3 | 20 |
| 4 | 20 |
| 5 | 1 (default — only tagged frames matter) |

## 4. Save & verify

- **Save Config** (the device defaults to running-config only — this step writes to flash).
- Plug a laptop into P3, get a v20 DHCP lease.
- From that laptop: `ping 10.10.10.2` should fail (correct — mgmt is on v10).
- Move laptop to v10 (or shell in via OPNsense): `ping 10.10.10.2` works.
