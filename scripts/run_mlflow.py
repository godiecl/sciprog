import logging
from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

from benchmarking import benchmark
from logger import configure_logging

# Logger instance named after this module
log = logging.getLogger(__name__)


# Entry point — receives directory for MLflow artifacts
def main():
    # Bunch object with .data (features), .target (labels), .feature_names
    wine = load_wine()
    # 178×13 DataFrame (alcohol, malic_acid, ...)
    # pyrefly: ignore [missing-attribute]
    X = pd.DataFrame(wine.data, columns=wine.feature_names)
    # 178 class labels (0, 1, 2)
    # pyrefly: ignore [missing-attribute]
    y = wine.target

    # 80/20 stratified split (random_state fixes seed)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Begin a tracked run — logs params, metrics, and model under this run
    with mlflow.start_run():
        # Hyperparameters to track
        params = {"n_estimators": 100, "max_depth": 5}
        # Record hyperparams so they appear in the MLflow UI
        mlflow.log_params(params)

        # 100 trees, max depth 5, fixed seed
        model = RandomForestClassifier(**params, random_state=42)
        # Train the classifier on 142 training samples
        model.fit(X_train, y_train)

        # Predict labels for the 36 held-out test samples
        y_pred = model.predict(X_test)
        # Fraction of correct predictions
        mlflow.log_metric("accuracy", accuracy_score(y_test, y_pred))
        # Weighted F1 across 3 classes
        mlflow.log_metric("f1", f1_score(y_test, y_pred, average="weighted"))

        # Serialise the trained pipeline to output/mlruns/
        mlflow.sklearn.log_model(model, name="model")


# Guard: only execute when run as a script, not when imported
if __name__ == "__main__":
    # Show DEBUG-level messages (timestamps, module, level, message)
    configure_logging(logging.DEBUG)

    # Project root (one level above scripts/)
    root_dir = Path(__file__).resolve().parent.parent
    # Log the resolved project root for debugging
    log.debug("root_dir: %s", root_dir)

    # All generated artifacts go here
    output_dir = root_dir / "output"
    # Create output/ if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    # Confirm the output directory path
    log.debug("output_dir: %s", output_dir)

    # Store runs and metadata in a SQLite database under output/
    mlflow.set_tracking_uri(f"sqlite:///{(output_dir / 'mlflow.db').as_posix()}")

    # Group runs under this experiment name
    mlflow.set_experiment("wine-classification")

    # log!
    # mlflow.sklearn.autolog()

    # Measure and log total wall-clock time of the block
    with benchmark("main", log):
        # Human-readable progress marker
        log.info("MLflow, starting ..")
        # Run the experiment — trains model, logs to MLflow
        main()
        # Signal completion
        log.info(" done.")
