import pandas as pd
import numpy as np
import json
import os
from datetime import datetime

import logging

# Configuration du logging pour Grafana (format JSON)
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        if hasattr(record, 'extra_data'):
            log_record.update(record.extra_data)
        return json.dumps(log_record)

logger = logging.getLogger("monitoring")
logger.setLevel(logging.INFO)
log_handler = logging.FileHandler("data/monitoring/monitoring_logs.json")
log_handler.setFormatter(JsonFormatter())
logger.addHandler(log_handler)

def calculate_and_save_stats(train_path, stats_path):
    """Calculates statistics from training data and saves them."""
    print(f"1. Calcul du dataset d'entraînement : {train_path}")
    df_train = pd.read_csv(train_path)
    
    # Matching user's requested structure: mean and std dictionaries
    # We filter for numerical columns to avoid errors with non-numeric data
    numerical_df = df_train.select_dtypes(include=[np.number])
    
    stats = {
        "mean": numerical_df.mean().to_dict(),
        "std": numerical_df.std().to_dict()
    }
    
    print(f"2. Sauvegarde des statistiques dans : {stats_path}")
    dir_name = os.path.dirname(stats_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=4)
    return stats

def monitor_production(prod_path, stats_path, history_dir):
    """Compares production data with reference stats and detects drift."""
    print(f"3. Comparaison avec les données de production : {prod_path}")
    if not os.path.exists(prod_path):
        print(f"Erreur : {prod_path} non trouvé.")
        return
    
    df_prod = pd.read_csv(prod_path)
    
    with open(stats_path, "r") as f:
        stats = json.load(f)
    
    print("4. Détection d'un éventuel data drift")
    drift_report = {
        "timestamp": datetime.now().isoformat(),
        "features": {}
    }
    drift_detected_global = False

    for col in df_prod.columns:
        # Only monitor columns present in our reference stats (numerical)
        if col in stats["mean"]:
            current_mean = df_prod[col].mean()
            ref_mean = stats["mean"][col]
            ref_std = stats["std"][col]
            
            diff = abs(current_mean - ref_mean)
            
            # Logic from snippet: diff > std
            if diff > ref_std:
                print(f"!! Data drift détecté sur la feature : {col}")
                logger.warning(f"Drift detected in {col}", extra={"extra_data": {"feature": col, "drift": True, "diff": diff, "threshold": ref_std}})
                status = "Drift Detected"
                drift_detected_global = True
            else:
                print(f"OK pour la feature : {col}")
                logger.info(f"Feature {col} is stable", extra={"extra_data": {"feature": col, "drift": False, "diff": diff, "threshold": ref_std}})
                status = "Stable"
            
            drift_report["features"][col] = {
                "status": status,
                "current_mean": current_mean,
                "ref_mean": ref_mean,
                "diff": diff,
                "threshold": ref_std
            }
    
    # Process à garantir: Garder un historique
    os.makedirs(history_dir, exist_ok=True)
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    history_file = os.path.join(history_dir, f"drift_report_{timestamp_str}.json")
    
    with open(history_file, "w") as f:
        json.dump(drift_report, f, indent=4)
    
    print(f"Historique sauvegardé dans : {history_file}")
    
    # Also update the latest report
    with open("data/monitoring/latest_report.json", "w") as f:
        json.dump(drift_report, f, indent=4)

if __name__ == "__main__":
    # Configuration based on user requirement to use data/train.csv and data/prod.csv
    # Note: Using project paths data/raw/train.csv and data/prod.csv
    TRAIN_CSV = "data/raw/train.csv"
    PROD_CSV = "data/prod.csv" 
    STATS_JSON = "train_stats.json"
    HISTORY_DIR = "data/monitoring/history"

    # Step 1 & 2
    calculate_and_save_stats(TRAIN_CSV, STATS_JSON)
    
    # Step 3 & 4
    monitor_production(PROD_CSV, STATS_JSON, HISTORY_DIR)
