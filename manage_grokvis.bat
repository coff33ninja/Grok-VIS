@echo off
setlocal enabledelayedexpansion

REM Check for virtual environment
set VENV_FOUND=0
set VENV_PATH=

if exist ".venv\Scripts\activate.bat" (
    set VENV_FOUND=1
    set VENV_PATH=.venv
) else if exist "venv\Scripts\activate.bat" (
    set VENV_FOUND=1
    set VENV_PATH=venv
)

echo Grok-VIS AI Assistant Manager
echo ============================
if !VENV_FOUND! EQU 1 (
    echo Using virtual environment: !VENV_PATH!
) else (
    echo No virtual environment found, using system Python
)
echo ============================
echo 1. Start Grok-VIS
echo 2. Stop Grok-VIS
echo 3. Check if Grok-VIS is running
echo 4. View logs
echo 5. Run Grok-VIS directly (for testing)
echo 6. Exit
echo ============================

set /p CHOICE=Enter your choice (1-6): 

if "%CHOICE%"=="1" (
    echo Starting Grok-VIS...
    
    REM Create a temporary start script with venv support
    echo @echo off > temp_start.bat
    echo cd /d "%~dp0" >> temp_start.bat
    
    if !VENV_FOUND! EQU 1 (
        echo call !VENV_PATH!\Scripts\activate.bat >> temp_start.bat
        echo python main.py >> temp_start.bat
        echo call deactivate >> temp_start.bat
    ) else (
        echo python main.py >> temp_start.bat
    )
    
    start "Grok-VIS" /min cmd /c "temp_start.bat"
    echo Grok-VIS started in background.
) else if "%CHOICE%"=="2" (
    echo Stopping Grok-VIS...
    for /f "tokens=2" %%i in ('tasklist ^| findstr "python.exe"') do (
        echo Found Python process with PID: %%i
        set /p CONFIRM=Kill this process? (Y/N): 
        if /i "!CONFIRM!"=="Y" (
            taskkill /PID %%i /F
            echo Process terminated.
        )
    )
) else if "%CHOICE%"=="3" (
    echo Checking if Grok-VIS is running...
    tasklist | findstr "python.exe"
    if %ERRORLEVEL% NEQ 0 (
        echo Grok-VIS is not running.
    ) else (
        echo Grok-VIS appears to be running.
    )
) else if "%CHOICE%"=="4" (
    if exist "logs\grokvis.out.log" (
        type "logs\grokvis.out.log"
    ) else (
        echo No log file found.
    )
) else if "%CHOICE%"=="5" (
    echo Running Grok-VIS directly (for testing)...
    
    if !VENV_FOUND! EQU 1 (
        call !VENV_PATH!\Scripts\activate.bat
        python main.py
        call deactivate
    ) else (
        python main.py
    )
    
    pause
    goto :eof
) else if "%CHOICE%"=="6" (
    exit
) else (
    echo Invalid choice. Please try again.
)

pause
goto :eof