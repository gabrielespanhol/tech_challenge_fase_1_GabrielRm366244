from pydantic import BaseModel


class BookSchema(BaseModel):
    id: int
    titulo: str
    preco: float
    estrelas: int
    disponibilidade: str
    categoria: str
    imagem: str
    link: str

    class Config:
        orm_mode = True  # Permite conversão direta de objetos SQLAlchemy
