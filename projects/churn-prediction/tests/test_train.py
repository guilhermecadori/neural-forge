"""Tests for src/train.py — model building, training, evaluation, persistence."""

from __future__ import annotations

import json
import pickle
from pathlib import Path

import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier

from src.train import (
    build_model,
    evaluate,
    load_splits,
    run,
    save_metrics,
    save_model,
    train_model,
)


class TestLoadSplits:
    """Tests for load_splits."""

    def test_raises_when_train_missing(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError, match="Train data not found"):
            load_splits(tmp_path)

    def test_raises_when_test_missing(
        self, tmp_path: Path, clean_df: pd.DataFrame
    ) -> None:
        (tmp_path / "train.csv").write_text(clean_df.to_csv(index=False))
        with pytest.raises(FileNotFoundError, match="Test data not found"):
            load_splits(tmp_path)

    def test_loads_both(self, tmp_path: Path, clean_df: pd.DataFrame) -> None:
        (tmp_path / "train.csv").write_text(clean_df.to_csv(index=False))
        (tmp_path / "test.csv").write_text(clean_df.to_csv(index=False))
        train_df, test_df = load_splits(tmp_path)
        assert len(train_df) == len(clean_df)
        assert len(test_df) == len(clean_df)


class TestBuildModel:
    """Tests for build_model."""

    def test_returns_rf(self) -> None:
        model = build_model()
        assert isinstance(model, RandomForestClassifier)

    def test_respects_params(self) -> None:
        model = build_model(n_estimators=10, random_state=0)
        assert model.n_estimators == 10
        assert model.random_state == 0


class TestTrainModel:
    """Tests for train_model."""

    def test_fits_model(self, clean_df: pd.DataFrame) -> None:
        model = build_model(n_estimators=5)
        fitted = train_model(model, clean_df)
        assert hasattr(fitted, "classes_")  # fitted models have classes_

    def test_returns_same_model(self, clean_df: pd.DataFrame) -> None:
        model = build_model(n_estimators=5)
        fitted = train_model(model, clean_df)
        assert fitted is model


class TestEvaluate:
    """Tests for evaluate."""

    def test_returns_accuracy(self, clean_df: pd.DataFrame) -> None:
        model = build_model(n_estimators=5)
        train_model(model, clean_df)
        metrics = evaluate(model, clean_df)
        assert "accuracy" in metrics
        assert 0.0 <= metrics["accuracy"] <= 1.0


class TestSaveModel:
    """Tests for save_model."""

    def test_creates_pickle(self, tmp_path: Path) -> None:
        model = build_model()
        pkl_path = tmp_path / "models" / "model.pkl"
        save_model(model, pkl_path)
        assert pkl_path.exists()

    def test_pickle_roundtrip(self, tmp_path: Path) -> None:
        model = build_model(n_estimators=7)
        pkl_path = tmp_path / "model.pkl"
        save_model(model, pkl_path)
        with pkl_path.open("rb") as f:
            loaded = pickle.load(f)
        assert loaded.n_estimators == 7


class TestSaveMetrics:
    """Tests for save_metrics."""

    def test_creates_json(self, tmp_path: Path) -> None:
        path = tmp_path / "metrics.json"
        save_metrics({"accuracy": 0.95}, path)
        assert path.exists()

    def test_json_content(self, tmp_path: Path) -> None:
        path = tmp_path / "metrics.json"
        save_metrics({"accuracy": 0.95}, path)
        data = json.loads(path.read_text())
        assert data["accuracy"] == pytest.approx(0.95)


class TestRun:
    """Tests for the end-to-end run function."""

    def test_end_to_end(self, tmp_path: Path, clean_df: pd.DataFrame) -> None:
        processed = tmp_path / "processed"
        processed.mkdir()
        (processed / "train.csv").write_text(clean_df.to_csv(index=False))
        (processed / "test.csv").write_text(clean_df.to_csv(index=False))

        models_dir = tmp_path / "models"
        metrics_file = tmp_path / "metrics.json"

        metrics = run(
            processed_dir=processed,
            models_dir=models_dir,
            metrics_file=metrics_file,
        )

        assert "accuracy" in metrics
        assert (models_dir / "model.pkl").exists()
        assert metrics_file.exists()
