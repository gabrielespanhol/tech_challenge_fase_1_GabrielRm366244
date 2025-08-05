from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from fastapi import Query

from db.session import get_db
from models.metrics_model import Metrics as MetricsModel
from schemas.metrics_schema import MetricsCreate, Metrics

metrics_route = APIRouter()


@metrics_route.post(
    "/metrics/", response_model=Metrics, status_code=status.HTTP_201_CREATED
)
def create_metric(metric: MetricsCreate, db: Session = Depends(get_db)):
    db_metric = MetricsModel(**metric.dict())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)  # para carregar id e timestamp do DB
    return Metrics.from_orm(db_metric)


@metrics_route.get("/metrics/", response_model=List[Metrics])
def list_metrics(
    skip: int = 0,
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
):
    metrics = db.query(MetricsModel).offset(skip).limit(limit).all()
    return [Metrics.from_orm(m) for m in metrics]
