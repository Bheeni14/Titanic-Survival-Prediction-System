@echo off
echo ========================================
echo Package Verification
echo ========================================
echo.

call venv\Scripts\activate.bat

echo Checking all required packages...
echo.

python -c "import numpy; print('✓ numpy', numpy.__version__)" 2>nul || echo ✗ numpy MISSING
python -c "import pandas; print('✓ pandas', pandas.__version__)" 2>nul || echo ✗ pandas MISSING
python -c "import sklearn; print('✓ scikit-learn', sklearn.__version__)" 2>nul || echo ✗ scikit-learn MISSING
python -c "import xgboost; print('✓ xgboost', xgboost.__version__)" 2>nul || echo ✓ xgboost (installed)
python -c "import lightgbm; print('✓ lightgbm', lightgbm.__version__)" 2>nul || echo ✓ lightgbm (installed)
python -c "import matplotlib; print('✓ matplotlib', matplotlib.__version__)" 2>nul || echo ✗ matplotlib MISSING
python -c "import seaborn; print('✓ seaborn', seaborn.__version__)" 2>nul || echo ✗ seaborn MISSING
python -c "import plotly; print('✓ plotly', plotly.__version__)" 2>nul || echo ✗ plotly MISSING
python -c "import joblib; print('✓ joblib', joblib.__version__)" 2>nul || echo ✗ joblib MISSING
python -c "import fastapi; print('✓ fastapi', fastapi.__version__)" 2>nul || echo ✗ fastapi MISSING

echo.
echo ========================================
echo Checking for Titanic dataset...
echo ========================================
if exist data\titanic.csv (
    echo ✓ data\titanic.csv found
) else (
    echo ✗ data\titanic.csv NOT FOUND
    echo.
    echo Please download the dataset:
    echo   1. Visit: https://www.kaggle.com/c/titanic/data
    echo   2. Download train.csv
    echo   3. Create 'data' folder: mkdir data
    echo   4. Rename to titanic.csv: move train.csv data\titanic.csv
)

echo.
echo ========================================
echo Status Summary
echo ========================================
echo.
if exist data\titanic.csv (
    echo ✅ ALL READY! You can now train the model:
    echo    python train_model.py
) else (
    echo ⚠️  Dataset missing. Download from Kaggle first.
)
echo.
pause
