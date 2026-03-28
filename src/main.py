from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI(title="E-commerce Churn Prediction API")

# Load the Champion Model
MODEL_PATH = "models/xgboost.pkl"

if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"Model file not found at {MODEL_PATH}")

model = joblib.load(MODEL_PATH)

class CustomerData(BaseModel):
    Recency: float
    Frequency: float
    TotalSpent: float
    AvgOrderValue: float
    PurchaseVelocity: float
    # Add other key features used in your src/03 script here

@app.get("/")
def read_root():
    return {"message": "Churn Prediction API is running!"}

@app.post("/predict")
def predict_churn(data: CustomerData):
    try:
        # Convert input to DataFrame
        df = pd.DataFrame([data.dict()])
        
        # Get probability and prediction
        probability = model.predict_proba(df)[0][1]
        prediction = int(model.predict(df)[0])
        
        return {
            "churn_probability": round(float(probability), 4),
            "prediction": "Churn" if prediction == 1 else "Active"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))