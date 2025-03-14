@echo off
echo ===================================
echo Grok-VIS Error Diagnosis
echo ===================================
echo.

REM Check if Python is available
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python not found in PATH. Please make sure Python is installed and added to PATH.
    exit /b 1
)

REM Set console to UTF-8 encoding
chcp 65001 > nul

echo Using Python from:
where python
echo.

REM Run the error diagnosis script
echo Running error diagnosis...
echo ===================================
python tests\error_diagnosis.py
set DIAGNOSIS_RESULT=%ERRORLEVEL%

echo.
echo ===================================
if %DIAGNOSIS_RESULT% equ 0 (
    echo Error diagnosis completed.
    echo Please check the output above and the error_diagnosis.log file for details.
) else (
    echo Error diagnosis failed to run. Please check your Python installation.
)
echo ===================================

REM Pause to see the results
pause