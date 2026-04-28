# 02 — Cabling Layout & Port Map

All physical links are **Cat6A RJ45**. 10G runs use the future 10G core switch; until that ships, MHV's `enp1s0f1` runs at 1G into the SG105E (X540 negotiates down).

## Color code (recommend matching label colors on the patch panel)

| Color | Role |
|---|---|
| Magenta / pink | WAN — ISP / Internet |
| Teal | LAN 10 GbE — X540 / 10G core |
| Blue | MGMT 1 GbE — `eno1` / IPMI / switch admin |
| Orange | IoT VLAN 30 |
| Purple | Guest VLAN 40 |
| Green | TEST VLAN 50 / sandbox |
| Yellow (dashed) | Tailscale overlay (logical, not a physical cable) |

## MHV (Proxmox) interfaces

| Interface | Speed | Role | Cable | Other end | VLANs |
|---|---|---|---|---|---|
| `eno1` | 1 GbE | Management | Cat6A | SG105E P2 | v10 (untagged) |
| `enp1s0f0` | 10G | WAN failover / direct test | Cat6A | OPNsense (igb0 alt) — direct | WAN |
| `enp1s0f1` | 10G | LAN trunk | Cat6A | Future 10G core (uplink 1) — interim: SG105E P2 | v10/20/30/50/60 tagged |
| IPMI / BMC | 100M | Out-of-band mgmt | Cat6A | SG105E P2 (shared on v10) | v10 |

## SG105E port map (5 ports, 802.1Q "Easy Smart")

| Port | Mode | VLANs | Connected to |
|---|---|---|---|
| P1 | Trunk | 10 (native), 20/30/40/50/60 tagged | OPNsense `igb1` |
| P2 | Trunk | 10 (native), 20/30/50/60 tagged | MHV `enp1s0f1` (and shared `eno1` mgmt) |
| P3 | Access | v20 | Main Media Server |
| P4 | Access | v20 | Downstream NUC / G4 / NAS (use a small unmanaged sub-switch if needed before 10G core arrives) |
| P5 | Trunk | 30/40/50 tagged | MikroTik hEX RB750Gr3 ether1 |

> The SG105E only has 5 ports — once you have 7+ devices you **need** the downstream hEX or the future 10G core. Treat the SG105E as "core L2" for now and the hEX as "downstream extender + IoT/Guest/Test router".

## hEX RB750Gr3 port map

| Port | Role | VLAN(s) | Connected to |
|---|---|---|---|
| `ether1` | Trunk uplink | 30/40/50 | SG105E P5 |
| `ether2` | Access — TEST lab | v50 | Lab patch panel / sandbox VMs |
| `ether3` | Access — IoT | v30 | TV, Hue Bridge, smart plugs |
| `ether4` | Access — Guest AP | v40 | Guest wireless AP (visitor SSID) |
| `ether5` | Spare / out-of-band | v10 | Mgmt patch (optional) |

## Future 10G core switch port plan

When the 10G switch lands (e.g. **MikroTik CRS305-1G-4S+IN** or **CRS309-1G-8S+IN**, or **QNAP QSW-M2108-2C** for RJ45):

| Port | Speed | Role | Connected to |
|---|---|---|---|
| 1 | 10G | OPNsense `igb1` LAN trunk uplink | OPNsense |
| 2 | 10G | MHV `enp1s0f1` LAN trunk | MHV |
| 3 | 10G | NAS storage trunk (when NIC upgraded) | NAS |
| 4 | 10G | Media server (when NIC upgraded) | Media |
| 5 | 1G via RJ45/SFP | SG105E uplink (legacy 1G) | SG105E |
| 6 | 1G | hEX uplink | hEX |
| 7–8 | 10G | Reserved (2nd MHV link, lab) | — |

## Cable run inventory

Add new entries here when you pull a cable. Helps when troubleshooting a flaky link.

| ID | From | To | Length | Type | Color | Tested |
|---|---|---|---|---|---|---|
| C-001 | ISP ONT | OPNsense `igb0` | 3 ft | Cat6A | magenta | ☐ |
| C-002 | OPNsense `igb1` | SG105E P1 | 6 ft | Cat6A | teal | ☐ |
| C-003 | MHV `eno1` | SG105E P2 (mgmt) | 6 ft | Cat6A | blue | ☐ |
| C-004 | MHV `enp1s0f1` | SG105E P2 (LAN trunk) | 6 ft | Cat6A | teal | ☐ |
| C-005 | MHV `enp1s0f0` | OPNsense direct | 6 ft | Cat6A | magenta | ☐ |
| C-006 | MHV IPMI | SG105E P2 (shared mgmt) | 6 ft | Cat6A | blue | ☐ |
| C-007 | Media Server | SG105E P3 | — | Cat6A | teal | ☐ |
| C-008 | NUC i5 | SG105E P4 (or sub-switch) | — | Cat6A | teal | ☐ |
| C-009 | G4 Mini | SG105E P4 (or sub-switch) | — | Cat6A | teal | ☐ |
| C-010 | NAS | SG105E P4 (or sub-switch) | — | Cat6A | teal | ☐ |
| C-011 | WGR | SG105E P4 (or sub-switch) | — | Cat6A | teal | ☐ |
| C-012 | SG105E P5 | hEX `ether1` | — | Cat6A | orange | ☐ |
| C-013 | hEX `ether3` | TV / Hue | — | Cat6A | orange | ☐ |
| C-014 | hEX `ether4` | Guest AP | — | Cat6A | purple | ☐ |
| C-015 | hEX `ether2` | Lab patch | — | Cat6A | green | ☐ |
