import warnings
warnings.filterwarnings('ignore')
import os
os.environ['PYTHONWARNINGS'] = 'ignore'

print("="*60)
print("TESTING SCRIPT")
print("="*60)

# Test imports
print("\nTesting imports...")
try:
    import pandas as pd
    print("✓ pandas imported")
except Exception as e:
    print(f"✗ pandas failed: {e}")

try:
    import numpy as np
    print("✓ numpy imported")
except Exception as e:
    print(f"✗ numpy failed: {e}")

try:
    import sklearn
    print(f"✓ scikit-learn {sklearn.__version__} imported")
except Exception as e:
    print(f"✗ scikit-learn failed: {e}")

# Check for train.csv
print("\nChecking for data files...")
if os.path.exists('train.csv'):
    df = pd.read_csv('train.csv')
    print(f"✓ train.csv found: {len(df)} rows, {len(df.columns)} columns")
    print(f"  Columns: {', '.join(df.columns[:5])}...")
    if 'Survived' in df.columns:
        print(f"  Survival rate: {df['Survived'].mean():.1%}")
else:
    print("✗ train.csv not found in current directory")

print("\n" + "="*60)
print("Ready to train! Run: python train_model.py")
print("="*60)
