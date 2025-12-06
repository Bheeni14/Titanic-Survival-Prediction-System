@echo off
echo.
echo ========================================
echo   TITANIC SURVIVAL PREDICTOR
echo   Setup Verification
echo ========================================
echo.

set "ERRORS=0"

REM Check Python
echo [1/8] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo    [FAIL] Python not found
    set /a ERRORS+=1
) else (
    python --version
    echo    [PASS] Python installed
)
echo.

REM Check Node.js
echo [2/8] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo    [FAIL] Node.js not found
    set /a ERRORS+=1
) else (
    node --version
    echo    [PASS] Node.js installed
)
echo.

REM Check npm
echo [3/8] Checking npm installation...
npm --version >nul 2>&1
if errorlevel 1 (
    echo    [FAIL] npm not found
    set /a ERRORS+=1
) else (
    npm --version
    echo    [PASS] npm installed
)
echo.

REM Check Docker
echo [4/8] Checking Docker installation (optional)...
docker --version >nul 2>&1
if errorlevel 1 (
    echo    [SKIP] Docker not found (optional)
) else (
    docker --version
    echo    [PASS] Docker installed
)
echo.

REM Check virtual environment
echo [5/8] Checking Python virtual environment...
if exist "venv\" (
    echo    [PASS] Virtual environment exists
) else (
    echo    [WARN] Virtual environment not found (run setup.bat)
)
echo.

REM Check requirements
echo [6/8] Checking Python dependencies...
if exist "requirements.txt" (
    echo    [PASS] requirements.txt found
) else (
    echo    [FAIL] requirements.txt not found
    set /a ERRORS+=1
)
echo.

REM Check model
echo [7/8] Checking trained model...
if exist "models\titanic_model.pkl" (
    echo    [PASS] Trained model exists
) else (
    echo    [WARN] Model not found (run: python train_model.py)
)
echo.

REM Check frontend dependencies
echo [8/8] Checking frontend setup...
if exist "frontend\node_modules\" (
    echo    [PASS] Frontend dependencies installed
) else (
    echo    [WARN] Frontend dependencies not installed (run: cd frontend ^&^& npm install)
)
echo.

echo ========================================
echo   VERIFICATION COMPLETE
echo ========================================

if %ERRORS% EQU 0 (
    echo [SUCCESS] All critical checks passed!
    echo.
    echo Ready to run:
    echo   - Run setup.bat (if not done)
    echo   - Run start.bat to launch app
    echo   - Or use Docker: docker-compose up
) else (
    echo [FAILED] %ERRORS% critical error(s) found
    echo Please install missing dependencies
)
echo ========================================
echo.
pause
