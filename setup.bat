@echo off
echo ========================================
echo Titanic Survival Predictor - Setup
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Upgrading pip...
python -m pip install --upgrade pip

echo [4/5] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [5/5] Training ML model...
python train_model.py
if errorlevel 1 (
    echo [ERROR] Model training failed
    pause
    exit /b 1
)

echo [6/6] Setup complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo 1. Start the backend:
echo    cd backend
echo    uvicorn main:app --reload
echo.
echo 2. In a new terminal, start the frontend:
echo    cd frontend
echo    npm install
echo    npm start
echo.
echo 3. Open http://localhost:3000 in your browser
echo ========================================
pause
