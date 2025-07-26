import os, platform, requests
import zipfile, subprocess, shutil
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# === CONFIG ===
UUID = os.getenv("UUID")
DOMAIN = os.getenv("DOMAIN")
PORT = 443  # Change from 80 to 443
XRAY_VERSION = "v25.6.8"
DOWNLOAD_BASE = f"https://github.com/XTLS/Xray-core/releases/download/{XRAY_VERSION}"
PROXY_PORT = 10808
XHTTP_PATH = "/xray"

# === END OF CONFIG ===

def check_tools():
    required = ["unzip", "curl", "python3"]
    missing = []
    for tool in required:
        if shutil.which(tool) is None:
            missing.append(tool)
    if missing:
        print(f"[!] Missing tools: {', '.join(missing)}")
        print("    Install them with: sudo apt install " + " ".join(missing))
        exit(1)
    print("[+] Environment checks passed.")

def detect_platform():
    os_name = platform.system().lower()
    arch = platform.machine().lower()
    if os_name == "linux" and (arch == "x86_64" or arch == "amd64"):
        asset = "Xray-linux-64.zip"
        bin_name = "xray"
    elif os_name == "windows" and (arch == "x86_64" or arch == "amd64"):
        asset = "Xray-windows-64.zip"
        bin_name = "xray.exe"
    else:
        raise Exception(f"Unsupported OS/arch: {os_name}/{arch}")
    print(f"[~] Detected OS: {os_name}, Arch: {arch}")
    return asset, bin_name

def create_config(uuid: str, domain: str, proxy_port: int = 10808, remote_port: int = 443, path: str = "/xray") -> None:
    config = {
        "log": {
            "loglevel": "warning"
        },
        "inbounds": [
            {
                "tag": "socks-in",
                "port": proxy_port,
                "listen": "127.0.0.1",
                "protocol": "socks",
                "settings": {
                    "auth": "noauth",
                    "udp": True
                }
            },
            {
                "tag": "http-in",
                "port": 10809,
                "listen": "127.0.0.1",
                "protocol": "http",
                "settings": {
                    "timeout": 300
                }
            }
            # Removed the FTP inbound - Xray doesn't support it
        ],
        "outbounds": [
            {
                "tag": "vless-out",
                "protocol": "vless",
                "settings": {
                    "vnext": [
                        {
                            "address": domain,
                            "port": remote_port,
                            "users": [
                                {
                                    "id": uuid,
                                    "encryption": "none"
                                }
                            ]
                        }
                    ]
                },
                "streamSettings": {
                    "network": "xhttp",
                    "security": "tls",
                    "tlsSettings": {
                        "serverName": domain,
                        "allowInsecure": False
                    },
                    "xhttpSettings": {
                        "path": path,
                        "host": domain,
                        "acceptProxyProtocol": False
                    }
                }
            },
            {
                "tag": "blocked",
                "protocol": "blackhole",
                "settings": {}
            }
        ],
        "dns": {
            "servers": [
                "1.1.1.1",
                "8.8.8.8",
                "localhost"
            ]
        },
        "routing": {
            "domainStrategy": "AsIs",
            "rules": [
                {
                    "type": "field",
                    "inboundTag": ["socks-in", "http-in"],  # Removed "ftp-in", for future use proxychain or something else
                    "outboundTag": "vless-out"
                },
                {
                    "type": "field",
                    "domain": ["geosite:category-ads"],
                    "outboundTag": "blocked"
                }
            ]
        }
    }

    config_path = Path("xray/config.json")
    config_path.write_text(json.dumps(config, indent=2))
    print(f"Client config written to {config_path.resolve()}")

    # === Printouts ===
    print("\n✅ Xray Client Configuration Generated!")
    print(f"📄 Config Path: {config_path.resolve()}")
    print(f"�� Local SOCKS5 Proxy: 127.0.0.1:{proxy_port}")
    print(f"�� Local HTTP Proxy: 127.0.0.1:10809")
    print(f"📁 Local FTP Proxy: 127.0.0.1:10810")
    print(f"�� Remote VLESS+XHTTP Server: {domain}:{remote_port}{path}")
    print(f"�� UUID: {uuid}")
    print("🌐 DNS forwarding: Enabled (1.1.1.1, 8.8.8.8)\n")
    print("🚀 To start Xray:")
    print("   ./xray run -c config.json\n")

def download_xray(asset):
    url = f"{DOWNLOAD_BASE}/{asset}"
    print(f"[+] Downloading Xray from {url}")
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"Failed to download Xray binary: {r.status_code}")
    with open("xray.zip", "wb") as f:
        f.write(r.content)
    print("[+] Download complete.")

def extract_xray():
    with zipfile.ZipFile("xray.zip", "r") as zip_ref:
        zip_ref.extractall("xray")
    print("[+] Extracted Xray.")

def print_proxy_details():
    print("\n" + "="*60)
    print("PROXY SERVER DETAILS")
    print("="*60)
    print(f"Local SOCKS5 Proxy: 127.0.0.1:{PROXY_PORT}")
    print(f"Local HTTP Proxy: 127.0.0.1:10809")
    print("PROXY SETTINGS FOR APPLICATIONS:")
    print("-" * 40)
    print(f"SOCKS5 Proxy: socks5h://127.0.0.1:{PROXY_PORT}")
    print(f"HTTP Proxy:   http://127.0.0.1:10809")
    print(f"HTTPS Proxy:  http://127.0.0.1:10809")
    print()
    print("SERVER CONNECTION DETAILS:")
    print("-" * 40)
    print(f"Server Domain: {DOMAIN}")
    print(f"Server Port: {PORT}")
    print(f"Protocol: VLESS")
    print(f"Transport: XHTTP")
    print(f"XHTTP Path: {XHTTP_PATH}")
    print(f"UUID: {UUID}")
    print(f"Security: TLS (Encrypted)")
    print()
    print("USAGE EXAMPLES:")
    print("-" * 40)
    print("curl --proxy socks5h://127.0.0.1:10808 https://api.ipify.org")
    print("curl --proxy http://127.0.0.1:10809 https://httpbin.org/ip")
    print("="*60)

def run_xray(bin_name):
    config_path = os.path.abspath("xray/config.json")
    xray_bin = os.path.abspath(f"xray/{bin_name}")
    os.chmod(xray_bin, 0o755)
    print("[+] Starting Xray...")
    print_proxy_details()
    subprocess.run([xray_bin, "run", "-config", config_path])

if __name__ == "__main__":
    check_tools()
    asset, bin_name = detect_platform()
    create_config(UUID, DOMAIN, PROXY_PORT, PORT, XHTTP_PATH)
    download_xray(asset)
    extract_xray()
    run_xray(bin_name)