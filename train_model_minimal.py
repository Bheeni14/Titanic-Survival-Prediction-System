"""
Simplified training script without visualization dependencies.
Works with minimal Python installation.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score

try:
    import xgboost as xgb
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False
    print("⚠️  XGBoost not available - using only sklearn models")

try:
    import lightgbm as lgb
    HAS_LIGHTGBM = True
except ImportError:
    HAS_LIGHTGBM = False
    print("⚠️  LightGBM not available - using only sklearn models")

try:
    import joblib
    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False
    print("⚠️  Joblib not available - model won't be saved")


class TitanicModelTrainerMinimal:
    """Minimal version without visualization dependencies"""
    
    def __init__(self):
        self.models = {}
        self.best_model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        
    def create_features(self, df):
        """Feature engineering"""
        df = df.copy()
        
        # Fill missing values
        df['Age'].fillna(df['Age'].median(), inplace=True)
        df['Fare'].fillna(df['Fare'].median(), inplace=True)
        df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
        
        # Extract title
        df['Title'] = df['Name'].str.extract(r' ([A-Za-z]+)\.', expand=False)
        df['Title'] = df['Title'].replace(['Lady', 'Countess', 'Capt', 'Col',
                                           'Don', 'Dr', 'Major', 'Rev', 'Sir',
                                           'Jonkheer', 'Dona'], 'Rare')
        df['Title'] = df['Title'].replace('Mlle', 'Miss')
        df['Title'] = df['Title'].replace('Ms', 'Miss')
        df['Title'] = df['Title'].replace('Mme', 'Mrs')
        
        # Family features
        df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
        df['IsAlone'] = (df['FamilySize'] == 1).astype(int)
        
        # Age groups
        df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 12, 20, 40, 60, 100],
                                labels=['Child', 'Teen', 'Adult', 'Middle', 'Senior'])
        
        # Fare per person
        df['FarePerPerson'] = df['Fare'] / df['FamilySize']
        
        # Cabin feature
        df['HasCabin'] = df['Cabin'].notna().astype(int)
        
        # Encode categorical
        df = pd.get_dummies(df, columns=['Sex', 'Embarked', 'Title', 'AgeGroup'],
                           drop_first=False)
        
        return df
    
    def train_models(self, X_train, y_train):
        """Train multiple models"""
        print("\n🔄 Training models...")
        
        # Logistic Regression
        print("  Training Logistic Regression...")
        lr_params = {'C': [0.001, 0.01, 0.1, 1, 10], 'max_iter': [1000]}
        lr = GridSearchCV(LogisticRegression(random_state=42), lr_params, cv=5, n_jobs=-1)
        lr.fit(X_train, y_train)
        self.models['Logistic Regression'] = lr.best_estimator_
        
        # Random Forest
        print("  Training Random Forest...")
        rf_params = {'n_estimators': [100, 200], 'max_depth': [5, 10, None],
                    'min_samples_split': [2, 5]}
        rf = GridSearchCV(RandomForestClassifier(random_state=42), rf_params, cv=5, n_jobs=-1)
        rf.fit(X_train, y_train)
        self.models['Random Forest'] = rf.best_estimator_
        
        # XGBoost
        if HAS_XGBOOST:
            print("  Training XGBoost...")
            xgb_params = {'n_estimators': [100, 200], 'max_depth': [3, 5, 7],
                         'learning_rate': [0.01, 0.1]}
            xgb_model = GridSearchCV(xgb.XGBClassifier(random_state=42, eval_metric='logloss'),
                                    xgb_params, cv=5, n_jobs=-1)
            xgb_model.fit(X_train, y_train)
            self.models['XGBoost'] = xgb_model.best_estimator_
        
        # LightGBM
        if HAS_LIGHTGBM:
            print("  Training LightGBM...")
            lgb_params = {'n_estimators': [100, 200], 'max_depth': [5, 10],
                         'learning_rate': [0.01, 0.1]}
            lgb_model = GridSearchCV(lgb.LGBMClassifier(random_state=42, verbose=-1),
                                    lgb_params, cv=5, n_jobs=-1)
            lgb_model.fit(X_train, y_train)
            self.models['LightGBM'] = lgb_model.best_estimator_
    
    def evaluate_models(self, X_test, y_test):
        """Evaluate all models"""
        print("\n📊 Model Performance:")
        print("=" * 60)
        
        best_score = 0
        for name, model in self.models.items():
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            try:
                y_pred_proba = model.predict_proba(X_test)[:, 1]
                roc_auc = roc_auc_score(y_test, y_pred_proba)
            except:
                roc_auc = 0.0
            
            print(f"\n{name}:")
            print(f"  Accuracy: {accuracy:.4f}")
            if roc_auc > 0:
                print(f"  ROC-AUC:  {roc_auc:.4f}")
            
            if accuracy > best_score:
                best_score = accuracy
                self.best_model = model
                print(f"  ⭐ New best model!")
        
        print("\n" + "=" * 60)
        print(f"Best Model Accuracy: {best_score:.4f}")
    
    def save_model(self, filepath='models/titanic_model_minimal.pkl'):
        """Save the best model"""
        if not HAS_JOBLIB:
            print("⚠️  Cannot save model - joblib not available")
            return
            
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        model_data = {
            'model': self.best_model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'models': self.models
        }
        
        joblib.dump(model_data, filepath)
        print(f"\n✅ Model saved to: {filepath}")


def main():
    print("=" * 60)
    print("🚢 TITANIC SURVIVAL PREDICTION - MINIMAL TRAINING")
    print("=" * 60)
    
    # Load data
    print("\n📂 Loading data...")
    try:
        df = pd.read_csv('data/titanic.csv')
        print(f"  Loaded {len(df)} records")
    except FileNotFoundError:
        print("❌ ERROR: data/titanic.csv not found!")
        print("   Download from: https://www.kaggle.com/c/titanic/data")
        return
    
    # Initialize trainer
    trainer = TitanicModelTrainerMinimal()
    
    # Feature engineering
    print("\n🔧 Creating features...")
    df_processed = trainer.create_features(df)
    
    # Prepare features
    feature_cols = [col for col in df_processed.columns 
                   if col not in ['Survived', 'PassengerId', 'Name', 'Ticket', 'Cabin']]
    
    X = df_processed[feature_cols].fillna(0)
    y = df_processed['Survived']
    
    trainer.feature_names = feature_cols
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    X_train = trainer.scaler.fit_transform(X_train)
    X_test = trainer.scaler.transform(X_test)
    
    print(f"  Training set: {len(X_train)} samples")
    print(f"  Test set: {len(X_test)} samples")
    
    # Train models
    trainer.train_models(X_train, y_train)
    
    # Evaluate
    trainer.evaluate_models(X_test, y_test)
    
    # Save model
    trainer.save_model()
    
    print("\n" + "=" * 60)
    print("✅ TRAINING COMPLETE!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Model is ready for predictions")
    print("  2. Install visualization packages for charts (optional)")
    print("  3. Start the backend API (requires fastapi)")


if __name__ == "__main__":
    main()
