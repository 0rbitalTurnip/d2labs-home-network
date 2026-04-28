# Runbook — Rotate VPN torrent keys + verify kill-switch

Cadence: every 90 days, or immediately if you suspect compromise.

## 1. Generate new WG keypair (Mullvad example)

- Log in to mullvad.net → **WireGuard configuration**.
- Generate new keypair, download the `.conf` file.
- Note the new private key, address, DNS, peer pubkey, and endpoint.

## 2. Update Gluetun

Update env vars on the Gluetun LXC/container:

```env
WIREGUARD_PRIVATE_KEY=<new private>
WIREGUARD_PUBLIC_KEY=<new peer pub>
WIREGUARD_ADDRESSES=<new /32>
VPN_ENDPOINT_IP=<new endpoint IP>
VPN_ENDPOINT_PORT=51820
```

Restart the container:

```bash
pct exec <gluetun-ctid> -- docker compose -f /opt/gluetun/docker-compose.yml up -d
# or for a pure-LXC Gluetun:
systemctl restart gluetun
```

## 3. OPNsense allow-list refresh

If the new endpoint IP differs, update the firewall alias `vpn_endpoints` and reload rules.

## 4. Verify (DO NOT SKIP)

```bash
# Inside the qBittorrent network namespace:
curl https://ifconfig.me                  # = Mullvad/Proton IP, NOT WAN
curl https://am.i.mullvad.net/json | jq    # confirms exit IP + country

# Kill-switch test
ip link set tun0 down
curl --connect-timeout 3 https://ifconfig.me   # MUST timeout
ip link set tun0 up
```

If the kill-switch test resolves *anything*, stop torrenting until [`05-vpn-torrent.md`](../05-vpn-torrent.md) rule #5 is correct.

## 5. Revoke old keypair

Back in Mullvad's portal, **delete the old WG keypair** so nothing else can use it.

## 6. Log it

Add a line to `docs/configs/key-rotation-log.md`:

```
2026-04-28  rotated WG keys for Gluetun  •  endpoint=se23-wg.mullvad.net  •  verified kill-switch
```
