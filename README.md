# Xray VLESS + XHTTP Dockerized Setup

A streamlined, Dockerized deployment for an Xray-core VPN utilizing the VLESS protocol with an XHTTP transport. This project uses a single codebase to run both the remote server and the local client via Docker Compose profiles.

## Architecture

Xray Core Version: v25.6.8

Protocol: VLESS

Transport: XHTTP

Security: TLS (Auto-generated self-signed certificates available)

## Folder Structure
.
├── docker-compose.yml       # Manages both server and client profiles
├── Dockerfile               # Multi-stage build for Xray + envsubst
├── setup-env.py             # Interactive script to generate your .env file
├── entrypoint.sh            # Injects environment variables at runtime
├── generate-certificates.sh  # Auto-generates self-signed TLS certs
├── client/
│   └── config.template.json # Xray client template
├── server/
│   └── config.template.json # Xray server template
├── windows-proxy/           # Guides and scripts for Windows OS routing
└── ubuntu-proxy/            # Guides for Ubuntu OS routing


## Prerequisites

- Docker and Docker Compose plugin installed.
- Python 3.x (to run the setup script).

(Optional) If you plan to pull the pre-built image from GitHub Packages and it is set to private, ensure your Docker client is authenticated with ghcr.io.

## Deployment Options: Local Build vs. GitHub Packages

By default, the docker-compose.yml is configured to build the image locally using the provided Dockerfile (build: .).

If you prefer to skip the build process and pull the pre-built image directly from GitHub Packages (yoseidonn), update your docker-compose.yml for both services by replacing build: . with the image directive.

services:
  server:
    image: ghcr.io/yoseidonn/your-repo-name:latest
    # remove build: .
    # ... rest of config ...


## Quick Start

1. Configure the Environment

Run the interactive setup script to generate your configuration. It will ask whether you are setting up the remote VPS or your local machine.
```bash
python3 setup-env.py
```

This will generate an .env file in the root directory. Keep this file secure, as it contains your UUID.

2. Deploy the Server (On your VPS)

After running setup-env.py and selecting server, start the server profile.
```bash
docker compose --profile server up -d --build
```

(If auto-generation is enabled in your setup, certificates will be generated and saved directly to your host machine in a ./certs directory).

3. Deploy the Client (On your Local Machine)

After running setup-env.py and selecting client, start the client profile.
```bash
docker compose --profile client up -d --build
```


Your local proxies will now be exposed and ready for use at:
```config
HTTP/HTTPS: 127.0.0.1:10809
SOCKS5: 127.0.0.1:10808
```

4. Route Your OS Traffic

To actually send your internet traffic through the VPN, you need to configure your operating system to use the local proxy ports. Check the windows-proxy/ or ubuntu-proxy/ folders for automated scripts and screenshot guides.