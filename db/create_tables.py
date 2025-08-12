from db.session import engine
from db.base import Base
from models.book_model import BookModel
from models.prediction_model import PredictionModel
from models.metrics_model import Metrics
from models.user_model import User


def create_tables():
    Base.metadata.create_all(bind=engine)
