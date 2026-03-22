from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, Query

from api.db import get_supabase
from api.schemas import PredictionRecord


router = APIRouter(tags=["history"])


@router.get("/predictions", response_model=List[PredictionRecord])
def list_predictions(
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> List[PredictionRecord]:
    try:
        response = (
            get_supabase()
            .table("predictions")
            .select("*")
            .order("created_at", desc=True)
            .range(offset, offset + limit - 1)
            .execute()
        )
        rows = response.data or []
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database fetch failed: {exc}") from exc

    records: List[PredictionRecord] = []
    for row in rows:
        features = row.get("features") or {}
        merged = {
            "predicted_price": float(row.get("predicted_price", 0.0)),
            "prediction_id": str(row.get("id", "")),
            "model_version": str(row.get("model_version", "unknown")),
            "created_at": str(row.get("created_at", "")),
            **features,
        }
        records.append(PredictionRecord(**merged))

    return records
