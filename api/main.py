from __future__ import annotations

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.model_loader import get_metadata, load_artifacts
from api.routes.history import router as history_router
from api.routes.model_info import router as model_info_router
from api.routes.predict import router as predict_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    load_dotenv()
    load_artifacts()
    yield


app = FastAPI(
    title="Housing Price Prediction API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration: reads from CORS_ORIGINS env var, defaults to ["*"] for development
cors_origins_str = os.getenv("CORS_ORIGINS", "*")
if cors_origins_str == "*":
    allow_origins = ["*"]
else:
    allow_origins = [origin.strip() for origin in cors_origins_str.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router, prefix="/api/v1")
app.include_router(history_router, prefix="/api/v1")
app.include_router(model_info_router, prefix="/api/v1")


@app.get("/health")
def health() -> dict:
    metadata = get_metadata()
    return {
        "status": "ok",
        "model_version": metadata.get("version", "unknown"),
    }
