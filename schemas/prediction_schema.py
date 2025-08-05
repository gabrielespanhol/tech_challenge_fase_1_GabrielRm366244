# schemas/prediction_schema.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PredictionCreate(BaseModel):
    book_id: int
    predicted_value: float
    model_name: Optional[str] = "default_model"


class PredictionResponse(PredictionCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
