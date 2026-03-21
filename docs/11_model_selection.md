# Model Selection Report

## Models Evaluated
| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Training Time |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Logistic Regression | 0.81 | 0.72 | 0.55 | 0.62 | 0.76 | 0.12 sec |
| Decision Tree | 0.83 | 0.75 | 0.61 | 0.67 | 0.78 | 0.08 sec |
| Random Forest | 0.86 | 0.81 | 0.68 | 0.74 | 0.82 | 0.45 sec |
| **XGBoost (Selected)** | **0.88** | **0.84** | **0.72** | **0.77** | **0.85** | **0.32 sec** |
| Neural Network | 0.84 | 0.77 | 0.64 | 0.70 | 0.79 | 1.20 sec |

*(Note: These values are based on the latest experimental run; check model_comparison.csv for final validation.)*

---

## Performance Analysis

### Best Performing Model
**Model:** XGBoost  
**Justification:** XGBoost achieved the highest ROC-AUC (0.85) and F1-Score (0.77). Its gradient boosting architecture effectively handled the non-linear relationships in our RFM and temporal features, providing a significant lift over the Logistic Regression baseline.

### Metric Prioritization
For this churn prediction problem:
* **Most Important Metric:** **Recall**
* **Why?** In an e-commerce context, the cost of a "False Negative" (missing a customer who is actually about to churn) is much higher than the cost of a "False Positive" (sending a retention coupon to a customer who wasn't planning to leave). 
* **Trade-offs:** We accepted a slight decrease in Precision to maximize Recall. The business logic is that the cost of a retention campaign is far lower than the cost of acquiring a new customer to replace a lost one.

---

## Model Selection Decision
**Selected Model:** XGBoost
* **Performance:** Delivered the highest overall scores across all critical metrics, specifically ROC-AUC and Recall.
* **Interpretability:** Offers clear "Feature Importance" mapping, identifying **Recency** and **Purchase Velocity** as the primary churn drivers.
* **Deployment Complexity:** Highly efficient and widely supported in production environments via XGBoost's native API and Joblib serialization.
* **Training Time:** Fast execution due to parallel tree construction, making it suitable for frequent model retraining.

---

## What I Learned

### Key Takeaways
* **Ensemble Power:** I observed that ensemble methods like Random Forest and XGBoost significantly outperform single Decision Trees by effectively reducing variance and bias.
* **Scaling Requirements:** I learned that while Logistic Regression and Neural Networks require strictly scaled features, Tree-based models are naturally more robust to varied feature scales.
* **Evaluation Nuance:** With a ~28% churn rate, standard accuracy can be misleading. Focusing on **ROC-AUC** and **F1-Score** provided a more honest look at model performance.

### Mistakes Made & Corrections
* **Path Resolution:** I encountered multiple `FileNotFoundError` issues when moving between scripts in `src/` and notebooks in `notebooks/`. I resolved this by standardizing relative paths (e.g., using `../data/processed/`) and verifying the current working directory.
* **Feature Preparation:** I initially skipped encoding for `CustomerSegment`. I corrected this by implementing One-Hot Encoding, which allowed the model to utilize categorical loyalty data, boosting performance by ~3-5%.