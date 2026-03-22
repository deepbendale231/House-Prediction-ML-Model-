from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.model_loader import get_metadata


router = APIRouter(tags=["model"])


@router.get("/model")
def model_info() -> dict:
    try:
        metadata = get_metadata()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Metadata unavailable: {exc}") from exc

    return {
        "version": metadata.get("version", "unknown"),
        "rmse": metadata.get("rmse"),
        "mae": metadata.get("mae"),
        "r2": metadata.get("r2"),
        "features_used": metadata.get("feature_list", []),
        "trained_at": metadata.get("trained_at", ""),
    }
