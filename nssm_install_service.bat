@echo off
echo This script will install Grok-VIS as a Windows service using NSSM
echo You need to have NSSM installed first: https://nssm.cc/download
echo.
echo Please make sure NSSM is in your PATH or copy nssm.exe to this directory.
echo.

REM Check if NSSM is available
where nssm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo NSSM not found in PATH. Please install NSSM first.
    echo Download from: https://nssm.cc/download
    pause
    exit /b 1
)

REM Create a wrapper script that ensures the service runs with the virtual environment
echo @echo off > "%~dp0run_grokvis_service.bat"
echo cd /d "%~dp0" >> "%~dp0run_grokvis_service.bat"

REM Check for virtual environments and add to the wrapper script
if exist "%~dp0.venv\Scripts\activate.bat" (
    echo Found .venv virtual environment
    echo call .venv\Scripts\activate.bat >> "%~dp0run_grokvis_service.bat"
    echo python main.py >> "%~dp0run_grokvis_service.bat"
    echo call deactivate >> "%~dp0run_grokvis_service.bat"
) else if exist "%~dp0venv\Scripts\activate.bat" (
    echo Found venv virtual environment
    echo call venv\Scripts\activate.bat >> "%~dp0run_grokvis_service.bat"
    echo python main.py >> "%~dp0run_grokvis_service.bat"
    echo call deactivate >> "%~dp0run_grokvis_service.bat"
) else (
    echo No virtual environment found, using system Python
    echo python main.py >> "%~dp0run_grokvis_service.bat"
)

echo Installing Grok-VIS service...
nssm install GrokVIS "%~dp0run_grokvis_service.bat"
nssm set GrokVIS AppDirectory "%~dp0"
nssm set GrokVIS DisplayName "Grok-VIS AI Assistant"
nssm set GrokVIS Description "Always-on AI assistant with voice recognition and web dashboard"
nssm set GrokVIS Start SERVICE_AUTO_START
nssm set GrokVIS AppStdout "%~dp0logs\grokvis.out.log"
nssm set GrokVIS AppStderr "%~dp0logs\grokvis.err.log"

echo.
echo Service installed. You can start it with: net start GrokVIS
echo Or use the Windows Services manager to control it.
echo.
set /p START_NOW=Do you want to start the service now? (Y/N): 
if /i "%START_NOW%"=="Y" (
    net start GrokVIS
    echo Service started!
)

pause