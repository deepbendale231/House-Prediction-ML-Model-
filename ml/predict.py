from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Batch inference using saved artifacts.")
    parser.add_argument("--input", required=True, help="Path to input CSV file.")
    parser.add_argument("--output", required=True, help="Path to output CSV file.")
    parser.add_argument(
        "--artifacts-dir",
        default="ml/artifacts",
        help="Directory containing model.pkl and pipeline.pkl.",
    )
    return parser.parse_args()


def load_required_features(artifacts_dir: Path, pipeline) -> list:
    metadata_path = artifacts_dir / "metadata.json"
    if metadata_path.exists():
        with metadata_path.open("r", encoding="utf-8") as f:
            metadata = json.load(f)
        feature_list = metadata.get("feature_list", [])
        if feature_list:
            return feature_list

    if hasattr(pipeline, "feature_names_in_"):
        return list(pipeline.feature_names_in_)

    raise ValueError("Could not determine required feature columns from metadata or pipeline.")


def main() -> None:
    args = parse_args()

    artifacts_dir = Path(args.artifacts_dir)
    input_path = Path(args.input)
    output_path = Path(args.output)

    model_path = artifacts_dir / "model.pkl"
    pipeline_path = artifacts_dir / "pipeline.pkl"

    if not model_path.exists() or not pipeline_path.exists():
        raise FileNotFoundError(
            f"Missing artifacts in {artifacts_dir}. Expected model.pkl and pipeline.pkl"
        )

    model = joblib.load(model_path)
    pipeline = joblib.load(pipeline_path)

    input_df = pd.read_csv(input_path)
    required_columns = load_required_features(artifacts_dir, pipeline)

    missing = [col for col in required_columns if col not in input_df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    transformed = pipeline.transform(input_df[required_columns])
    predictions = model.predict(transformed)

    output_df = input_df.copy()
    output_df["median_house_value"] = predictions

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(output_path, index=False)

    print(f"Predictions written to: {output_path}")


if __name__ == "__main__":
    main()
