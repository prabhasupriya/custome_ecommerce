# E-commerce Customer Churn Prediction System

##  Project Overview
This project implements an end-to-end Machine Learning pipeline to predict customer churn for an e-commerce platform. By analyzing transaction history and behavioral patterns, the system identifies customers likely to stop shopping, allowing for proactive retention strategies.

## Project Structure

The repository is organized into a modular structure to separate data science research from production-grade code:

```text
├── data/           # Contains raw, cleaned, and processed CSV files
├── models/         # Saved model binaries (.pkl) and model_comparison.csv
├── visualizations/ # Exported plots (Confusion Matrix, ROC Curve, etc.)
├── notebooks/      # Jupyter notebooks for EDA and initial prototyping
├── src/            # Production-ready Python scripts:
│   ├── 01_data_acquisition.py
│   ├── 02_data_cleaning.py
│   ├── 03_feature_engineering.py
│   ├── 04_model_preparation.py
│   ├── 06_train_Final_models.py
│   └── main.py     # FastAPI application logic
├── docs/           # Technical reports and feature dictionaries
├── requirements.txt# Project dependencies
└── Dockerfile      # Containerization configuration

```
##   Key Insights
* **Baseline Churn Rate:** 28.09%
* **Champion Model:** XGBoost (Selected for high Recall and ROC-AUC)
* **Core Features:** RFM Metrics (Recency, Frequency, Monetary), Purchase Velocity, and Weekend Purchase Ratios.

##  Tech Stack
* **Language:** Python 3.12
* **ML Libraries:** Scikit-learn, XGBoost, Pandas, Joblib
* **API Framework:** FastAPI with Uvicorn
* **Containerization:** Docker & Docker Compose

##  How to Run the Project

### 1. Build and Start the Environment
Ensure Docker is running, then execute:
```bash
docker-compose up -d --build
```
##  Model Training & Results

To ensure reproducibility and environment consistency, the full pipeline was executed within a containerized environment using the following command sequence:

```bash
# Execute the full data and modeling pipeline
docker exec ecommerce-churn-prediction python src/01_data_acquisition.py
docker exec ecommerce-churn-prediction python src/02_data_cleaning.py
docker exec ecommerce-churn-prediction python src/03_feature_engineering.py
docker exec ecommerce-churn-prediction python src/04_model_preparation.py
docker exec ecommerce-churn-prediction python src/06_train_Final_models.py
```
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
### Final Model Comparison

After training on the processed RFM (Recency, Frequency, Monetary) and behavioral features, the following performance metrics were achieved on the validation set:
```bash
| Model | ROC-AUC | Recall |
| :--- | :---: | :---: |
| Decision Tree | 0.7100 | 0.2685 |
| Random Forest | 0.7374 | 0.6204 |
| **XGBoost (Champion)** | **0.7654** | **1.0000** |
| Neural Network | 0.7206 | 0.1852 |
```
## 4. Access the API
Once the Docker containers are running, you can access the interactive API documentation (Swagger UI) to test predictions:

1. Open your web browser.
2. Navigate to: [http://localhost:8000/docs](http://localhost:8000/docs)
3. Here you can test the `/predict` and `/predict_batch` endpoints directly.
## Project Structure
**data/:** Contains raw and processed CSV files.

**models/:** Saved model binaries (.pkl) and performance comparisons.

**notebooks/:** Exploratory Data Analysis and model prototyping.

**src/:** Production-ready Python scripts and API logic.

**docs/:** Technical reports and feature dictionaries.
