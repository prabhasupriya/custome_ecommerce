# E-commerce Customer Churn Prediction System

## 📌 Project Overview
This project implements an end-to-end Machine Learning pipeline to predict customer churn for an e-commerce platform. By analyzing transaction history and behavioral patterns, the system identifies customers likely to stop shopping, allowing for proactive retention strategies.

## 📊 Key Insights
* **Baseline Churn Rate:** 28.09%
* **Champion Model:** XGBoost (Selected for high Recall and ROC-AUC)
* **Core Features:** RFM Metrics (Recency, Frequency, Monetary), Purchase Velocity, and Weekend Purchase Ratios.

## 🛠️ Tech Stack
* **Language:** Python 3.12
* **ML Libraries:** Scikit-learn, XGBoost, Pandas, Joblib
* **API Framework:** FastAPI with Uvicorn
* **Containerization:** Docker & Docker Compose

## 🚀 How to Run the Project

### 1. Build and Start the Environment
Ensure Docker is running, then execute:
```bash
docker-compose up -d --build

## 2. Train the Models
Run the training script inside the container to generate the .pkl files:

```Bash
docker-compose exec data-science-app python src/06_train_final_models.py
```
## 3. Launch the API
Start the FastAPI server:

```Bash
docker-compose exec data-science-app python src/05_app.py
```
## 4. Access the API
Open your browser and navigate to:
http://localhost:8000/docs

## Project Structure
**data/:** Contains raw and processed CSV files.

**models/:** Saved model binaries (.pkl) and performance comparisons.

**notebooks/:** Exploratory Data Analysis and model prototyping.

**src/:** Production-ready Python scripts and API logic.

**docs/:** Technical reports and feature dictionaries.