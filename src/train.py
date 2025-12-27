import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow
import mlflow.sklearn
import os

def train():
    df = pd.read_csv("data/processed/final_train.csv")
    X = df.drop(columns=['Survived'])
    y = df['Survived']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # MLflow tracking
    mlflow.set_experiment("Titanic_Survival_Prediction")
    
    models = [
        ("Logistic_Regression", LogisticRegression(max_iter=1000, random_state=42)),
        ("Random_Forest", RandomForestClassifier(n_estimators=100, min_samples_leaf=2, max_features='sqrt', random_state=42))
    ]
    
    for name, model in models:
        with mlflow.start_run(run_name=name):
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            # Metrics
            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred)
            rec = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            
            print(f"{name} - Acc: {acc:.4f}, Prec: {prec:.4f}, Rec: {rec:.4f}, F1: {f1:.4f}")
            
            # Log metrics
            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("precision", prec)
            mlflow.log_metric("recall", rec)
            mlflow.log_metric("f1_score", f1)
            
            # Log model
            mlflow.sklearn.log_model(model, "model")
            
            # Log params
            if name == "Random_Forest":
                mlflow.log_param("n_estimators", 100)
            elif name == "Logistic_Regression":
                mlflow.log_param("max_iter", 1000)

if __name__ == "__main__":
    train()
