@echo off
echo ========================================
echo Complete Package Verification
echo ========================================
echo.

call venv\Scripts\activate.bat

echo Checking all required packages...
echo.

python -c "import warnings; warnings.filterwarnings('ignore'); import numpy; print('✓ numpy', numpy.__version__)"
python -c "import warnings; warnings.filterwarnings('ignore'); import pandas; print('✓ pandas', pandas.__version__)"
python -c "import warnings; warnings.filterwarnings('ignore'); import sklearn; print('✓ scikit-learn', sklearn.__version__)"
python -c "import warnings; warnings.filterwarnings('ignore'); import xgboost; print('✓ xgboost', xgboost.__version__)"
python -c "import warnings; warnings.filterwarnings('ignore'); import lightgbm; print('✓ lightgbm', lightgbm.__version__)"
python -c "import warnings; warnings.filterwarnings('ignore'); import matplotlib; print('✓ matplotlib', matplotlib.__version__)"
python -c "import warnings; warnings.filterwarnings('ignore'); import seaborn; print('✓ seaborn', seaborn.__version__)"
python -c "import warnings; warnings.filterwarnings('ignore'); import plotly; print('✓ plotly', plotly.__version__)"
python -c "import warnings; warnings.filterwarnings('ignore'); import joblib; print('✓ joblib', joblib.__version__)"
python -c "import warnings; warnings.filterwarnings('ignore'); import fastapi; print('✓ fastapi', fastapi.__version__)"

echo.
echo ========================================
echo Checking for Titanic dataset...
echo ========================================
if exist data\titanic.csv (
    echo ✓ data\titanic.csv found
    for %%A in (data\titanic.csv) do echo    File size: %%~zA bytes
    echo.
    echo ✅ READY TO TRAIN! Run:
    echo    python train_model.py
) else (
    echo ✗ data\titanic.csv NOT FOUND
    echo.
    echo 📥 DOWNLOAD REQUIRED:
    echo.
    echo Option 1: Download from Kaggle
    echo   1. Visit: https://www.kaggle.com/c/titanic/data
    echo   2. Download train.csv
    echo   3. Run these commands:
    echo      mkdir data
    echo      move Downloads\train.csv data\titanic.csv
    echo.
    echo Option 2: Use sample data (demo only)
    echo   Run: python create_sample_data.py
)

echo.
pause
