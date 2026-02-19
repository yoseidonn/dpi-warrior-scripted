@echo off
SETLOCAL EnableDelayedExpansion

echo === Windows Proxy Toggle ===

:: Check the current proxy status in the Registry
FOR /F "tokens=3" %%A IN ('reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable 2^>nul') DO (
    SET ProxyEnable=%%A
)

:: If it's 0 (OFF), turn it ON
IF "%ProxyEnable%"=="0x0" (
    echo [~] Turning Proxy ON...
    
    :: Enable proxy
    reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f >nul
    
    :: Set the IP and ports for HTTP, HTTPS, and SOCKS
    reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d "http=127.0.0.1:10809;https=127.0.0.1:10809;socks=127.0.0.1:10808" /f >nul
    
    :: Set ignored hosts (local network)
    reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyOverride /t REG_SZ /d "localhost;127.*;10.*;172.16.*;192.168.*;<local>" /f >nul
    
    echo ✅ Proxy is now ON (Routing through Xray).

) ELSE (
    :: If it's 1 (ON), turn it OFF
    echo [~] Turning Proxy OFF...
    reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f >nul
    echo ❌ Proxy is now OFF (Direct Connection).
)

:: Force Windows to refresh internet settings
powershell -command "$net = New-Object -ComObject WScript.Network; rundll32.exe ietcpl.cpl,UpdatePerUserSystemParameters"

echo.
pause