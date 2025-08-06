from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes.livros_route import book_route
from routes.metrics_route import metrics_route
from routes.machine_learning_route import machine_learning_route
from db.create_tables import create_tables
from middlewares import MetricsMiddleware

app = FastAPI(
    title="API Gabriel Espanhol RM366244",
    version="1.0.0",
    description="Tech Challenge 2025 6MLET, API Pública para Consulta de Livros",
)


@app.on_event("startup")
def startup_event():
    create_tables()


app.include_router(book_route, tags=["Books"])
app.include_router(machine_learning_route, tags=["Machine Learning"])
app.include_router(metrics_route, tags=["Metrics"])

app.add_middleware(MetricsMiddleware)
