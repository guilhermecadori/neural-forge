"""Tests for src/prepare.py — data loading, imputation, splitting, saving."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from src.prepare import impute_median, load_raw, run, save_splits, split


class TestLoadRaw:
    """Tests for load_raw."""

    def test_raises_when_file_missing(self, tmp_path: Path) -> None:
        missing = tmp_path / "does_not_exist.csv"
        with pytest.raises(FileNotFoundError, match="Raw data not found"):
            load_raw(missing)

    def test_loads_csv(self, tmp_path: Path, raw_df: pd.DataFrame) -> None:
        csv_path = tmp_path / "churn.csv"
        raw_df.to_csv(csv_path, index=False)
        loaded = load_raw(csv_path)
        assert list(loaded.columns) == list(raw_df.columns)
        assert len(loaded) == len(raw_df)


class TestImputeMedian:
    """Tests for impute_median."""

    def test_fills_missing_values(self, raw_df: pd.DataFrame) -> None:
        result = impute_median(raw_df)
        assert result.isna().sum().sum() == 0

    def test_preserves_complete_values(self, raw_df: pd.DataFrame) -> None:
        result = impute_median(raw_df)
        # Tenure had no NaNs — should be unchanged
        pd.testing.assert_series_equal(result["Tenure"], raw_df["Tenure"])

    def test_does_not_modify_original(self, raw_df: pd.DataFrame) -> None:
        original_nulls = raw_df.isna().sum().sum()
        impute_median(raw_df)
        assert raw_df.isna().sum().sum() == original_nulls


class TestSplit:
    """Tests for split."""

    def test_split_sizes(self, clean_df: pd.DataFrame) -> None:
        train_df, test_df = split(clean_df, test_size=0.2, random_state=42)
        assert len(train_df) + len(test_df) == len(clean_df)
        assert len(test_df) == pytest.approx(len(clean_df) * 0.2, abs=1)

    def test_deterministic(self, clean_df: pd.DataFrame) -> None:
        t1, _ = split(clean_df, test_size=0.2, random_state=42)
        t2, _ = split(clean_df, test_size=0.2, random_state=42)
        pd.testing.assert_frame_equal(
            t1.reset_index(drop=True), t2.reset_index(drop=True)
        )


class TestSaveSplits:
    """Tests for save_splits."""

    def test_creates_files(self, tmp_path: Path, clean_df: pd.DataFrame) -> None:
        train_df, test_df = split(clean_df)
        train_path, test_path = save_splits(train_df, test_df, tmp_path)
        assert train_path.exists()
        assert test_path.exists()

    def test_roundtrip(self, tmp_path: Path, clean_df: pd.DataFrame) -> None:
        train_df, test_df = split(clean_df)
        train_path, _ = save_splits(train_df, test_df, tmp_path)
        reloaded = pd.read_csv(train_path)
        pd.testing.assert_frame_equal(
            reloaded.reset_index(drop=True),
            train_df.reset_index(drop=True),
        )


class TestRun:
    """Tests for the end-to-end run function."""

    def test_end_to_end(self, tmp_path: Path, raw_df: pd.DataFrame) -> None:
        raw_path = tmp_path / "raw" / "churn.csv"
        raw_path.parent.mkdir(parents=True)
        raw_df.to_csv(raw_path, index=False)

        output_dir = tmp_path / "processed"
        train_path, test_path = run(raw_file=raw_path, output_dir=output_dir)

        assert train_path.exists()
        assert test_path.exists()
        train = pd.read_csv(train_path)
        test = pd.read_csv(test_path)
        assert train.isna().sum().sum() == 0
        assert test.isna().sum().sum() == 0
        assert len(train) + len(test) == len(raw_df)
