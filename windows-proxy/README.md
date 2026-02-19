# Windows Proxy Configuration

This folder contains the necessary guides and scripts to route your Windows 10/11 network traffic through the local Xray client. 

You have two options to set up your proxy: an automated batch script or manual configuration via the Windows UI.

## Option 1: The Automated Way (Recommended)
Use the included `proxy-toggle.bat` script to quickly switch your proxy settings on and off.

1. Double-click `proxy-toggle.bat`.
2. The script will check your current registry settings.
3. If the proxy is OFF, it will turn it ON (routing traffic through Xray on ports `10808` and `10809`).
4. If the proxy is ON, it will turn it OFF (restoring direct internet connection).

*Note: You might see a brief terminal window flash as it updates the Windows Registry and forces the OS to refresh its network settings.*

## Option 2: The Manual Way (Screenshots)
If you prefer to configure the proxy manually or if the script is blocked by your system policies, follow the included screenshots:

1. Open **Settings** > **Network & internet** > **Proxy**.
2. Under **Manual proxy setup**, click **Set up**.
3. Toggle **Use a proxy server** to **On**.
4. Set the **Proxy IP address** to `127.0.0.1` and the **Port** to `10809`.
5. Enter `localhost;127.0.0.1;` in the exceptions box to prevent local apps from looping.
6. Check **Don't use the proxy server for local (intranet) addresses**.
7. Click **Save**.