@echo off
chcp 65001 >nul
title Roblox Sniperz Setup
color 5

:: Display ASCII banneral
cls
echo.
echo              ██████╗  ██████╗ ██████╗ ██╗      ██████╗ ██╗  ██╗    
echo              ██╔══██╗██╔═══██╗██╔══██╗██║     ██╔═══██╗╚██╗██╔╝    
echo              ██████╔╝██║   ██║██████╔╝██║     ██║   ██║ ╚███╔╝     
echo              ██╔══██╗██║   ██║██╔══██╗██║     ██║   ██║ ██╔██╗     
echo              ██║  ██║╚██████╔╝██████╔╝███████╗╚██████╔╝██╔╝ ██╗    
echo              ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝   
echo.
echo                       - ROBLOX SNIPERZ - MADE BY LARXY -
echo.

:: Ask for webhook usage
set /p useWebhook=Do you want to get notified on Discord when you get a snipe? (yes/no): 

:: Ask for webhook if needed
if /I "%useWebhook%"=="yes" (
    set /p webhook=Paste your Discord webhook URL: 
) else (
    set webhook=
)

:: Ask for username length
:askLength
set /p length=Enter how many characters you want (3 to 5): 

if %length% LSS 3 (
    echo Error: Length must be 3, 4 or 5.
    goto askLength
)
if %length% GTR 5 (
    echo Error: Length must be 3, 4 or 5.
    goto askLength
)

echo.
echo Launching sniper...

:: Run the Python sniper with parameters
python sniper.py %length% %webhook%

echo.
echo Press any key to exit...
pause >nul
