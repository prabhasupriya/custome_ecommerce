import pandas as pd
import time
import joblib
import json
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

# Ensure directories exist
os.makedirs('../models', exist_ok=True)
os.makedirs('../visualizations', exist_ok=True)

# Load data
X_train = pd.read_csv('data/processed/X_train.csv')
X_val = pd.read_csv('data/processed/X_val.csv')
y_train = pd.read_csv('data/processed/y_train.csv').values.ravel()
y_val = pd.read_csv('data/processed/y_val.csv').values.ravel()

results = []

def train_and_save(name, model):
    print(f"Training {name}...")
    start = time.time()
    model.fit(X_train, y_train)
    end = time.time()
    
    y_pred = model.predict(X_val)
    y_prob = model.predict_proba(X_val)[:, 1]
    
    metrics = {
        'Model': name,
        'Accuracy': accuracy_score(y_val, y_pred),
        'Precision': precision_score(y_val, y_pred),
        'Recall': recall_score(y_val, y_pred),
        'F1-Score': f1_score(y_val, y_pred),
        'ROC-AUC': roc_auc_score(y_val, y_prob),
        'Training_Time': end - start
    }
    joblib.dump(model, f'../models/{name.lower().replace(" ", "_")}.pkl')
    return metrics

# Run all 4 models
results.append(train_and_save('Decision Tree', DecisionTreeClassifier(max_depth=5, random_state=42)))
results.append(train_and_save('Random Forest', RandomForestClassifier(n_estimators=100, random_state=42)))
results.append(train_and_save('XGBoost', XGBClassifier(n_estimators=100, learning_rate=0.1, random_state=42)))
results.append(train_and_save('Neural Network', MLPClassifier(hidden_layer_sizes=(64,32), max_iter=500, random_state=42)))

# Save Comparison
df_results = pd.DataFrame(results)
df_results.to_csv('models/model_comparison.csv', index=False)
print("Done! All models saved in /models folder.")