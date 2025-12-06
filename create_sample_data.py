"""
Create a small sample Titanic dataset for testing/demo purposes.
This is NOT the real Kaggle dataset but allows you to test the pipeline.
"""

import pandas as pd
import os

# Create sample data matching Titanic structure
sample_data = {
    'PassengerId': range(1, 101),
    'Survived': [0, 1, 1, 1, 0, 0, 0, 0, 1, 1] * 10,
    'Pclass': [3, 1, 3, 1, 3, 3, 1, 3, 3, 2] * 10,
    'Name': [
        'Braund, Mr. Owen Harris',
        'Cumings, Mrs. John Bradley (Florence Briggs Thayer)',
        'Heikkinen, Miss. Laina',
        'Futrelle, Mrs. Jacques Heath (Lily May Peel)',
        'Allen, Mr. William Henry',
        'Moran, Mr. James',
        'McCarthy, Mr. Timothy J',
        'Palsson, Master. Gosta Leonard',
        'Johnson, Mrs. Oscar W (Elisabeth Vilhelmina Berg)',
        'Nasser, Mrs. Nicholas (Adele Achem)'
    ] * 10,
    'Sex': ['male', 'female', 'female', 'female', 'male', 'male', 'male', 'male', 'female', 'female'] * 10,
    'Age': [22, 38, 26, 35, 35, None, 54, 2, 27, 14] * 10,
    'SibSp': [1, 1, 0, 1, 0, 0, 0, 3, 0, 1] * 10,
    'Parch': [0, 0, 0, 0, 0, 0, 0, 1, 2, 0] * 10,
    'Ticket': ['A/5 21171', 'PC 17599', 'STON/O2. 3101282', '113803', '373450', 
               '330877', '17463', '349909', '347742', '237736'] * 10,
    'Fare': [7.25, 71.28, 7.92, 53.10, 8.05, 8.46, 51.86, 21.08, 11.13, 30.07] * 10,
    'Cabin': [None, 'C85', None, 'C123', None, None, 'E46', None, None, None] * 10,
    'Embarked': ['S', 'C', 'S', 'S', 'S', 'Q', 'S', 'S', 'S', 'C'] * 10
}

# Create DataFrame
df = pd.DataFrame(sample_data)

# Create data directory
os.makedirs('data', exist_ok=True)

# Save to CSV
df.to_csv('data/titanic.csv', index=False)

print("=" * 60)
print("✅ Sample dataset created: data/titanic.csv")
print("=" * 60)
print(f"  Records: {len(df)}")
print(f"  Features: {len(df.columns)}")
print(f"  Survivors: {df['Survived'].sum()}/{len(df)} ({df['Survived'].mean()*100:.1f}%)")
print()
print("⚠️  NOTE: This is SAMPLE data for testing only!")
print("   For real training, download from Kaggle:")
print("   https://www.kaggle.com/c/titanic/data")
print()
print("Next step: python train_model.py")
