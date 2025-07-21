# Xray Cross-Platform Python Client

## Features
- Downloads and runs Xray-core v25.6.8 for your OS/arch
- Generates a working config.json for VLESS+XHTTP (no TLS)
- Starts a local SOCKS5 proxy on 127.0.0.1:10808
- Logs proxy server info (IP, port, protocol, etc.) after startup
- Automatic environment checks and dependency validation
- Cross-platform support (Linux, Windows, macOS, ARM64)

## Folder Structure
```
client/
├── main.py         # Main runner script
├── utils.py        # Environment checks and utilities
├── xray/           # Holds the downloaded core
├── README.md       # This file
├── .env            # Your UUID and DOMAIN config
```

## Requirements
- Python 3.6 or higher
- `requests` package (`pip install requests`)
- `python-dotenv` package (`pip install python-dotenv`)
- Write permissions in the current directory

## Setup
1. Create a `.env` file in the `client/` directory:
   ```env
   UUID=your-uuid-here
   DOMAIN=your-domain-here
   ```
   Replace with your actual UUID and server domain.
2. Install required Python packages:
   ```bash
   pip install requests python-dotenv
   ```

## Usage
```bash
python main.py
```
- This will download Xray-core v25.6.8, generate `xray/config.json`, and start the proxy.
- After startup, the script will log your local proxy info and server connection details.
- Use `socks5h://127.0.0.1:10808` as your proxy in browsers or tools.

## Configuration
The client automatically:
- Detects your OS and architecture
- Downloads the appropriate Xray-core binary
- Creates a config.json with XHTTP transport
- Connects to your server using VLESS+XHTTP (no TLS)
- Reads UUID and DOMAIN from `.env`

## Test
```bash
curl --proxy socks5h://127.0.0.1:10808 https://api.ipify.org
```
You should see your VPS IP.

## Environment Checks
The script includes automatic checks for:
- Python version compatibility
- Required packages (requests, python-dotenv)
- Write permissions
- System architecture detection

## Notes
- Uses XHTTP transport (xhttp)
- Supports Xray-core v25.6.8
- Cross-platform (Linux, Windows, macOS, ARM64)
- Automatic binary download and setup
- Configurable XHTTP path via XHTTP_PATH variable in `main.py`
- Proxy info is logged after startup for easy reference 