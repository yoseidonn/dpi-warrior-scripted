import os, platform, subprocess
import zipfile, requests, json
import uuid as uuidlib
from pathlib import Path

import dotenv

dotenv.load_dotenv()

# === CONFIG ===
UUID = os.getenv("UUID")
DOMAIN = os.getenv("DOMAIN")
PORT = 443
USE_TLS = True
WS_PATH = "/apple"  # Must match the server's nginx + xray path

XRAY_VERSION = "1.8.13"
XRAY_DIR = Path("xray")
CONFIG_PATH = XRAY_DIR / "config.json"

PROXY_PORT = 10808

# === END OF CONFIG ===

def detect_os_arch():
    os_name = platform.system().lower()
    arch = platform.machine().lower()
    if "arm" in arch or "aarch64" in arch:
        arch = "arm64"
    elif "x86_64" in arch or arch == "amd64":
        arch = "64"
    elif "386" in arch or arch == "x86":
        arch = "32"
    return os_name, arch

def download_xray(os_name, arch):
    XRAY_DIR.mkdir(parents=True, exist_ok=True)

    asset = f"xray-{os_name}-{arch}.zip"
    bin_name = "xray.exe" if os_name == "windows" else "xray"
    zip_url = f"https://github.com/XTLS/Xray-core/releases/download/v{XRAY_VERSION}/{asset}"
    zip_path = XRAY_DIR / "xray.zip"

    print(f"[+] Downloading Xray from {zip_url}")
    r = requests.get(zip_url)

    if r.status_code != 200:
        print(r.content)
        raise Exception(f"Failed to download Xray binary: {r.status_code}")

    with open(zip_path, "wb") as f:
        f.write(r.content)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(XRAY_DIR)

    xray_bin = XRAY_DIR / bin_name
    if xray_bin.exists():
        os.chmod(xray_bin, 0o755)

    zip_path.unlink()

def create_config(uuid, domain, port, tls):
    print("[+] Creating config.json")
    config = {
        "log": {
            "loglevel": "warning"
        },
        "inbounds": [{
            "port": PROXY_PORT,
            "listen": "127.0.0.1",
            "protocol": "socks",
            "settings": {
                "auth": "noauth",
                "udp": True
            }
        }],
        "outbounds": [{
            "protocol": "vless",
            "settings": {
                "vnext": [{
                    "address": domain,
                    "port": port,
                    "users": [{
                        "id": uuid,
                        "encryption": "none"
                    }]
                }]
            },
            "streamSettings": {
                "network": "ws",
                "security": "tls" if tls else "none",
                "tlsSettings": {
                    "serverName": domain
                } if tls else {},
                "wsSettings": {
                    "path": WS_PATH,
                    "headers": {
                        "Host": domain
                    }
                }
            }
        }]
    }

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

def run_xray():
    print("[+] Starting Xray...")
    print(f"[+] SOCKS5 proxy will be available at: 127.0.0.1:{PROXY_PORT}")
    print(f"[+] Configure your applications to use SOCKS5 proxy: 127.0.0.1:{PROXY_PORT}")
    os_name = platform.system().lower()
    xray_bin = XRAY_DIR / ("xray.exe" if os_name == "windows" else "xray")
    subprocess.run([str(xray_bin), "run", "-config", str(CONFIG_PATH)])

if __name__ == "__main__":
    os_name, arch = detect_os_arch()
    print(f"[~] Detected OS: {os_name}, Arch: {arch}")
    xray_bin = XRAY_DIR / ("xray.exe" if os_name == "windows" else "xray")
    if not xray_bin.exists():
        download_xray(os_name, arch)
    create_config(UUID, DOMAIN, PORT, USE_TLS)
    run_xray()
