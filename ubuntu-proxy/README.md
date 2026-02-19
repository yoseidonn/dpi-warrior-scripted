# Ubuntu Proxy Configuration

This folder contains screenshots detailing how to route your Ubuntu network traffic through the local Xray client.

**Important Note for Linux Users:** Because different Linux distributions use different Desktop Environments (GNOME, KDE Plasma, XFCE, etc.), system-wide proxy settings are handled differently depending on your OS flavor. The screenshots in this folder are specifically for **Ubuntu (GNOME)**. 

## UI Configuration (For Browsers & General Desktop Apps)
Follow the provided screenshots to configure your network settings:

1. Open **Settings** > **Network** > **Proxy**.
2. Set Configuration to **Manual** (Elle).
3. **HTTP / HTTPS Proxy**: 
   * URL: `127.0.0.1`
   * Port: `10809`
4. **FTP Proxy**: 
   * Leave both URL and Port completely **blank**.
5. **SOCKS Host**: 
   * URL: `127.0.0.1`
   * Port: `10808`
6. **Ignored Hosts**: 
   * Leave as default (`localhost, 127.0.0.0/8, ::1`) to prevent routing loops.

## Terminal Configuration (For CLI Tools)
The GNOME UI proxy settings usually do not apply to terminal applications like `curl`, `wget`, or `apt`. To route your terminal traffic through the VPN, run the following commands in your session:

```bash
export http_proxy=[http://127.0.0.1:10809](http://127.0.0.1:10809)
export https_proxy=[http://127.0.0.1:10809](http://127.0.0.1:10809)
export all_proxy=socks5://127.0.0.1:10808
```
