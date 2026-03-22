from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class PredictionInput(BaseModel):
    longitude: float
    latitude: float
    housing_median_age: float
    total_rooms: float
    total_bedrooms: float
    population: float
    households: float
    median_income: float
    ocean_proximity: str


class PredictionOutput(BaseModel):
    predicted_price: float
    prediction_id: str
    model_version: str
    created_at: str


class PredictionRecord(PredictionOutput):
    longitude: float
    latitude: float
    housing_median_age: float
    total_rooms: float
    total_bedrooms: float
    population: float
    households: float
    median_income: float
    ocean_proximity: str

    model_config = ConfigDict(extra="ignore")
