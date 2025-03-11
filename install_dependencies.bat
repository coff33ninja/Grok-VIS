@echo off
echo ===================================
echo Grok-VIS Dependency Installer
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

REM Install dependencies from requirements.txt
echo Installing dependencies from requirements.txt...
echo This may take a while, please be patient.
echo ===================================
python -m pip install -r requirements.txt
set INSTALL_RESULT=%ERRORLEVEL%

echo.
echo ===================================
if %INSTALL_RESULT% equ 0 (
    echo Dependencies installed successfully!
    
    REM Install spaCy model
    echo.
    echo Installing spaCy English language model...
    python -m spacy download en_core_web_sm
    set SPACY_RESULT=%ERRORLEVEL%
    
    if %SPACY_RESULT% equ 0 (
        echo spaCy model installed successfully!
    ) else (
        echo Failed to install spaCy model. Please install it manually:
        echo python -m spacy download en_core_web_sm
    )
) else (
    echo Failed to install dependencies. Please check the output above for details.
)
echo ===================================

REM Run dependency check
echo.
echo Checking if all dependencies are installed...
call check_dependencies.bat

REM Pause to see the results
pause