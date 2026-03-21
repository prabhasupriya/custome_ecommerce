# Churn Definition Report

## Problem Statement
The objective is to identify customers who have stopped purchasing from the platform. Since this is non-contractual retail, we must define a "silence" threshold that signifies a customer has moved from active to churned.

## Approach: Observation Window Method

### Step 1: Define Time Windows
Based on the cleaned dataset (Dec 2009 - Dec 2010), we applied a 90-day split:
* **Total Data Period:** 2009-12-01 to 2010-12-09
* **Training Period (Feature Window):** 2009-12-01 to 2010-09-10
    * *Purpose:* All behavioral features (Recency, Frequency, Monetary) are calculated only from this data.
* **Observation Period (Target Window):** 2010-09-11 to 2010-12-09
    * *Purpose:* Used strictly to label customers as Churned or Active.

### Step 2: Churn Definition
* **CHURNED (Label 1):** A customer who made a purchase during the Training Period but made **ZERO** purchases in the subsequent 90-day Observation Period.
* **ACTIVE (Label 0):** A customer who made a purchase during the Training Period and **REMAINED ACTIVE** by making at least one purchase in the Observation Period.

### Step 3: Implementation Logic (Dynamic Approach)
We utilized a dynamic window to ensure the model remains valid even if new data is added:
```python
max_date = df['InvoiceDate'].max()
training_cutoff = max_date - pd.Timedelta(days=90)

# Features calculated from data < training_cutoff
# Labels (Churn) calculated based on existence in data >= training_cutoff