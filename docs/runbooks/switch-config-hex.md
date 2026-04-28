# Runbook — MikroTik hEX RB750Gr3 (RouterOS 7)

Role: VLAN trunk extender + IoT/Guest/Test access router downstream of SG105E P5.

## 1. Reset and update

```routeros
/system reset-configuration no-defaults=yes skip-backup=yes
# After reboot:
/system identity set name=hex.d2.lol
/system package update check-for-updates
/system package update install
```

## 2. Bridge + VLAN-aware

```routeros
/interface bridge add name=bridge1 vlan-filtering=no
/interface bridge port
add bridge=bridge1 interface=ether1
add bridge=bridge1 interface=ether2
add bridge=bridge1 interface=ether3
add bridge=bridge1 interface=ether4
add bridge=bridge1 interface=ether5

/interface bridge vlan
add bridge=bridge1 vlan-ids=30 tagged=bridge1,ether1 untagged=ether3
add bridge=bridge1 vlan-ids=40 tagged=bridge1,ether1 untagged=ether4
add bridge=bridge1 vlan-ids=50 tagged=bridge1,ether1 untagged=ether2
add bridge=bridge1 vlan-ids=10 tagged=bridge1,ether1 untagged=ether5

/interface ethernet switch port set [find name=ether1] vlan-mode=secure
/interface bridge set bridge1 vlan-filtering=yes pvid=10

# PVIDs per access port
/interface bridge port set [find interface=ether2] pvid=50
/interface bridge port set [find interface=ether3] pvid=30
/interface bridge port set [find interface=ether4] pvid=40
/interface bridge port set [find interface=ether5] pvid=10
```

## 3. Mgmt IP on v10

```routeros
/interface vlan add interface=bridge1 vlan-id=10 name=vlan10
/ip address add interface=vlan10 address=10.10.10.3/24
/ip route add gateway=10.10.10.1 distance=1
/ip dns set servers=10.10.10.1
```

## 4. Optional standalone mode for v50

When you want the hEX to **be** the v50 router (so OPNsense doesn't see test traffic at all):

```routeros
/interface vlan add interface=bridge1 vlan-id=50 name=vlan50-rtr
/ip address add interface=vlan50-rtr address=10.10.50.1/24
/ip pool add name=pool50 ranges=10.10.50.50-10.10.50.200
/ip dhcp-server add interface=vlan50-rtr address-pool=pool50 disabled=no
/ip dhcp-server network add address=10.10.50.0/24 gateway=10.10.50.1 dns-server=10.10.10.1
/ip firewall nat add chain=srcnat out-interface=vlan10 src-address=10.10.50.0/24 action=masquerade
```

(Pull this when you want OPNsense back in charge.)

## 5. Verify

```routeros
/interface bridge vlan print
/ip address print
/ping 10.10.10.1
/ping 1.1.1.1
```
