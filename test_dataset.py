import pandas as pd
import sys

try:
    df = pd.read_csv('train.csv')
    print(f"SUCCESS: Loaded {len(df)} rows")
    print(f"Columns: {list(df.columns)}")
    print(f"Has 'Survived': {'Survived' in df.columns}")
    if 'Survived' in df.columns:
        print(f"Survival rate: {df['Survived'].mean():.2%}")
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
