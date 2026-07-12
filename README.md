# DPI Warrior — VLESS + XHTTP VPN

Xray-core VPN using **VLESS** protocol with **XHTTP** transport and **TLS** encryption (Nginx terminates TLS). Designed to bypass DPI/censorship.

## Architecture

```
Client → Nginx :443 (TLS) → grpc_pass → Xray (Unix socket) → Internet
```

## ⚠️ Critical Lessons Learned

### 1. Use `grpc_pass`, NOT `proxy_pass`
XHTTP transport uses gRPC-like multiplexed streams. Nginx **must** use `grpc_pass` to forward correctly. Using `proxy_pass` will buffer and break the XHTTP streams — client connects but no traffic flows.

### 2. Always set XHTTP `mode`
Both server and client MUST explicitly set `"mode": "stream-one"` in `xhttpSettings`. Without it, Xray uses an undefined/unknown mode.

### 3. HTTP/2 is required
XHTTP stream-one mode requires HTTP/2. Add `listen ... ssl http2` and `http2 on;` in the nginx server block.

### 4. Long timeouts
XHTTP uses long-lived connections. Use these nginx settings:
- `client_header_timeout 5m`
- `keepalive_timeout 5m`  
- `client_body_timeout 5m`
- `grpc_read_timeout 315`
- `grpc_send_timeout 5m`

### 5. Unix socket, not TCP
Xray should listen on a Unix socket (`/dev/shm/xrxh.socket,0666`) for XHTTP + Nginx, not TCP 127.0.0.1:10000.

### 6. Client & server Xray versions MUST match
XHTTP is under active development. Mismatched versions cause protocol glitches.

### 7. `allowInsecure` removed in Xray v26.6+
Use `pinnedPeerCertSha256` (a string, NOT an array) with the certificate SHA-256 fingerprint instead.

### 8. Sing-box clients don't support XHTTP
Streisand, Sing-box etc. do NOT support XHTTP. Use Xray-core based clients: v2RayTun, FoXray, V2Box, Nekobox, v2rayNG.

## Files

| File | Description |
|------|-------------|
| `server/config.json` | Xray server config — Unix socket + stream-one |
| `server/nginx.conf` | Nginx config — grpc_pass + http2 + long timeouts |
| `server/xray.service` | Xray systemd service unit |
| `client/config.example.json` | Client config template |
| `client/main.py` | Client management script |

## Quick Setup (Server)

```bash
# Install dependencies
apt-get install -y nginx
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)"

# Generate UUID and cert
UUID=$(uuidgen)
IP=$(curl -s ifconfig.me)
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl-certificates/$IP.key \
  -out /etc/nginx/ssl-certificates/$IP.crt \
  -subj "/CN=$IP"

# Copy configs from this repo
cp server/config.json /usr/local/etc/xray/config.json   # edit UUID
cp server/nginx.conf /etc/nginx/sites-available/dpi-warrior  # edit IP
# Enable & start services
systemctl restart xray
systemctl restart nginx
```

## Share Link (for client import)

```
vless://YOUR_UUID@YOUR_IP:443?encryption=none&security=tls&type=xhttp&path=%2Fxray&mode=stream-one&host=YOUR_IP&alpn=h2&allowInsecure=true&fp=firefox#DPI-Warrior
```

## Active Deployments

| Instance | IP | UUID | Status |
|---|---|---|---|
| Current | `49.13.83.178` | `dafaa97c-4e16-4b13-9b11-a41c437912c7` | ✅ Online |
| Previous | `167.233.110.236` | — | ❌ Deleted |
| Previous | `46.225.186.1` | — | ❌ Deleted |
