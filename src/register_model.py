import mlflow
from mlflow.tracking import MlflowClient

def register_best_model():
    client = MlflowClient()
    experiment = client.get_experiment_by_name("Titanic_Survival_Prediction")
    
    # Get all runs in the experiment
    runs = client.search_runs(experiment_ids=[experiment.experiment_id])
    
    # Sort runs by F1-score descending
    best_run = sorted(runs, key=lambda x: x.data.metrics.get("f1_score", 0), reverse=True)[0]
    
    run_id = best_run.info.run_id
    f1_score = best_run.data.metrics.get("f1_score")
    model_name = best_run.data.tags.get("mlflow.runName", "BestModel")
    
    print(f"Best run ID: {run_id} with F1-score: {f1_score:.4f} ({model_name})")
    
    # Register the model
    model_uri = f"runs:/{run_id}/model"
    registered_model_name = "TitanicBestModel"
    
    mv = mlflow.register_model(model_uri, registered_model_name)
    
    # Promote to Production
    client.transition_model_version_stage(
        name=registered_model_name,
        version=mv.version,
        stage="Production"
    )
    
    print(f"Model version {mv.version} promoted to Production.")

if __name__ == "__main__":
    register_best_model()
