# MikroTik hEX RB750Gr3 — RouterOS 7 base config for d2lab
# Apply via /import or paste through the terminal. Adjust passwords before running.

/system identity set name=hex.d2.lol

/interface bridge add name=bridge1 vlan-filtering=no

/interface bridge port
add bridge=bridge1 interface=ether1 pvid=10
add bridge=bridge1 interface=ether2 pvid=50
add bridge=bridge1 interface=ether3 pvid=30
add bridge=bridge1 interface=ether4 pvid=40
add bridge=bridge1 interface=ether5 pvid=10

/interface bridge vlan
add bridge=bridge1 vlan-ids=10 tagged=bridge1,ether1 untagged=ether5
add bridge=bridge1 vlan-ids=30 tagged=bridge1,ether1 untagged=ether3
add bridge=bridge1 vlan-ids=40 tagged=bridge1,ether1 untagged=ether4
add bridge=bridge1 vlan-ids=50 tagged=bridge1,ether1 untagged=ether2

/interface bridge set bridge1 vlan-filtering=yes pvid=10

/interface vlan add interface=bridge1 vlan-id=10 name=vlan10
/ip address add interface=vlan10 address=10.10.10.3/24
/ip route add gateway=10.10.10.1 distance=1
/ip dns set servers=10.10.10.1

/ip service disable telnet,ftp,api,api-ssl,www
/ip service set ssh port=22
/user set admin password="CHANGE-ME"
