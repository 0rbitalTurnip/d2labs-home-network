Gluetun + qBittorrent example

This folder contains a minimal `docker-compose.yml` and `.env.example` showing how to run Gluetun (VPN client) and qBittorrent bound to the VPN container.

Quick start

1. Copy `.env.example` to `.env` and fill in `VPN_USERNAME`/`VPN_PASSWORD`.
2. Start the stack:

```bash
cd examples/gluetun
docker-compose up -d
```

3. Access qBittorrent web UI on the host port mapped in `docker-compose.yml` (see `8080` example mapping).

Notes

- `network_mode: service:gluetun` makes qBittorrent share the network namespace of the Gluetun container; traffic will egress via the VPN.
- Do NOT commit your `.env` file. Keep credentials out of the repo.
