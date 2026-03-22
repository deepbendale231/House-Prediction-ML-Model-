from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

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
    parser = argparse.ArgumentParser(description="Train RandomForest model and save artifacts.")
    parser.add_argument(
        "--data-path",
        default="data/housing.csv",
        help="Path to training CSV file.",
    )
    parser.add_argument(
        "--output-dir",
        default="ml/artifacts",
        help="Directory to save model artifacts.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = load_data(args.data_path)
    df = add_income_category(df)
    train_set, test_set = stratified_split(df, test_size=0.2, random_state=42)

    train_features = train_set.drop("median_house_value", axis=1)
    train_labels = train_set["median_house_value"].copy()

    test_features = test_set.drop("median_house_value", axis=1)
    test_labels = test_set["median_house_value"].copy()

    num_attributes = train_features.drop("ocean_proximity", axis=1).columns.tolist()
    cat_attributes = ["ocean_proximity"]

    pipeline = build_pipeline(num_attributes, cat_attributes)
    train_prepared = pipeline.fit_transform(train_features)

    model = RandomForestRegressor()
    model.fit(train_prepared, train_labels)

    test_prepared = pipeline.transform(test_features)
    predictions = model.predict(test_prepared)

    rmse = mean_squared_error(test_labels, predictions) ** 0.5
    mae = mean_absolute_error(test_labels, predictions)
    r2 = r2_score(test_labels, predictions)

    model_path = output_dir / "model.pkl"
    pipeline_path = output_dir / "pipeline.pkl"
    metadata_path = output_dir / "metadata.json"

    joblib.dump(model, model_path)
    joblib.dump(pipeline, pipeline_path)

    metadata = {
        "version": "v1.0",
        "feature_list": train_features.columns.tolist(),
        "rmse": float(rmse),
        "mae": float(mae),
        "r2": float(r2),
        "trained_at": datetime.now(timezone.utc).isoformat(),
    }

    with metadata_path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"Saved model: {model_path}")
    print(f"Saved pipeline: {pipeline_path}")
    print(f"Saved metadata: {metadata_path}")
    print(f"RMSE={rmse:.4f} MAE={mae:.4f} R2={r2:.4f}")


if __name__ == "__main__":
    main()
