@echo off
echo ===================================
echo Grok-VIS Specific Test Runner
echo ===================================
echo.

REM Check if a test file was specified
if "%~1"=="" (
    echo Please specify a test file to run.
    echo Usage: run_specific_test.bat test_file_name
    echo Example: run_specific_test.bat test_core
    exit /b 1
)

REM Check if Python is available
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python not found in PATH. Please make sure Python is installed and added to PATH.
    exit /b 1
)

echo Using Python from:
where python
echo.

REM Run the specified test
set TEST_FILE=%~1
if not "%TEST_FILE:~0,5%"=="test_" set TEST_FILE=test_%TEST_FILE%
if not "%TEST_FILE:~-3%"==".py" set TEST_FILE=%TEST_FILE%.py

echo Running test: %TEST_FILE%
echo ===================================

if exist "tests\%TEST_FILE%" (
    python tests\%TEST_FILE%
    set TEST_RESULT=%ERRORLEVEL%
) else (
    echo Test file not found: tests\%TEST_FILE%
    echo Available test files:
    dir /b tests\test_*.py
    exit /b 1
)

echo.
echo ===================================
if %TEST_RESULT% equ 0 (
    echo Test passed successfully!
) else (
    echo Test failed. Please check the output above for details.
)
echo ===================================

REM Pause to see the results
pause