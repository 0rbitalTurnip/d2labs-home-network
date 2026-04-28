# Sample configs

Sanitized, committable configs. Anything with a real secret lives in `secrets/` (gitignored) or in your password manager.

| File | Purpose |
|---|---|
| [`opnsense-vlans.example.xml`](opnsense-vlans.example.xml) | Snippet of the VLAN section of an OPNsense config |
| [`hex-routeros.example.rsc`](hex-routeros.example.rsc) | RouterOS export for the hEX |
| [`adguard-rewrites.example.yaml`](adguard-rewrites.example.yaml) | Split-horizon `*.d2.lol` overrides |
| [`gluetun-compose.example.yml`](gluetun-compose.example.yml) | Gluetun + qBittorrent + Prowlarr Compose stack |
| [`tailscale-acl.example.json`](tailscale-acl.example.json) | Tag-based ACLs from `04-tailscale.md` |
| [`mhv-interfaces.example`](mhv-interfaces.example) | `/etc/network/interfaces` for MHV |
| `key-rotation-log.md` | Append-only log of VPN/SSH/cert rotations |
