from fastapi import FastAPI
from routes.livros_route import livros_routes
from db.create_tables import create_tables

app = FastAPI(
    title="API Gabriel Espanhol RM366244",
    version="1.0.0",
    description="Tech Challenge 2025 6MLET, API Pública para Consulta de Livros",
)


# Garante que as tabelas sejam criadas ao iniciar o app
@app.on_event("startup")
def startup_event():
    create_tables()


# Inclui as rotas
app.include_router(livros_routes)
