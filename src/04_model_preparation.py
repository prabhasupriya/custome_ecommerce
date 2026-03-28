import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import json
import os

def prepare_data():
    """
    Performs the final data split (Train/Val/Test) and feature scaling.
    Saves the scaler and feature names as artifacts for the Deployment phase.
    """
    # 1. Load data
    df = pd.read_csv('data/processed/customer_features.csv')
    
    # 2. Separate features (X) and target (y)
    # Remove CustomerID and any non-feature columns
    y = df['Churn']
    X = df.drop(columns=['CustomerID', 'Churn'])
    
    # 3. Handle categorical variables
    # One-Hot Encoding for CustomerSegment
    X = pd.get_dummies(X, columns=['CustomerSegment'], prefix='Segment')
    
    # Drop Country if it exists (as per instructions)
    if 'Country' in X.columns:
        X = X.drop(columns=['Country'])
        
    # PreferredDay and PreferredHour stay as-is (Ordinal)
    
    # 4. Split data into train/validation/test (70:15:15)
    # First split: 70% train, 30% temp
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=y
    )
    
    # Second split: Split temp into 50/50 (results in 15% val, 15% test)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
    )
    
    # 5. Scale features (ONLY Numerical, NOT the one-hot dummies)
    # Identify boolean/dummy columns to exclude them from scaling
    cols_to_scale = [col for col in X_train.columns if not col.startswith('Segment_')]
    
    scaler = StandardScaler()
    # Change these lines:
    X_train.loc[:, cols_to_scale] = scaler.fit_transform(X_train[cols_to_scale])
    X_val.loc[:, cols_to_scale] = scaler.transform(X_val[cols_to_scale])
    X_test.loc[:, cols_to_scale] = scaler.transform(X_test[cols_to_scale])
# 6. Save prepared data and scaler
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    X_train.to_csv('data/processed/X_train.csv', index=False)
    X_val.to_csv('data/processed/X_val.csv', index=False)
    X_test.to_csv('data/processed/X_test.csv', index=False)
    y_train.to_csv('data/processed/y_train.csv', index=False)
    y_val.to_csv('data/processed/y_val.csv', index=False)
    y_test.to_csv('data/processed/y_test.csv', index=False)
    
    joblib.dump(scaler, 'models/scaler.pkl')
    
    with open('data/processed/feature_names.json', 'w') as f:
        json.dump(list(X_train.columns), f)

    # Data Preparation Summary
    print(f"""
Data Preparation Summary:
- Original features: {df.shape[1] - 2}
- Features after encoding: {X_train.shape[1]}
- Training samples: {len(X_train)}
- Validation samples: {len(X_val)}
- Test samples: {len(X_test)}
- Churn rate in train: {y_train.mean()*100:.2f}%
- Churn rate in test: {y_test.mean()*100:.2f}%
    """)

if __name__ == "__main__":
    prepare_data()