# Titanic MLOps Pipeline: Implementation Guide

This guide details the step-by-step construction of a production-grade MLOps pipeline using the Titanic dataset.

## Table of Contents

1. [Environment & Git Setup](#1-environment--git-setup)
2. [Data Versioning with DVC](#2-data-versioning-with-dvc)
3. [Experiment Tracking with MLflow](#3-experiment-tracking-with-mlflow)
4. [Pipeline Automation (DVC)](#4-pipeline-automation-dvc)
5. [Advanced Feature: Model Selection](#5-advanced-feature-model-selection)
6. [CI/CD with GitHub Actions](#6-cicd-with-github-actions)

---

## 1. Environment & Git Setup

First, initialize the repository and install dependencies.

```bash
# Initialize Git
git init

# Create requirements.txt
# Include: pandas, dvc, mlflow, scikit-learn, fpdf, boto3
pip install -r requirements.txt
```

## 2. Data Versioning with DVC

DVC is used to track three versions of the dataset.

- **V1 (Raw)**: `data/raw/train.csv` (Original dataset).
- **V2 (Cleaned)**: Handled missing values and encoding.
- **V3 (Enhanced)**: Feature engineering + Class balancing.

```bash
# Initialize DVC
dvc init

# Track V1
dvc add data/raw/train.csv
git add data/raw/train.csv.dvc
```

## 3. Experiment Tracking with MLflow

The `src/train.py` script logs metrics (F1, Accuracy) and models to MLflow.

```python
# snippet from src/train.py
with mlflow.start_run(run_name="Random_Forest"):
    model.fit(X_train, y_train)
    mlflow.log_metric("f1_score", f1)
    mlflow.sklearn.log_model(model, "model")
```

## 4. Pipeline Automation (DVC)

The `dvc.yaml` file orchestrates the workflow.

```yaml
stages:
  clean_data:
    cmd: python src/clean_data.py
    deps: [data/raw/train.csv, src/clean_data.py]
    outs: [data/interim/cleaned_train.csv]
  feature_engineering:
    cmd: python src/feature_engineering.py
    deps: [data/interim/cleaned_train.csv]
    outs: [data/processed/final_train.csv]
  training:
    cmd: python src/train.py
    deps: [data/processed/final_train.csv, src/train.py]
  registration:
    cmd: python src/register_model.py
    deps: [src/register_model.py]
```

## 5. Advanced Feature: Model Selection

Implemented `src/register_model.py` to automatically register the best model.

1.  Query MLflow for all runs in the experiment.
2.  Rank by `f1_score`.
3.  Register the winner and promote to **Production** stage in MLflow Model Registry.

## 6. CI/CD with GitHub Actions

The `.github/workflows/mlops.yml` triggers on every push to validate the pipeline.

```yaml
on: [push, pull_request]
jobs:
  run-pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pip install -r requirements.txt
      - run: dvc init --no-scm
      - run: dvc repro
```

---

## Summary of Results

- **Dataset Versions**: 3 (Raw, Cleaned, Enhanced).
- **Models**: Logistic Regression, Random Forest (Winner: RF, F1 ~0.80).
- **Automation**: One command `dvc repro` executes everything.
