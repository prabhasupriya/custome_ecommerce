# Business Problem Statement: RetailCo Analytics

## 1. Business Context
In the highly competitive e-commerce industry, customer loyalty is volatile. Data shows that acquiring a new customer costs 5x to 25x more than retaining an existing one. For "RetailCo," losing a high-value customer directly impacts the bottom line and reduces the return on marketing spend.

## 2. Problem Definition
The primary goal is to address **Customer Churn**. 
**Churn Definition:** A customer is considered "churned" if they have not made a single transaction in the 90 days following their last purchase.

## 3. Stakeholders
* **Marketing Team:** Requires customer segments to design targeted re-engagement campaigns.
* **Sales Team:** Needs a list of "at-risk" customers to offer personalized discounts.
* **Executive Team:** Needs to see the projected ROI and a reduction in the churn rate.

## 4. Business Impact
* **Churn Reduction:** Target a 15-20% decrease in the current churn rate.
* **Revenue Growth:** By retaining top-tier customers identified through RFM analysis, we project a 10% increase in quarterly revenue.
* **Cost Efficiency:** Reducing "spray and pray" marketing by focusing budgets on customers with high predicted churn probability.

## 5. Success Metrics
* **Primary Metric:** ROC-AUC Score > 0.78
* **Secondary Metrics:** * Precision > 0.75 (To ensure we don't give discounts to customers who weren't going to leave).
    * Recall > 0.70 (To ensure we catch the majority of actual churners).
    * F1-Score > 0.72.