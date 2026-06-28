import os
import uuid

def prompt(question, default=""):
    ans = input(f"{question} [{default}]: ").strip()
    return ans if ans else default

def main():
    print("=== Xray Configuration Setup ===")
    
    mode = prompt("Are you setting up the 'server' or 'client'?", "server").lower()
    
    domain = prompt("Enter your domain", "vpn.yourdomain.com")
    xhttp_path = prompt("Enter XHTTP path", "/xray")
    
    user_uuid = prompt("Enter UUID (leave blank to auto-generate)", "")
    if not user_uuid:
        user_uuid = str(uuid.uuid4())
        print(f"[+] Generated new UUID: {user_uuid}")
        
    # Prompt for ALL variables regardless of mode
    cert_file = prompt("CERT_FILE path", "/etc/ssl/xray/fullchain.pem")
    key_file = prompt("KEY_FILE path", "/etc/ssl/xray/privkey.pem")
    gen_certs = prompt("Auto-generate self-signed certs? (true/false)", "true")
    port = prompt("Remote Server Port", "443")
    proxy_port = prompt("Local SOCKS5 Proxy Port", "10808")

    env_lines = [
        f"UUID={user_uuid}",
        f"DOMAIN={domain}",
        f"XHTTP_PATH={xhttp_path}",
        f"CERT_FILE={cert_file}",
        f"KEY_FILE={key_file}",
        f"GENERATE_CERTS={gen_certs}",
        f"PORT={port}",
        f"PROXY_PORT={proxy_port}",
    ]

    if mode not in ("server", "client"):
        print("[-] Unknown mode. Please run again and specify 'server' or 'client'.")
        return

    with open(".env", "w") as f:
        f.write("\n".join(env_lines) + "\n")

    print(f"\n✅ Successfully generated .env file for {mode}!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSetup cancelled.")