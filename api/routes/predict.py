from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

import pandas as pd
from fastapi import APIRouter, HTTPException

from api.db import get_supabase
from api.model_loader import get_metadata, get_model, get_pipeline
from api.schemas import PredictionInput, PredictionOutput


router = APIRouter(tags=["predict"])


@router.post("/predict", response_model=PredictionOutput)
def predict(payload: PredictionInput) -> PredictionOutput:
    try:
        metadata = get_metadata()
        pipeline = get_pipeline()
        model = get_model()

        features = payload.model_dump()
        feature_df = pd.DataFrame([features])

        transformed = pipeline.transform(feature_df)
        predicted_price = round(float(model.predict(transformed)[0]), 2)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Inference failed: {exc}") from exc

    created_at = datetime.now(timezone.utc).isoformat()
    model_version = str(metadata.get("version", "unknown"))

    record = {
        "features": features,
        "predicted_price": predicted_price,
        "model_version": model_version,
        "created_at": created_at,
    }

    try:
        response = (
            get_supabase()
            .table("predictions")
            .insert(record)
            .execute()
        )
        inserted = (response.data or [{}])[0]
        prediction_id = str(inserted.get("id", uuid4()))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database insert failed: {exc}") from exc

    return PredictionOutput(
        predicted_price=predicted_price,
        prediction_id=prediction_id,
        model_version=model_version,
        created_at=created_at,
    )
