@echo off
echo ========================================
echo Install scikit-learn for Python 3.13
echo ========================================
echo.

call venv\Scripts\activate.bat

echo Trying to install scikit-learn pre-release with 3.13 support...
echo.

REM Try installing the latest version that may have 3.13 wheels
pip install --pre scikit-learn

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo ✅ SUCCESS! scikit-learn installed
    echo ========================================
    echo.
    echo Verifying installation:
    python -c "import sklearn; print('✓ scikit-learn version:', sklearn.__version__)"
    echo.
    echo Next step: Train the model
    echo    python train_model.py
) else (
    echo.
    echo ========================================
    echo ❌ Installation failed
    echo ========================================
    echo.
    echo OPTION 1: Use minimal training (no sklearn)
    echo    We can modify code to use XGBoost/LightGBM only
    echo.
    echo OPTION 2: Install Python 3.11
    echo    Download from python.org and recreate venv
    echo.
    echo OPTION 3: Try nightly build
    echo    pip install --pre --extra-index-url https://pypi.anaconda.org/scientific-python-nightly-wheels/simple scikit-learn
)

echo.
pause
