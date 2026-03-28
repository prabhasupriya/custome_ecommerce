import joblib
import pandas as pd
import numpy as np

def load_model():
    return joblib.load('models/best_model.pkl')

def load_scaler():
    return joblib.load('models/scaler.pkl')

def preprocess_input(data, scaler, feature_names):
    # Convert input to DataFrame
    df = pd.DataFrame(data)
    
    # Reorder columns to match training
    df = df[feature_names]
    
    # Scale only numeric columns
    numeric_cols = [c for c in feature_names if not c.startswith('Segment_')]
    df[numeric_cols] = scaler.transform(df[numeric_cols])
    return df

def predict(data):
    model = load_model()
    scaler = load_scaler()
    # Logic to handle JSON or CSV...
    # Return 0 or 1