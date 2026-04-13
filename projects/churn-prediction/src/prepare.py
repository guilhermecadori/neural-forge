"""Load raw churn data, impute missing values, and persist train/test splits."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

RAW_FILE = Path("data/raw/churn.csv")
PROCESSED_DIR = Path("data/processed")
TEST_SIZE = 0.2
RANDOM_STATE = 42


def load_raw(path: Path = RAW_FILE) -> pd.DataFrame:
    """Read the raw churn CSV from disk.

    Raises:
        FileNotFoundError: If the raw file does not exist.
    """
    if not path.exists():
        raise FileNotFoundError(f"Raw data not found: {path}. Run dvc pull first.")
    return pd.read_csv(path)


def impute_median(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing numeric values with column medians."""
    return df.fillna(df.median(numeric_only=True))


def split(
    df: pd.DataFrame,
    test_size: float = TEST_SIZE,
    random_state: int = RANDOM_STATE,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Stratification-free train/test split."""
    train_df, test_df = train_test_split(
        df, test_size=test_size, random_state=random_state
    )
    return train_df, test_df


def save_splits(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    output_dir: Path = PROCESSED_DIR,
) -> tuple[Path, Path]:
    """Write train and test DataFrames to CSV."""
    output_dir.mkdir(parents=True, exist_ok=True)
    train_path = output_dir / "train.csv"
    test_path = output_dir / "test.csv"
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    return train_path, test_path


def run(
    raw_file: Path = RAW_FILE,
    output_dir: Path = PROCESSED_DIR,
) -> tuple[Path, Path]:
    """End-to-end preparation pipeline."""
    df = load_raw(raw_file)
    df = impute_median(df)
    train_df, test_df = split(df)
    return save_splits(train_df, test_df, output_dir)


if __name__ == "__main__":
    run()
