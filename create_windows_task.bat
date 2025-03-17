@echo off
echo Creating Windows Scheduled Task for Grok-VIS...

REM Get the current directory
set CURRENT_DIR=%~dp0
set TASK_NAME=GrokVIS_AI_Assistant

REM Create a wrapper script that checks for virtual environment
echo @echo off > "%CURRENT_DIR%run_grokvis_task.bat"
echo cd /d "%CURRENT_DIR%" >> "%CURRENT_DIR%run_grokvis_task.bat"

REM Check for virtual environments and add to the wrapper script
if exist "%CURRENT_DIR%.venv\Scripts\activate.bat" (
    echo Found .venv virtual environment
    echo call .venv\Scripts\activate.bat >> "%CURRENT_DIR%run_grokvis_task.bat"
    echo python main.py >> "%CURRENT_DIR%run_grokvis_task.bat"
    echo call deactivate >> "%CURRENT_DIR%run_grokvis_task.bat"
) else if exist "%CURRENT_DIR%venv\Scripts\activate.bat" (
    echo Found venv virtual environment
    echo call venv\Scripts\activate.bat >> "%CURRENT_DIR%run_grokvis_task.bat"
    echo python main.py >> "%CURRENT_DIR%run_grokvis_task.bat"
    echo call deactivate >> "%CURRENT_DIR%run_grokvis_task.bat"
) else (
    echo No virtual environment found, using system Python
    echo python main.py >> "%CURRENT_DIR%run_grokvis_task.bat"
)

set SCRIPT_PATH=%CURRENT_DIR%run_grokvis_task.bat

REM Create the task
schtasks /create /tn "%TASK_NAME%" /tr "%SCRIPT_PATH%" /sc onlogon /ru "%USERNAME%" /rl highest /f

REM Check if task was created successfully
if %ERRORLEVEL% EQU 0 (
    echo Task created successfully!
    echo The Grok-VIS AI Assistant will start automatically when you log on.
    echo You can also start it manually from Task Scheduler.
    
    REM Ask if user wants to start the task now
    set /p START_NOW=Do you want to start Grok-VIS now? (Y/N): 
    if /i "%START_NOW%"=="Y" (
        schtasks /run /tn "%TASK_NAME%"
        echo Grok-VIS is now running!
    )
) else (
    echo Failed to create task. Please run this script as administrator.
)

pause