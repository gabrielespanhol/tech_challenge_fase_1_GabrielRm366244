from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from db.base import Base


class PredictionModel(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(
        Integer, ForeignKey("books.id"), nullable=False
    )  # relação com books.id
    predicted_value = Column(Float, nullable=False)
    model_name = Column(String, default="default_model")
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
