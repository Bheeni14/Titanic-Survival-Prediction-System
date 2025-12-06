@echo off
echo ========================================
echo DIAGNOSIS: Python 3.13 Numpy Crash
echo ========================================
echo.
echo Your Python 3.13 + numpy combination is crashing.
echo This is a KNOWN ISSUE with Python 3.13 on Windows.
echo.
echo ========================================
echo SOLUTION: Switch to Python 3.11
echo ========================================
echo.
echo Step 1: Download Python 3.11
echo   Visit: https://www.python.org/downloads/
echo   Download: Python 3.11.x (Windows installer)
echo.
echo Step 2: Install Python 3.11
echo   - Run installer
echo   - Check "Add to PATH"
echo   - Complete installation
echo.
echo Step 3: Recreate virtual environment
echo   Commands to run:
echo.
echo   rmdir /s /q venv
echo   py -3.11 -m venv venv
echo   call venv\Scripts\activate
echo   pip install -r requirements.txt
echo   python train_emergency.py
echo.
echo ========================================
echo Why Python 3.11?
echo ========================================
echo - Stable, mature release
echo - All packages have pre-built wheels
echo - No compilation needed
echo - Used in production by millions
echo.
echo Python 3.13 was released November 2024
echo (less than 2 months ago) and many packages
echo don't have stable Windows builds yet.
echo.
pause
