@echo off
echo ========================================
echo Offline Package Installation
echo ========================================
echo.
echo This script will try to install packages
echo that work with your Python 3.13 without
echo requiring internet connection or compilation.
echo.

call venv\Scripts\activate.bat

echo [1/4] Checking what's already installed...
pip list
echo.

echo [2/4] Installing packages that don't need compilation...
pip install --no-deps joblib || echo joblib failed

echo [3/4] For packages requiring internet, you need to:
echo     1. Connect to internet temporarily, OR
echo     2. Download .whl files on another computer, OR  
echo     3. Use Python 3.11 instead of 3.13 (better compatibility)
echo.

echo [4/4] Current status:
python -c "import numpy; print('✓ numpy', numpy.__version__)" 2>nul || echo ✗ numpy MISSING
python -c "import pandas; print('✓ pandas', pandas.__version__)" 2>nul || echo ✗ pandas MISSING  
python -c "import sklearn; print('✓ scikit-learn', sklearn.__version__)" 2>nul || echo ✗ scikit-learn MISSING
python -c "import xgboost; print('✓ xgboost', xgboost.__version__)" 2>nul || echo ✓ xgboost (already installed)
python -c "import lightgbm; print('✓ lightgbm', lightgbm.__version__)" 2>nul || echo ✓ lightgbm (already installed)
python -c "import matplotlib; print('✓ matplotlib', matplotlib.__version__)" 2>nul || echo ✗ matplotlib MISSING
python -c "import joblib; print('✓ joblib', joblib.__version__)" 2>nul || echo ✗ joblib MISSING

echo.
echo ========================================
echo RECOMMENDATION:
echo ========================================
echo Python 3.13 is very new (Nov 2024) and many
echo packages don't have pre-built wheels yet.
echo.
echo OPTIONS:
echo 1. Install Python 3.11 (recommended)
echo 2. Connect to internet to download packages
echo 3. Wait for package maintainers to build 3.13 wheels
echo.
pause
