# 04 — Tailscale Tailnet

## Architecture

- **Subnet router + exit node:** OPNsense g3 (the Tailscale plugin).
  - Advertises `10.10.0.0/16` so all VLANs are reachable through one route.
  - Exit-node mode lets your phone/laptop egress through your home WAN when on hostile networks.
- **Native clients:** MHV (host + select LXCs), Media Server, NAS, WGR, phones, laptop.
- **MagicDNS:** enabled. Aliases match `*.d2.lol` so the same hostname works on LAN and on the tailnet (see [`06-dns.md`](06-dns.md)).

## ACL design (tag-based)

Tags assigned in the Tailscale admin → Access Controls JSON:

| Tag | Who | Reaches |
|---|---|---|
| `tag:admin` | Personal laptop, phone | All VLANs incl. MGMT v10 |
| `tag:user` | WGR, TV apps, friend devices | LAN v20 only (Plex, NAS shares) |
| `tag:exit` | OPNsense | Exit node only (no inbound) |
| `tag:server` | MHV, Media, NAS | Receive from `tag:admin` + `tag:user` per port rules |

Skeleton ACL JSON:

```json
{
  "tagOwners": {
    "tag:admin":  ["autogroup:admin"],
    "tag:user":   ["autogroup:admin"],
    "tag:exit":   ["autogroup:admin"],
    "tag:server": ["autogroup:admin"]
  },
  "acls": [
    { "action": "accept", "src": ["tag:admin"],  "dst": ["*:*"] },
    { "action": "accept", "src": ["tag:user"],   "dst": ["10.10.20.0/24:*"] },
    { "action": "accept", "src": ["tag:server"], "dst": ["tag:server:*"] }
  ],
  "ssh": [
    { "action": "check", "src": ["tag:admin"], "dst": ["tag:server"], "users": ["root", "autogroup:nonroot"] }
  ]
}
```

## Setup checklist

1. Install Tailscale on OPNsense (`os-tailscale` plugin).
2. `tailscale up --advertise-routes=10.10.0.0/16 --advertise-exit-node --accept-dns=false`
3. In Tailscale admin → **Machines** → enable **Subnet routes** + **Exit node** for the OPNsense node.
4. Disable key expiry on the OPNsense node (it's infra).
5. Apply the ACL JSON above.
6. Install Tailscale on each native client; assign the right tag at first auth.
7. Test:
   - From phone off-LAN: `curl https://plex.d2.lol` should resolve to LAN IP and load Plex.
   - From phone with exit-node enabled: `curl https://ifconfig.me` returns home WAN IP.

## Failure modes & fallbacks

- **Tailscale control plane down:** the WireGuard server on OPNsense is the backup remote-admin path. Keep one client config off-site.
- **OPNsense down:** Tailscale on MHV can act as a fallback subnet router — pre-configure but leave routes off until needed.
