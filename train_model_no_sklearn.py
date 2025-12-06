"""
Training script that works WITHOUT scikit-learn.
Uses only XGBoost and LightGBM (already installed).
"""

import numpy as np
import pandas as pd
import xgboost as xgb
import lightgbm as lgb
import joblib
import os

class TitanicModelTrainerNoSklearn:
    """Train Titanic model using only XGBoost and LightGBM"""
    
    def __init__(self):
        self.xgb_model = None
        self.lgb_model = None
        self.best_model = None
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
                                labels=[0, 1, 2, 3, 4])
        
        # Fare per person
        df['FarePerPerson'] = df['Fare'] / df['FamilySize']
        
        # Cabin feature
        df['HasCabin'] = df['Cabin'].notna().astype(int)
        
        # Encode categorical
        df = pd.get_dummies(df, columns=['Sex', 'Embarked', 'Title', 'AgeGroup'],
                           drop_first=False)
        
        return df
    
    def train_test_split_manual(self, X, y, test_size=0.2, random_state=42):
        """Manual train-test split"""
        np.random.seed(random_state)
        indices = np.random.permutation(len(X))
        test_size_count = int(len(X) * test_size)
        
        test_indices = indices[:test_size_count]
        train_indices = indices[test_size_count:]
        
        if isinstance(X, pd.DataFrame):
            X_train = X.iloc[train_indices]
            X_test = X.iloc[test_indices]
        else:
            X_train = X[train_indices]
            X_test = X[test_indices]
            
        if isinstance(y, pd.Series):
            y_train = y.iloc[train_indices]
            y_test = y.iloc[test_indices]
        else:
            y_train = y[train_indices]
            y_test = y[test_indices]
        
        return X_train, X_test, y_train, y_test
    
    def calculate_accuracy(self, y_true, y_pred):
        """Calculate accuracy"""
        return np.mean(y_true == y_pred)
    
    def train_models(self, X_train, y_train):
        """Train XGBoost and LightGBM"""
        print("\n🔄 Training models...")
        
        # XGBoost
        print("  Training XGBoost...")
        self.xgb_model = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.1,
            random_state=42,
            eval_metric='logloss'
        )
        self.xgb_model.fit(X_train, y_train)
        
        # LightGBM
        print("  Training LightGBM...")
        self.lgb_model = lgb.LGBMClassifier(
            n_estimators=200,
            max_depth=7,
            learning_rate=0.1,
            random_state=42,
            verbose=-1
        )
        self.lgb_model.fit(X_train, y_train)
    
    def evaluate_models(self, X_test, y_test):
        """Evaluate both models"""
        print("\n📊 Model Performance:")
        print("=" * 60)
        
        # XGBoost
        xgb_pred = self.xgb_model.predict(X_test)
        xgb_acc = self.calculate_accuracy(y_test, xgb_pred)
        print(f"\nXGBoost:")
        print(f"  Accuracy: {xgb_acc:.4f}")
        
        # LightGBM
        lgb_pred = self.lgb_model.predict(X_test)
        lgb_acc = self.calculate_accuracy(y_test, lgb_pred)
        print(f"\nLightGBM:")
        print(f"  Accuracy: {lgb_acc:.4f}")
        
        # Choose best
        if xgb_acc > lgb_acc:
            self.best_model = self.xgb_model
            print(f"\n⭐ Best Model: XGBoost ({xgb_acc:.4f})")
        else:
            self.best_model = self.lgb_model
            print(f"\n⭐ Best Model: LightGBM ({lgb_acc:.4f})")
        
        print("=" * 60)
    
    def save_model(self, filepath='models/titanic_model.pkl'):
        """Save the best model"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        model_data = {
            'model': self.best_model,
            'xgb_model': self.xgb_model,
            'lgb_model': self.lgb_model,
            'feature_names': self.feature_names,
            'scaler': None  # Compatibility with original
        }
        
        joblib.dump(model_data, filepath)
        print(f"\n✅ Model saved to: {filepath}")


def main():
    print("=" * 60)
    print("🚢 TITANIC SURVIVAL PREDICTION - TRAINING")
    print("   (XGBoost + LightGBM version)")
    print("=" * 60)
    
    # Load data
    print("\n📂 Loading data...")
    try:
        df = pd.read_csv('data/titanic.csv')
        print(f"  Loaded {len(df)} records")
    except FileNotFoundError:
        print("❌ ERROR: data/titanic.csv not found!")
        print("\n📥 Please download the Titanic dataset:")
        print("   1. Go to: https://www.kaggle.com/c/titanic/data")
        print("   2. Download train.csv")
        print("   3. Create 'data' folder")
        print("   4. Rename to titanic.csv and place in data folder")
        return
    
    # Initialize trainer
    trainer = TitanicModelTrainerNoSklearn()
    
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
    X_train, X_test, y_train, y_test = trainer.train_test_split_manual(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"  Training set: {len(X_train)} samples")
    print(f"  Test set: {len(X_test)} samples")
    print(f"  Features: {len(feature_cols)}")
    
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
    print("  1. Model saved successfully")
    print("  2. Start backend: cd backend && uvicorn main:app --reload")
    print("  3. Access API docs: http://localhost:8000/docs")
    
    print("\n💡 Note: This version uses XGBoost + LightGBM")
    print("   (No scikit-learn required)")


if __name__ == "__main__":
    main()
