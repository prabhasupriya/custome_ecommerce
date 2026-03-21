import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import joblib
import os

def train_models():
    print("🤖 Starting Model Training Phase...")
    
    # 1. Load the features
    if not os.path.exists('data/processed/customer_features.csv'):
        print("❌ Error: customer_features.csv not found. Run Phase 4 first!")
        return

    # Using index_col=0 to avoid the naming error
    df = pd.read_csv('data/processed/customer_features.csv', index_col=0)
    
    # 2. CRITICAL FIX: Drop any rows with NaN values
    initial_count = len(df)
    df = df.dropna()
    if len(df) < initial_count:
        print(f"⚠️ Dropped {initial_count - len(df)} rows containing NaN values.")

    # 3. Prepare X (Features) and y (Target)
    X = df.drop(['Churn'], axis=1)
    y = df['Churn']
    
    # 4. Split data (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 5. Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 6. Define Models
    models = {
        "Logistic Regression": LogisticRegression(),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42)
    }
    
    results = {}
    os.makedirs('models', exist_ok=True)

    # 7. Train and Evaluate
    for name, model in models.items():
        # Use scaled data for Logistic Regression, raw data for Trees
        X_tr = X_train_scaled if name == "Logistic Regression" else X_train
        X_ts = X_test_scaled if name == "Logistic Regression" else X_test
        
        model.fit(X_tr, y_train)
        probs = model.predict_proba(X_ts)[:, 1]
        auc = roc_auc_score(y_test, probs)
        results[name] = auc
        print(f"✅ {name} ROC-AUC: {auc:.4f}")

    # 8. Save the best model
    best_model_name = max(results, key=results.get)
    best_model = models[best_model_name]
    
    joblib.dump(best_model, 'models/churn_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    
    print(f"\n🏆 Best Model: {best_model_name}")
    
    # 9. Final Evaluation Report
    final_X_test = X_test if best_model_name != "Logistic Regression" else X_test_scaled
    y_pred = best_model.predict(final_X_test)
    
    print("\n" + "="*30)
    print("FINAL CLASSIFICATION REPORT")
    print("="*30)
    print(classification_report(y_test, y_pred))
    
    # 10. Save Metrics for submission.json
    report = classification_report(y_test, y_pred, output_dict=True)
    metrics = {
        "best_model": best_model_name,
        "precision": round(report['weighted avg']['precision'], 2),
        "recall": round(report['weighted avg']['recall'], 2),
        "f1_score": round(report['weighted avg']['f1-score'], 2),
        "roc_auc": round(results[best_model_name], 2)
    }
    
    with open('data/processed/model_metrics.json', 'w') as f:
        import json
        json.dump(metrics, f, indent=4)
    print("\n✅ Metrics saved to data/processed/model_metrics.json")

if __name__ == "__main__":
    train_models()