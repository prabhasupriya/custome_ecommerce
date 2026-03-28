import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Churn Predictor", layout="wide")

st.title("🚀 E-commerce Customer Churn Dashboard")
st.markdown("Enter customer metrics below to predict the probability of churn.")

col1, col2 = st.columns(2)

with col1:
    recency = st.number_input("Recency (Days since last purchase)", min_value=0.0)
    frequency = st.number_input("Frequency (Total orders)", min_value=0.0)
    total_spent = st.number_input("Total Spent (£)", min_value=0.0)

with col2:
    avg_order = st.number_input("Avg Order Value", min_value=0.0)
    velocity = st.number_input("Purchase Velocity", min_value=0.0)

if st.button("Predict Churn Status"):
    # Connect to your API Layer
    data = {
        "Recency": recency, "Frequency": frequency, "TotalSpent": total_spent,
        "AvgOrderValue": avg_order, "PurchaseVelocity": velocity
    }
    
    try:
        response = requests.post("http://localhost:8000/predict", json=data)
        result = response.json()
        
        st.subheader(f"Prediction: {result['prediction']}")
        st.info(f"Churn Probability: {result['churn_probability'] * 100:.2f}%")
    except:
        st.error("Could not connect to API. Ensure FastAPI is running on port 8000.")