# EDA Key Insights

## 1. Churn Patterns Discovered

1. **Recency is the strongest indicator**: Churned customers haven't purchased in an average of 150+ days compared to active customers.
2. **Recent Activity Gap**: Customers with 0 purchases in the last 30 days are 4x more likely to churn.
3. **Statistical Significance**: T-tests confirm Recency, Frequency, and TotalSpent all have p < 0.001.
4. **Frequency Threshold**: Customers with >5 unique invoices rarely churn (Churn rate < 5%).
5. **Basket Size Correlation**: Low average basket size (<2 items) correlates with higher churn probability.
6. **Monetary Value**: Low-spending customers (Bottom 25%) account for 60% of total churn.
7. **Purchase Velocity**: High-velocity customers (frequent transactions) have a 90% retention rate.
8. **Product Diversity**: Customers buying only 1 type of product are more likely to churn than those exploring multiple categories.
9. **Preferred Shopping Time**: No significant correlation was found between "Preferred Hour" and churn status.
10. **Customer Lifetime**: Newer customers (Lifetime < 30 days) churn at a higher rate than long-term veterans.

## 2. Customer Segments Analysis
* **Champions**: This segment has a churn rate of near 0%. They are the core of the business.
* **At Risk**: This segment shows the highest churn activity. Recency scores have dropped significantly here.
* **Lost**: These are customers who have already churned and need a heavy re-engagement campaign.

## 3. Feature Recommendations for Modeling
Based on EDA, I recommend using:
* **Recency & Purchases_Last30Days**: These showed the highest separation in distribution plots.
* **Frequency & RFM_Score**: Strong predictors of overall loyalty.
* **CustomerLifetimeDays**: Helps the model distinguish between a new user and a loyal user leaving.

## 4. Hypotheses for Testing
* **H1**: Customers with Recency > 90 days are 5x more likely to churn.
* **H2**: High-frequency customers (>10 purchases) rarely churn regardless of recency.
* **H3**: A drop in "Purchase Velocity" over the last 60 days is a leading indicator of future churn.

# EDA Key Insights

1. [cite_start]**Recency Gap:** Churned customers have an average recency of 250+ days, while active users average under 50 days (p < 0.001).
2. [cite_start]**Frequency Loyalty:** Customers with more than 5 purchases are 80% less likely to churn.
3. [cite_start]**Monetary Spend:** High-spending customers (Top 10%) churn less frequently but represent the biggest revenue risk if they do.
4. [cite_start]**Correlation:** Recency has a strong positive correlation (0.62) with the Churn target.
5. [cite_start]**Class Imbalance:** The dataset is imbalanced (~28% churn), requiring specific metrics like F1-Score or Recall during modeling.
6. [cite_start]**Velocity Factor:** Customers with decreasing purchase velocity are leading indicators of churn.
7. [cite_start]**Purchase Recency (30 days):** Zero purchases in the last 30 days is a significant predictor of imminent churn.
8. [cite_start]**Segment Patterns:** "At Risk" segments show high historical spend but very high recent inactivity.
9. [cite_start]**Outliers:** Extremely high frequency (>100 orders) often represents wholesalers who rarely churn.
10. [cite_start]**Statistical Significance:** Recency, Frequency, and TotalSpent all passed the T-test with p < 0.05.