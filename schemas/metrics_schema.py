from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class MetricsCreate(BaseModel):
    id: int
    method: str
    path: str
    status_code: int
    duration: float
    client_ip: Optional[str]
    user_agent: Optional[str]
    query_params: Optional[str]
    body_size: Optional[int]
    response_size: Optional[int]
    auth_user_id: Optional[str]
    error_message: Optional[str]
    timestamp: datetime


class Metrics(MetricsCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
