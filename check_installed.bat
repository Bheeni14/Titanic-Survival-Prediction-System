@echo off
echo ========================================
echo Checking Installed Packages
echo ========================================
echo.

call venv\Scripts\activate.bat

echo Checking Python version:
python --version
echo.

echo Installed packages:
pip list
echo.

echo ========================================
echo Critical packages for training:
echo ========================================
python -c "import sys; packages = ['numpy', 'pandas', 'sklearn', 'xgboost', 'lightgbm', 'matplotlib', 'seaborn', 'plotly', 'joblib']; [print(f'✓ {pkg}') if __import__('importlib').util.find_spec(pkg.replace('sklearn', 'scikit-learn')) else print(f'✗ {pkg} - MISSING') for pkg in packages]" 2>nul || echo Some packages missing

echo.
pause
