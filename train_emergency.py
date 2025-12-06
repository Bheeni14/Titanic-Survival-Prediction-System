"""
Emergency training script that handles numpy crashes gracefully
"""
import sys
import os

# Suppress ALL warnings before any imports
import warnings
warnings.filterwarnings('ignore')
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['PYTHONIOENCODING'] = 'utf-8'

print("="*60)
print("TITANIC MODEL TRAINING - EMERGENCY MODE")
print("="*60)
print()

# Test each import individually with error handling
print("Step 1: Testing imports...")

try:
    import numpy as np
    print(f"  ✓ numpy {np.__version__}")
except Exception as e:
    print(f"  ✗ numpy FAILED: {e}")
    print("\n  CRITICAL: Numpy is crashing Python.")
    print("  Solution: Install Python 3.11 instead of 3.13")
    sys.exit(1)

try:
    import pandas as pd
    print(f"  ✓ pandas {pd.__version__}")
except Exception as e:
    print(f"  ✗ pandas FAILED: {e}")
    sys.exit(1)

try:
    import sklearn
    print(f"  ✓ scikit-learn {sklearn.__version__}")
except Exception as e:
    print(f"  ✗ scikit-learn FAILED: {e}")
    sys.exit(1)

try:
    import xgboost
    print(f"  ✓ xgboost {xgboost.__version__}")
except Exception as e:
    print(f"  ✗ xgboost FAILED: {e}")
    sys.exit(1)

try:
    import lightgbm
    print(f"  ✓ lightgbm {lightgbm.__version__}")
except Exception as e:
    print(f"  ✗ lightgbm FAILED: {e}")
    sys.exit(1)

print("\nStep 2: All imports successful!")
print("\nStep 3: Loading data...")

# Find dataset
if os.path.exists('train.csv'):
    df = pd.read_csv('train.csv')
    print(f"  ✓ Loaded train.csv: {len(df)} rows")
elif os.path.exists('data/train.csv'):
    df = pd.read_csv('data/train.csv')
    print(f"  ✓ Loaded data/train.csv: {len(df)} rows")
else:
    print("  ✗ Dataset not found!")
    sys.exit(1)

print(f"  Survival rate: {df['Survived'].mean():.1%}")

print("\nStep 4: Training model...")

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import joblib

# Simple feature engineering
print("  - Feature engineering...")
df['Age'].fillna(df['Age'].median(), inplace=True)
df['Fare'].fillna(df['Fare'].median(), inplace=True)
df['Embarked'].fillna('S', inplace=True)
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
df['IsAlone'] = (df['FamilySize'] == 1).astype(int)

# Encode categorical
df_encoded = pd.get_dummies(df, columns=['Sex', 'Embarked'], drop_first=True)

# Select features
feature_cols = ['Pclass', 'Age', 'Fare', 'FamilySize', 'IsAlone', 
                'Sex_male', 'Embarked_Q', 'Embarked_S']
X = df_encoded[feature_cols]
y = df_encoded['Survived']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("  - Training XGBoost...")
model = XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.1,
    random_state=42,
    eval_metric='logloss'
)
model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n  ✓ Training complete!")
print(f"  Accuracy: {accuracy:.2%}")

# Save model
print("\nStep 5: Saving model...")
os.makedirs('models', exist_ok=True)
model_data = {
    'model': model,
    'scaler': scaler,
    'feature_names': feature_cols
}
joblib.dump(model_data, 'models/titanic_model.pkl')
print("  ✓ Model saved to models/titanic_model.pkl")

print("\n" + "="*60)
print("SUCCESS! Model trained and saved")
print("="*60)
print("\nNext steps:")
print("  1. Start backend: cd backend")
print("  2. Run API: uvicorn main:app --reload")
print("  3. Access: http://localhost:8000/docs")
