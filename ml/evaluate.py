from __future__ import annotations

import argparse
from typing import Dict

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import make_scorer, mean_absolute_error
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor

try:
    from ml.pipeline_utils import (
        add_income_category,
        build_pipeline,
        load_data,
        stratified_split,
    )
except ModuleNotFoundError:
    from pipeline_utils import (  # type: ignore
        add_income_category,
        build_pipeline,
        load_data,
        stratified_split,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run 10-fold CV model comparison.")
    parser.add_argument(
        "--data-path",
        default="data/housing.csv",
        help="Path to training CSV file.",
    )
    return parser.parse_args()


def evaluate_models(data_path: str) -> Dict[str, Dict[str, float]]:
    df = load_data(data_path)
    df = add_income_category(df)
    train_set, _ = stratified_split(df, test_size=0.2, random_state=42)

    train_features = train_set.drop("median_house_value", axis=1)
    train_labels = train_set["median_house_value"].copy()

    num_attributes = train_features.drop("ocean_proximity", axis=1).columns.tolist()
    cat_attributes = ["ocean_proximity"]

    pipeline = build_pipeline(num_attributes, cat_attributes)
    prepared = pipeline.fit_transform(train_features)

    models = {
        "LinearRegression": LinearRegression(),
        "DecisionTreeRegressor": DecisionTreeRegressor(),
        "RandomForestRegressor": RandomForestRegressor(),
    }

    results: Dict[str, Dict[str, float]] = {}
    mae_scorer = make_scorer(mean_absolute_error, greater_is_better=False)

    for model_name, model in models.items():
        mse_scores = cross_val_score(
            model,
            prepared,
            train_labels,
            scoring="neg_mean_squared_error",
            cv=10,
        )
        mae_scores = cross_val_score(
            model,
            prepared,
            train_labels,
            scoring=mae_scorer,
            cv=10,
        )

        rmse = float(np.mean(np.sqrt(-mse_scores)))
        mae = float(np.mean(-mae_scores))

        results[model_name] = {"RMSE": rmse, "MAE": mae}

    return results


def print_table(results: Dict[str, Dict[str, float]]) -> None:
    header = f"{'Model':<24} {'RMSE':>12} {'MAE':>12}"
    sep = "-" * len(header)
    print(header)
    print(sep)
    for model_name, metrics in results.items():
        print(f"{model_name:<24} {metrics['RMSE']:>12.4f} {metrics['MAE']:>12.4f}")


def main() -> None:
    args = parse_args()
    results = evaluate_models(args.data_path)
    print_table(results)


if __name__ == "__main__":
    main()
