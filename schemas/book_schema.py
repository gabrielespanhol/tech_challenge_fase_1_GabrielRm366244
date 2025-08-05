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
        from_attributes = True
