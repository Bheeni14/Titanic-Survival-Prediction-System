@echo off
echo ========================================
echo Starting Titanic Survival Predictor
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [ERROR] Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start backend in a new window
echo [1/2] Starting backend server...
start "Titanic Backend" cmd /k "cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to start
timeout /t 5 /nobreak >nul

REM Start frontend in a new window
echo [2/2] Starting frontend server...
start "Titanic Frontend" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo Servers are starting!
echo ========================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo Press any key to open the application...
pause >nul

REM Open browser
start http://localhost:3000

echo.
echo Application is running!
echo Close the server windows to stop the application.
echo.
pause
