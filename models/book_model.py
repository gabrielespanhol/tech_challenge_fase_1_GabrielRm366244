from sqlalchemy import Column, Integer, String, Float
from db.base import Base


class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    preco = Column(Float)
    estrelas = Column(Integer)
    disponibilidade = Column(String)
    categoria = Column(String)
    imagem = Column(String)
    link = Column(String)
