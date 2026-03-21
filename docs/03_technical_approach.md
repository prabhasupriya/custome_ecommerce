# Technical Approach

## 1. Why Classification?
We are predicting a discrete outcome: **Will the customer return or not?** (1 or 0). Since the target is categorical, classification is the appropriate supervised learning approach rather than regression.

## 2. Feature Engineering Strategy
We will transform raw transaction data into a **Customer-Centric Dataset**. Key features include:
* **RFM Metrics:** The strongest predictors of retail behavior.
* **Temporal Features:** Hour of day and Day of week to find "habitual" shoppers.
* **Monetary Aggregates:** Average order value and total spend to identify high-value targets.

## 3. Multi-Model Strategy
No single algorithm fits all data. We will compare:
1.  **Logistic Regression** (Baseline).
2.  **Random Forest** (To handle non-linear relationships).
3.  **XGBoost/Gradient Boosting** (To optimize for the ROC-AUC target).
4.  **Neural Networks (MLP)** (To capture complex patterns).

## 4. Deployment
The final model will be containerized using **Docker** to ensure the environment remains consistent from the developer's laptop to the evaluation server.