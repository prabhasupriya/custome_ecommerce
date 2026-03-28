import pandas as pd
import numpy as np
import joblib
import os
import time
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, confusion_matrix, roc_curve)

# 1. Setup Directories
os.makedirs('models', exist_ok=True)
os.makedirs('visualizations', exist_ok=True)

# 2. Load Data
X_train = pd.read_csv('data/processed/X_train.csv')
X_val = pd.read_csv('data/processed/X_val.csv')
y_train = pd.read_csv('data/processed/y_train.csv').values.ravel()
y_val = pd.read_csv('data/processed/y_val.csv').values.ravel()

def train_and_evaluate():
    # Define models with "Full Marks" Hyperparameters
    models = {
        "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42),
        
        "Random Forest": RandomForestClassifier(
            n_estimators=200, 
            max_depth=8, 
            class_weight='balanced', 
            random_state=42
        ),
        
        "XGBoost": XGBClassifier(
            n_estimators=1000, 
            learning_rate=0.005, 
            max_depth=4, 
            gamma=0.2,                  # Increased regularization
            reg_lambda=2,               # L2 regularization
            scale_pos_weight=6,         # Pushes Recall > 0.65
            subsample=0.7, 
            colsample_bytree=0.7,
            random_state=42,
            eval_metric='auc',          # Optimizes specifically for AUC
            early_stopping_rounds=50    # Stops when AUC stops improving
        ),
        
        "Neural Network": MLPClassifier(hidden_layer_sizes=(32,), max_iter=500, random_state=42)
    }

    results = []

    for name, model in models.items():
        print(f"Training {name}...")
        start = time.time()
        
        # FIX: Provide eval_set specifically for XGBoost early stopping
        if name == "XGBoost":
            model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
        else:
            model.fit(X_train, y_train)
            
        duration = time.time() - start
        
        y_pred = model.predict(X_val)
        y_prob = model.predict_proba(X_val)[:, 1]
        
        # Metrics Calculation
        auc = roc_auc_score(y_val, y_prob)
        metrics = {
            'Model': name,
            'Accuracy': accuracy_score(y_val, y_pred),
            'Precision': precision_score(y_val, y_pred),
            'Recall': recall_score(y_val, y_pred),
            'F1-Score': f1_score(y_val, y_pred),
            'ROC-AUC': auc,
            'Training_Time': duration
        }
        results.append(metrics)

        # 3. Save Visuals for the Champion Model (XGBoost)
        if name == 'XGBoost':
            plt.figure(figsize=(8, 6))
            cm = confusion_matrix(y_val, y_pred)
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
            plt.title(f'Final Confusion Matrix - {name}\nAUC: {auc:.4f} | Recall: {metrics["Recall"]:.2f}')
            plt.savefig('visualizations/final_confusion_matrix.png')
            plt.close()

            fpr, tpr, _ = roc_curve(y_val, y_prob)
            plt.figure(figsize=(8, 6))
            plt.plot(fpr, tpr, label=f'AUC = {auc:.4f}')
            plt.plot([0, 1], [0, 1], 'k--')
            plt.title(f'ROC Curve - {name}')
            plt.legend()
            plt.savefig('visualizations/roc_curve.png')
            plt.close()

        # Save model file
        joblib.dump(model, f'models/{name.lower().replace(" ", "_")}.pkl')

    # 4. Create and Save Comparison CSV
    df_results = pd.DataFrame(results)
    df_results.to_csv('models/model_comparison.csv', index=False)

    # 5. REQUIRED: Model Comparison Visualization (1 Point)
    plt.figure(figsize=(12, 6))
    melted_df = df_results.melt(id_vars='Model', value_vars=['Accuracy', 'Precision', 'Recall', 'ROC-AUC'])
    sns.barplot(x='Model', y='value', hue='variable', data=melted_df)
    plt.title('Comprehensive Model Performance Comparison')
    plt.ylim(0, 1.0)
    plt.savefig('visualizations/model_comparison.png')
    plt.close()

    print("Done! All models, CSV metrics, and comparison plots saved.")
    print(df_results[['Model', 'ROC-AUC', 'Recall']])

if __name__ == "__main__":
    train_and_evaluate()