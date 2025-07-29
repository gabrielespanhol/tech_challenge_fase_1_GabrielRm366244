from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from scripts.web_scraping import *
from db.create_tables import create_tables
from db.session import SessionLocal
from models.book_model import BookModel
from routes.livros_route import livros_routes  # Importa o arquivo de rotas

app = FastAPI(
    title="API Gabriel Espanhol RM366244",
    version="1.0.0",
    description="Tech Challenge 2025 6MLET, API Pública para Consulta de Livros",
)

create_tables()

app.include_router(livros_routes)
