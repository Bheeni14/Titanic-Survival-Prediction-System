@echo off
echo ========================================
echo Quick Fix - Installing Dependencies
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

echo [1/3] Upgrading pip...
python -m pip install --upgrade pip

echo [2/3] Installing core dependencies...
pip install numpy>=1.24.0,<2.0.0
pip install pandas>=2.0.0,<2.3.0
pip install scikit-learn==1.3.2
pip install xgboost==2.0.3
pip install lightgbm==4.1.0

echo [3/3] Installing remaining dependencies...
pip install fastapi==0.109.0
pip install uvicorn[standard]==0.27.0
pip install pydantic==2.5.3
pip install python-multipart==0.0.6
pip install matplotlib==3.8.2
pip install seaborn==0.13.1
pip install plotly==5.18.0
pip install joblib==1.3.2

echo.
echo ========================================
echo Dependencies installed successfully!
echo ========================================
echo.
echo Next step: Run model training
echo    python train_model.py
echo.
pause
