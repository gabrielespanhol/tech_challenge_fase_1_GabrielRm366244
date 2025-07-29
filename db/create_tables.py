from db.session import engine
from db.base import Base
from models.book_model import BookModel


def create_tables():
    Base.metadata.create_all(bind=engine)
