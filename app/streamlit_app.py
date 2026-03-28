import streamlit as st
import pandas as pd
import joblib
import json
import numpy as np

# Load assets
@st.cache_resource
def load_assets():
    """Loads the trained model, scaler, and feature names for consistent preprocessing."""
    model = joblib.load('models/xgboost.pkl') 
    scaler = joblib.load('models/scaler.pkl')
    with open('data/processed/feature_names.json', 'r') as f:
        features = json.load(f)
    return model, scaler, features

model, scaler, model_features = load_assets()

st.title("📊 E-commerce Churn Predictor")

# --- BATCH PREDICTION ---
st.header("Batch Prediction (CSV)")
uploaded_file = st.file_uploader("Upload Customer CSV", type="csv")

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    
    # Preprocessing the uploaded file
    processed_data = data.copy()
    
    # 1. Handle One-Hot Encoding for Segment
    if 'CustomerSegment' in processed_data.columns:
        processed_data = pd.get_dummies(processed_data, columns=['CustomerSegment'], prefix='Segment')
    
    # 2. Ensure all training features exist (fill missing with 0)
    for col in model_features:
        if col not in processed_data.columns:
            processed_data[col] = 0
            
    # 3. Reorder and Scale
    processed_data = processed_data[model_features]
    cols_to_scale = [c for c in model_features if not c.startswith('Segment_')]
    processed_data[cols_to_scale] = scaler.transform(processed_data[cols_to_scale])
    
    # 4. Predict
    probs = model.predict_proba(processed_data)[:, 1]
    predictions = (probs > 0.5).astype(int)
    
    data['Churn_Probability'] = probs
    data['Churn_Prediction'] = ["Churn" if p == 1 else "Active" for p in predictions]
    
    st.write(data.head())
    
    # Download Button
    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Predictions", data=csv, file_name="batch_predictions.csv")