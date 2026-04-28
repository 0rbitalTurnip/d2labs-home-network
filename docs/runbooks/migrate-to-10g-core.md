# Runbook — Migrate to 10G core switch

Cutover plan for when the 10G switch (e.g. **MikroTik CRS305-1G-4S+IN**, **CRS309-1G-8S+IN**, or **QNAP QSW-M2108-2C**) arrives.

## Pre-flight

- [ ] 10G switch unboxed, firmware updated to latest.
- [ ] At least 2× Cat6A patch cables (6–10 ft) on hand for the OPNsense + MHV uplinks.
- [ ] SFP+ to RJ45 modules if the switch is SFP+ only (CRS305/309) — confirm compatibility (10GBASE-T modules run hot, plan airflow).
- [ ] All 802.1Q config translated from [SG105E port map](../02-cabling.md#sg105e-port-map-5-ports-8021q) into the new switch's UI/CLI.
- [ ] Backup OPNsense + hEX configs.

## Cutover order (minimize downtime)

1. **Bring up the 10G switch out-of-band** with mgmt IP `10.10.10.4`. Configure all VLANs (10/20/30/40/50/60) and trunk ports first, with no cables plugged into uplinks yet.
2. Run a temporary cable: 10G switch port 5 → SG105E P1 (replacing OPNsense uplink for a moment? **No** — keep OPNsense → SG105E live). Instead, plug 10G switch port 5 → SG105E P5 (where hEX was) **after** you move the hEX uplink to 10G switch port 6. Net effect: hEX is now downstream of the 10G core, SG105E still runs through OPNsense.
3. **Move OPNsense uplink:** unplug `igb1` from SG105E P1 → plug into 10G switch port 1. SG105E loses VLAN trunk for ~5 sec. Set the 10G switch port 1 to trunk all VLANs, native 10.
4. **Move SG105E uplink:** plug SG105E P1 → 10G switch port 5 (1G). Now SG105E is a downstream access switch hanging off the 10G core.
5. **Move MHV `enp1s0f1`:** unplug from SG105E P2 → plug into 10G switch port 2. Trunk all VLANs.
6. **Verify:** Proxmox UI still loads, Plex still streams, NAS still mounted.
7. **Move NAS** when its 10G NIC is in: 10G switch port 3.
8. **Move Media Server** when its 10G NIC is in: 10G switch port 4.

## Post-cutover

- [ ] Update [`02-cabling.md`](../02-cabling.md) port-map table.
- [ ] Update DHCP reservation: `sw10g.d2.lol` = `10.10.10.4`.
- [ ] Disable any now-unused ports on SG105E.
- [ ] Speed test: `iperf3` MHV ↔ NAS should hit ~9.4 Gbit/s once both are on 10G ports.

## Rollback

If anything misbehaves: unplug from 10G switch, plug back into SG105E in the original port — no config changes needed because both switches carry the same VLAN tagging.
