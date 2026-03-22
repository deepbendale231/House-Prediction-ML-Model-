from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import joblib
from dotenv import load_dotenv


_MODEL = None
_PIPELINE = None
_METADATA: dict[str, Any] | None = None


def _resolve_paths() -> tuple[Path, Path, Path]:
    load_dotenv()

    model_path = Path(os.getenv("MODEL_PATH", "ml/artifacts/model.pkl"))
    pipeline_path = Path(os.getenv("PIPELINE_PATH", "ml/artifacts/pipeline.pkl"))
    metadata_path = model_path.parent / "metadata.json"

    return model_path, pipeline_path, metadata_path


def load_artifacts() -> None:
    global _MODEL, _PIPELINE, _METADATA

    if _MODEL is not None and _PIPELINE is not None and _METADATA is not None:
        return

    model_path, pipeline_path, metadata_path = _resolve_paths()

    missing = [
        str(path)
        for path in (model_path, pipeline_path, metadata_path)
        if not path.exists()
    ]
    if missing:
        raise FileNotFoundError(
            "Missing model artifacts: " + ", ".join(missing)
        )

    _MODEL = joblib.load(model_path)
    _PIPELINE = joblib.load(pipeline_path)

    with metadata_path.open("r", encoding="utf-8") as f:
        _METADATA = json.load(f)


def get_model() -> Any:
    if _MODEL is None:
        raise RuntimeError("Model is not loaded. Call load_artifacts() on startup.")
    return _MODEL


def get_pipeline() -> Any:
    if _PIPELINE is None:
        raise RuntimeError("Pipeline is not loaded. Call load_artifacts() on startup.")
    return _PIPELINE


def get_metadata() -> dict[str, Any]:
    if _METADATA is None:
        raise RuntimeError("Metadata is not loaded. Call load_artifacts() on startup.")
    return _METADATA
