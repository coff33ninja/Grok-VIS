@echo off
echo ===================================
echo Grok-VIS Dependency Checker
echo ===================================
echo.

REM Check if Python is available
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python not found in PATH. Please make sure Python is installed and added to PATH.
    exit /b 1
)

echo Using Python from:
where python
echo.

REM List of dependencies to check
set DEPENDENCIES=joblib numpy sentence_transformers spacy pynvml sqlite3 TTS apscheduler sqlalchemy requests wakeonlan opencv-python psutil scikit-learn librosa pvporcupine sounddevice flask wikipedia beautifulsoup4 pillow

echo Checking dependencies...
echo ===================================

set MISSING_COUNT=0

for %%d in (%DEPENDENCIES%) do (
    python tests\check_dependency.py %%d
    if %ERRORLEVEL% neq 0 (
        set /a MISSING_COUNT+=1
    )
)

echo.
echo ===================================
if %MISSING_COUNT% equ 0 (
    echo All dependencies are installed!
) else (
    echo %MISSING_COUNT% dependencies are missing. Please install them using:
    echo pip install -r requirements.txt
)
echo ===================================

REM Pause to see the results
pause