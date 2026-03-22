from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def load_data(path: str) -> pd.DataFrame:
    """Load a CSV dataset from a relative or absolute path."""
    data_path = Path(path)
    return pd.read_csv(data_path)


def add_income_category(df: pd.DataFrame) -> pd.DataFrame:
    """Add stratification buckets based on median_income."""
    output = df.copy()
    output["income_cat"] = pd.cut(
        output["median_income"],
        bins=[0.0, 1.5, 3.0, 4.5, 6.0, float("inf")],
        labels=[1, 2, 3, 4, 5],
    )
    return output


def stratified_split(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Return train/test splits stratified by income_cat."""
    splitter = StratifiedShuffleSplit(
        n_splits=1,
        test_size=test_size,
        random_state=random_state,
    )

    for train_idx, test_idx in splitter.split(df, df["income_cat"]):
        train_set = df.loc[train_idx].drop("income_cat", axis=1).copy()
        test_set = df.loc[test_idx].drop("income_cat", axis=1).copy()
        return train_set, test_set

    raise RuntimeError("Failed to create stratified split.")


def build_pipeline(
    num_attributes: list,
    cat_attributes: list,
) -> ColumnTransformer:
    """Build the preprocessing pipeline used by training and inference."""
    num_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    cat_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder()),
        ]
    )

    return ColumnTransformer(
        [
            ("num", num_pipeline, num_attributes),
            ("cat", cat_pipeline, cat_attributes),
        ]
    )
