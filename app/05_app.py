from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os
import json

app = FastAPI(title="E-commerce Churn Prediction API")

# 1. Load the best model and the scaler
# Change these lines to match your actual files in the models folder
MODEL_PATH = '/app/models/xgboost.pkl'  # Not xgboost.pkl
SCALER_PATH = '/app/models/scaler.pkl'
FEATURES_PATH = '/app/data/processed/feature_names.json'
if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
    raise RuntimeError("Model or Scaler not found. Run training/prep scripts first!")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# Load the exact feature order used during training
with open(FEATURES_PATH, 'r') as f:
    model_features = json.load(f)

# 2. Define Input Schema (Standard RFM + Behavioral)
class CustomerData(BaseModel):
    Recency: float
    Frequency: float
    TotalSpent: float
    AvgOrderValue: float
    UniqueProducts: int
    TotalItems: int
    AvgDaysBetween: float
    AvgBasketSize: float
    PreferredHour: int
    DiversityScore: float
    CountryDiv: int
    LifetimeDays: int
    PurchaseVelocity: float
    Last30Days: int
    CustomerSegment: str  # We will encode this inside the function

@app.get("/")
def home():
    return {"status": "Online", "model": "XGBoost", "version": "1.0"}

@app.post("/predict")
def predict_churn(data: CustomerData):
    try:
        # Convert input to dictionary
        input_dict = data.dict()
        segment_val = input_dict.pop('CustomerSegment')
        
        # Create DataFrame
        df = pd.DataFrame([input_dict])
        
        # 3. Manual One-Hot Encoding for Segments
        # Must match the 'Segment_Name' columns created in src/04_model_preparation.py
        all_segments = ['Segment_At Risk', 'Segment_Champions', 'Segment_Loyal', 
                        'Segment_Lost', 'Segment_Potential']
        
        for seg in all_segments:
            df[seg] = 1 if seg == f"Segment_{segment_val}" else 0
            
        # 4. Ensure column order matches training exactly
        # If any features are missing from the request, fill with 0
        for col in model_features:
            if col not in df.columns:
                df[col] = 0
        
        df = df[model_features] # Reorder columns
        
        # 5. Scale the numerical columns (Everything except the Segment dummies)
        cols_to_scale = [c for c in df.columns if not c.startswith('Segment_')]
        df[cols_to_scale] = scaler.transform(df[cols_to_scale])
        
        # 6. Final Prediction
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0][1]
        
        return {
            "prediction": "Churn" if prediction == 1 else "Active",
            "probability": round(float(probability), 4),
            "risk_level": "High" if probability > 0.5 else "Low"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)