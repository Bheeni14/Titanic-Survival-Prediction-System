"""
Advanced Titanic Survival Prediction Model Training
Features: XGBoost, LightGBM, Feature Engineering, Hyperparameter Tuning
"""

import warnings
warnings.filterwarnings('ignore')
import os
os.environ['PYTHONWARNINGS'] = 'ignore'

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
import xgboost as xgb
import lightgbm as lgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os
from pathlib import Path

warnings.filterwarnings('ignore')

class TitanicModelTrainer:
    """Advanced Titanic Survival Prediction Model with Feature Engineering"""
    
    def __init__(self):
        self.models = {}
        self.best_model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []
        
    def create_features(self, df):
        """Advanced feature engineering"""
        df = df.copy()
        
        # Fill missing values
        df['Age'].fillna(df['Age'].median(), inplace=True)
        df['Fare'].fillna(df['Fare'].median(), inplace=True)
        df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
        
        # Extract titles from names
        df['Title'] = df['Name'].str.extract(r' ([A-Za-z]+)\.', expand=False)
        df['Title'] = df['Title'].replace(['Lady', 'Countess','Capt', 'Col',
                                           'Don', 'Dr', 'Major', 'Rev', 'Sir',
                                           'Jonkheer', 'Dona'], 'Rare')
        df['Title'] = df['Title'].replace('Mlle', 'Miss')
        df['Title'] = df['Title'].replace('Ms', 'Miss')
        df['Title'] = df['Title'].replace('Mme', 'Mrs')
        
        # Family features
        df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
        df['IsAlone'] = (df['FamilySize'] == 1).astype(int)
        df['SmallFamily'] = ((df['FamilySize'] >= 2) & (df['FamilySize'] <= 4)).astype(int)
        df['LargeFamily'] = (df['FamilySize'] >= 5).astype(int)
        
        # Age groups
        df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 12, 18, 35, 60, 100],
                                labels=['Child', 'Teen', 'Adult', 'Middle', 'Senior'])
        
        # Fare bins
        df['FareBin'] = pd.qcut(df['Fare'], q=5, labels=['Very_Low', 'Low', 'Medium', 'High', 'Very_High'])
        
        # Interaction features
        df['Age_Class'] = df['Age'] * df['Pclass']
        df['Fare_Per_Person'] = df['Fare'] / df['FamilySize']
        
        # Cabin features
        if 'Cabin' in df.columns:
            df['HasCabin'] = df['Cabin'].notna().astype(int)
            df['CabinDeck'] = df['Cabin'].str[0].fillna('Unknown')
        else:
            df['HasCabin'] = 0
            df['CabinDeck'] = 'Unknown'
        
        # Sex to binary
        df['Sex_Binary'] = (df['Sex'] == 'male').astype(int)
        
        return df
    
    def prepare_data(self, df, is_training=True):
        """Prepare data for training or prediction"""
        df = self.create_features(df)
        
        # Select features
        categorical_features = ['Embarked', 'Title', 'AgeGroup', 'FareBin', 'CabinDeck']
        numerical_features = ['Pclass', 'Age', 'SibSp', 'Parch', 'Fare', 
                             'FamilySize', 'IsAlone', 'SmallFamily', 'LargeFamily',
                             'Age_Class', 'Fare_Per_Person', 'HasCabin', 'Sex_Binary']
        
        # Encode categorical features
        for col in categorical_features:
            if is_training:
                self.label_encoders[col] = LabelEncoder()
                df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
            else:
                # Handle unseen categories
                df[col] = df[col].astype(str)
                df[col] = df[col].apply(lambda x: x if x in self.label_encoders[col].classes_ 
                                       else self.label_encoders[col].classes_[0])
                df[col] = self.label_encoders[col].transform(df[col])
        
        self.feature_names = numerical_features + categorical_features
        X = df[self.feature_names]
        
        if is_training:
            X = self.scaler.fit_transform(X)
        else:
            X = self.scaler.transform(X)
        
        return X
    
    def train_models(self, X_train, y_train, X_test, y_test):
        """Train multiple models with hyperparameter tuning"""
        print("🚀 Training Advanced ML Models...\n")
        
        # 1. Logistic Regression
        print("1️⃣  Training Logistic Regression...")
        lr_params = {
            'C': [0.01, 0.1, 1, 10],
            'penalty': ['l2'],
            'solver': ['lbfgs'],
            'max_iter': [1000]
        }
        lr = GridSearchCV(LogisticRegression(random_state=42), lr_params, cv=5, scoring='accuracy')
        lr.fit(X_train, y_train)
        self.models['logistic_regression'] = lr.best_estimator_
        print(f"   ✅ Best params: {lr.best_params_}")
        
        # 2. Random Forest
        print("\n2️⃣  Training Random Forest...")
        rf = RandomForestClassifier(
            n_estimators=300,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        rf.fit(X_train, y_train)
        self.models['random_forest'] = rf
        print("   ✅ Training complete")
        
        # 3. XGBoost
        print("\n3️⃣  Training XGBoost...")
        xgb_model = xgb.XGBClassifier(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=6,
            min_child_weight=3,
            gamma=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            objective='binary:logistic',
            random_state=42,
            n_jobs=-1
        )
        xgb_model.fit(X_train, y_train)
        self.models['xgboost'] = xgb_model
        print("   ✅ Training complete")
        
        # 4. LightGBM
        print("\n4️⃣  Training LightGBM...")
        lgb_model = lgb.LGBMClassifier(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=6,
            num_leaves=31,
            min_child_samples=20,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1,
            verbose=-1
        )
        lgb_model.fit(X_train, y_train)
        self.models['lightgbm'] = lgb_model
        print("   ✅ Training complete")
        
        # 5. Stacked Ensemble
        print("\n5️⃣  Training Stacked Ensemble...")
        ensemble = VotingClassifier(
            estimators=[
                ('lr', self.models['logistic_regression']),
                ('rf', self.models['random_forest']),
                ('xgb', self.models['xgboost']),
                ('lgb', self.models['lightgbm'])
            ],
            voting='soft',
            n_jobs=-1
        )
        ensemble.fit(X_train, y_train)
        self.models['ensemble'] = ensemble
        print("   ✅ Training complete")
        
        # Evaluate all models
        print("\n" + "="*60)
        print("📊 MODEL PERFORMANCE COMPARISON")
        print("="*60)
        
        best_accuracy = 0
        for name, model in self.models.items():
            y_pred = model.predict(X_test)
            y_proba = model.predict_proba(X_test)[:, 1]
            
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            roc_auc = roc_auc_score(y_test, y_proba)
            
            print(f"\n{name.upper().replace('_', ' ')}")
            print(f"  Accuracy:  {accuracy:.4f}")
            print(f"  Precision: {precision:.4f}")
            print(f"  Recall:    {recall:.4f}")
            print(f"  F1-Score:  {f1:.4f}")
            print(f"  ROC-AUC:   {roc_auc:.4f}")
            
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                self.best_model = model
                self.best_model_name = name
        
        print("\n" + "="*60)
        print(f"🏆 Best Model: {self.best_model_name.upper().replace('_', ' ')}")
        print(f"🎯 Best Accuracy: {best_accuracy:.4f}")
        print("="*60)
    
    def generate_visualizations(self, X_test, y_test):
        """Generate model visualizations"""
        print("\n📈 Generating Visualizations...")
        
        # Create output directory
        output_dir = Path('models/visualizations')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        y_pred = self.best_model.predict(X_test)
        y_proba = self.best_model.predict_proba(X_test)[:, 1]
        
        # 1. Confusion Matrix
        plt.figure(figsize=(8, 6))
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
        plt.title('Confusion Matrix', fontsize=16, fontweight='bold')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig(output_dir / 'confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. ROC Curve
        plt.figure(figsize=(8, 6))
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        roc_auc = roc_auc_score(y_test, y_proba)
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve', fontsize=16, fontweight='bold')
        plt.legend(loc="lower right")
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_dir / 'roc_curve.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Feature Importance
        if hasattr(self.best_model, 'feature_importances_'):
            plt.figure(figsize=(10, 8))
            importance = self.best_model.feature_importances_
            indices = np.argsort(importance)[::-1][:15]
            
            plt.barh(range(len(indices)), importance[indices], color='steelblue')
            plt.yticks(range(len(indices)), [self.feature_names[i] for i in indices])
            plt.xlabel('Feature Importance')
            plt.title('Top 15 Feature Importance', fontsize=16, fontweight='bold')
            plt.gca().invert_yaxis()
            plt.tight_layout()
            plt.savefig(output_dir / 'feature_importance.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        print(f"   ✅ Visualizations saved to {output_dir}")
    
    def save_model(self, output_path='models/titanic_model.pkl'):
        """Save the best model and preprocessors"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        model_package = {
            'model': self.best_model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_names': self.feature_names,
            'model_name': self.best_model_name
        }
        
        joblib.dump(model_package, output_path)
        print(f"\n💾 Model saved to {output_path}")
    
    def load_model(self, model_path='models/titanic_model.pkl'):
        """Load a trained model"""
        model_package = joblib.load(model_path)
        self.best_model = model_package['model']
        self.scaler = model_package['scaler']
        self.label_encoders = model_package['label_encoders']
        self.feature_names = model_package['feature_names']
        self.best_model_name = model_package['model_name']
        print(f"✅ Model loaded from {model_path}")


def download_titanic_data():
    """Load Titanic dataset from multiple possible locations"""
    # Try multiple possible locations
    possible_paths = [
        'train.csv',                    # Root directory
        'data/train.csv',               # Data subdirectory
        'data/titanic.csv',             # Alternative name
        Path('data') / 'titanic.csv',   # Using Path object
    ]
    
    for csv_path in possible_paths:
        if Path(csv_path).exists():
            print(f"✅ Loading data from {csv_path}")
            df = pd.read_csv(csv_path)
            print(f"   Records: {len(df)} | Features: {len(df.columns)}")
            return df
    
    # Try to load from seaborn as fallback
    try:
        import seaborn as sns
        df = sns.load_dataset('titanic')
        data_path = Path('data')
        data_path.mkdir(exist_ok=True)
        csv_path = data_path / 'titanic.csv'
        df.to_csv(csv_path, index=False)
        print(f"✅ Downloaded Titanic dataset to {csv_path}")
        return df
    except:
        print("❌ Dataset not found! Please ensure train.csv is available.")
        return None


def main():
    """Main training pipeline"""
    print("\n" + "="*60)
    print("🚢 TITANIC SURVIVAL PREDICTION MODEL TRAINING")
    print("="*60 + "\n")
    
    # Load data
    df = download_titanic_data()
    if df is None:
        return
    
    print(f"📊 Dataset shape: {df.shape}")
    print(f"📊 Survival rate: {df['Survived'].mean():.2%}\n")
    
    # Initialize trainer
    trainer = TitanicModelTrainer()
    
    # Prepare data
    print("🔧 Preparing data with advanced feature engineering...")
    X = trainer.prepare_data(df, is_training=True)
    y = df['Survived'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   Train set: {X_train.shape[0]} samples")
    print(f"   Test set:  {X_test.shape[0]} samples")
    
    # Train models
    trainer.train_models(X_train, y_train, X_test, y_test)
    
    # Generate visualizations
    trainer.generate_visualizations(X_test, y_test)
    
    # Save model
    trainer.save_model()
    
    print("\n✨ Training complete! Ready for deployment.\n")


if __name__ == "__main__":
    main()
