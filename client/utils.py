import sys

# === BASIC SYSTEM CHECKS ===
def check_requirements():
    # Check Python version
    if sys.version_info < (3, 6):
        print("[-] Python 3.6 or higher is required.")
        sys.exit(1)

    # Check for 'requests' package
    try:
        import requests
    except ImportError:
        print("[-] Required Python package 'requests' is missing.")
        print("[*] You can install it by running: pip install requests")
        sys.exit(1)

    # Optional: Check for write permissions
    from pathlib import Path
    try:
        Path("test_permission.tmp").write_text("test")
        Path("test_permission.tmp").unlink()
    except Exception as e:
        print(f"[-] Warning: No write permission in current directory. ({e})")
        print("[*] Run this script from a writable directory or with appropriate permissions.")
        sys.exit(1)

    print("[+] Environment checks passed.")
