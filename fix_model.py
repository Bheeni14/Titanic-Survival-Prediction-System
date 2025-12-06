"""
Fix the saved model to be compatible with backend
"""
import joblib
import os

# Load the emergency model
model_data = joblib.load('models/titanic_model.pkl')

# Add missing components the backend expects
model_data['label_encoders'] = {}  # Empty dict since we used one-hot encoding
model_data['model_name'] = 'XGBoost'

# Resave
joblib.dump(model_data, 'models/titanic_model.pkl')
print("✅ Model fixed and saved")
print("   Added 'label_encoders' and 'model_name' keys")
