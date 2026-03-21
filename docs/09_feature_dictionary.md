# Feature Dictionary

## Target Variable
| Feature | Type | Description | Example | Business Meaning |
| :--- | :--- | :--- | :--- | :--- |
| Churn | Binary | 1=Churned, 0=Active | 1 | Customer did not purchase during the 6-month observation window. |

---

## RFM Features
| Feature | Type | Description | Range | Business Meaning |
| :--- | :--- | :--- | :--- | : :--- |
| Recency | Integer | Days since last purchase from cutoff | 0-365 | Lower values indicate higher recent engagement. |
| Frequency | Integer | Count of unique Invoice numbers | 1-200+ | Higher values indicate repeat purchase behavior. |
| TotalSpent | Float | Sum of TotalPrice for all orders | 0-50k+ | Direct measure of monetary value to the business. |
| AvgOrderValue | Float | TotalSpent / Frequency | 5-500 | Indicates if the customer is a high-ticket or low-ticket buyer. |
| UniqueProducts | Integer | Count of unique StockCodes | 1-100 | Measure of product range exploration. |
| TotalItems | Integer | Sum of Quantity purchased | 1-10k+ | Physical volume of goods moved by the customer. |

---

## Behavioral & Product Features
| Feature | Type | Description | Range | Business Meaning |
| :--- | : :--- | :--- | :--- | :--- |
| AvgDaysBetween | Float | Mean of days between invoices | 0-100 | Predicts the expected date of the next purchase. |
| AvgBasketSize | Float | Mean items per invoice | 1-500 | Differentiates between bulk buyers and casual shoppers. |
| PreferredHour | Integer | Mode of purchase hour (24h) | 0-23 | Useful for timing marketing emails or push notifications. |
| DiversityScore | Float | Unique / Total products ratio | 0.0-1.0 | 1.0 means they never buy the same thing twice. |
| CountryDiv | Integer | Count of unique countries | 1-5 | Indicates if the customer is a multi-region entity. |

---

## Temporal Features
| Feature | Type | Description | Range | Business Meaning |
| :--- | :--- | :--- | :--- | :--- |
| LifetimeDays | Integer | Days between first and last order | 0-365 | Distinguishes "veteran" customers from new ones. |
| PurchaseVelocity | Float | Frequency / Lifetime | 0.0-1.0 | Speed of transaction accumulation over time. |
| Last30Days | Integer | Order count in last 30 days | 0-20 | Vital "momentum" indicator for churn prediction. |

---

## Feature Engineering Decisions

### Why these features?
The selection focuses on the **RFM model**, which is the industry standard for retail. We added **Behavioral features** (like `AvgDaysBetweenPurchases`) because churn is often preceded by a "slowdown" in purchase frequency. **Product features** (like `ProductDiversityScore`) help identify if a customer is loyal to a specific category or exploring the whole shop, which correlates with retention.

### Feature Interactions
* **Recency vs. Last30Days:** A high Recency (e.g., 200 days) will always result in 0 purchases in the Last 30 Days.
* **TotalSpent vs. AvgBasketSize:** High-value customers usually have either a high basket size or a high frequency; this interaction defines the "Customer Type" (Wholesale vs. Retail).

### Feature Importance Hypothesis
Based on business knowledge, we expect the following features to be the strongest predictors of churn:
1. **Recency:** (Strongest) If they haven't bought in months, they are likely already gone.
2. **Purchases_Last30Days:** A sudden drop to zero is a major red flag.
3. **Frequency:** Loyal customers (high frequency) are historically less likely to churn than one-time buyers.