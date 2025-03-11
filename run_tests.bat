@echo off
echo ===================================
echo Grok-VIS Test Runner
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

REM Run all tests
echo Running all tests...
echo ===================================
python tests\run_tests.py
set TEST_RESULT=%ERRORLEVEL%

echo.
echo ===================================
if %TEST_RESULT% equ 0 (
    echo All tests passed successfully!
) else (
    echo Some tests failed. Please check the output above for details.
)
echo ===================================

REM Pause to see the results
pause