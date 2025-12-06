@echo off
echo ========================================
echo Quick Training - No Warnings Version
echo ========================================
echo.

call venv\Scripts\activate.bat

REM Set environment to suppress all warnings
set PYTHONWARNINGS=ignore

echo Starting training with suppressed warnings...
echo.

python -W ignore train_model.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo Training failed or crashed
    echo ========================================
    echo.
    echo This is likely due to numpy compatibility issues
    echo with Python 3.13 on Windows.
    echo.
    echo SOLUTION: Use Python 3.11 instead
    echo   1. Download Python 3.11 from python.org
    echo   2. Install it
    echo   3. Delete venv folder: rmdir /s /q venv
    echo   4. Create new venv: py -3.11 -m venv venv
    echo   5. Run setup again: setup.bat
    echo.
) else (
    echo.
    echo ========================================
    echo Training completed successfully!
    echo ========================================
)

pause
