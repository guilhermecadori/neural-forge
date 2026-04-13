"""Shared fixtures for churn-prediction tests."""

from __future__ import annotations

import pandas as pd
import pytest


@pytest.fixture
def raw_df() -> pd.DataFrame:
    """Minimal DataFrame mimicking churn.csv with a missing value."""
    return pd.DataFrame(
        {
            "Age": [25, 30, None, 45, 50, 35, 28, 40, 55, 60],
            "MonthlyCharges": [
                50.0,
                70.0,
                65.0,
                80.0,
                None,
                55.0,
                60.0,
                75.0,
                90.0,
                85.0,
            ],
            "Tenure": [12, 24, 36, 48, 6, 18, 30, 42, 54, 3],
            "Churn": [0, 1, 0, 1, 0, 0, 1, 1, 0, 1],
        }
    )


@pytest.fixture
def clean_df(raw_df: pd.DataFrame) -> pd.DataFrame:
    """DataFrame with no missing values (median-imputed)."""
    return raw_df.fillna(raw_df.median(numeric_only=True))
