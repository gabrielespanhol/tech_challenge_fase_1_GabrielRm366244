from sqlalchemy import Column, Integer, String, Float, DateTime, func
from db.base import Base  # seu declarative_base


class Metrics(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    method = Column(String, nullable=False)
    path = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
    duration = Column(Float, nullable=False)
    client_ip = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    query_params = Column(String, nullable=True)
    body_size = Column(Integer, nullable=True)
    response_size = Column(Integer, nullable=True)
    auth_user_id = Column(String, nullable=True)
    error_message = Column(String, nullable=True)
    timestamp = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
