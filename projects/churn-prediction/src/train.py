"""Train a RandomForest churn classifier and persist model + metrics."""

from __future__ import annotations

import json
import pickle
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

PROCESSED_DIR = Path("data/processed")
MODELS_DIR = Path("models")
METRICS_FILE = Path("metrics.json")
TARGET_COL = "Churn"
N_ESTIMATORS = 50
RANDOM_STATE = 42


def load_splits(
    processed_dir: Path = PROCESSED_DIR,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load train and test CSVs produced by prepare.py."""
    train_path = processed_dir / "train.csv"
    test_path = processed_dir / "test.csv"
    if not train_path.exists():
        raise FileNotFoundError(f"Train data not found: {train_path}.")
    if not test_path.exists():
        raise FileNotFoundError(f"Test data not found: {test_path}.")
    return pd.read_csv(train_path), pd.read_csv(test_path)


def build_model(
    n_estimators: int = N_ESTIMATORS,
    random_state: int = RANDOM_STATE,
) -> RandomForestClassifier:
    """Create an untrained RandomForestClassifier."""
    return RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)


def train_model(
    model: RandomForestClassifier,
    train_df: pd.DataFrame,
    target_col: str = TARGET_COL,
) -> RandomForestClassifier:
    """Fit the model on training data and return it."""
    x_train = train_df.drop(columns=[target_col])
    y_train = train_df[target_col]
    model.fit(x_train, y_train)
    return model


def evaluate(
    model: RandomForestClassifier,
    test_df: pd.DataFrame,
    target_col: str = TARGET_COL,
) -> dict[str, float]:
    """Compute accuracy on the test set."""
    x_test = test_df.drop(columns=[target_col])
    y_test = test_df[target_col]
    y_pred = model.predict(x_test)
    return {"accuracy": accuracy_score(y_test, y_pred)}


def save_model(model: RandomForestClassifier, path: Path) -> None:
    """Persist a trained model as pickle."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        pickle.dump(model, f)


def save_metrics(metrics: dict[str, float], path: Path = METRICS_FILE) -> None:
    """Write metrics dict to JSON."""
    with path.open("w") as f:
        json.dump(metrics, f, indent=2)


def run(
    processed_dir: Path = PROCESSED_DIR,
    models_dir: Path = MODELS_DIR,
    metrics_file: Path = METRICS_FILE,
) -> dict[str, float]:
    """End-to-end training pipeline."""
    train_df, test_df = load_splits(processed_dir)
    model = build_model()
    model = train_model(model, train_df)
    save_model(model, models_dir / "model.pkl")
    metrics = evaluate(model, test_df)
    save_metrics(metrics, metrics_file)
    return metrics


if __name__ == "__main__":
    run()
