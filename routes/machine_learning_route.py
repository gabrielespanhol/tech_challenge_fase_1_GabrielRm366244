from fastapi import APIRouter, Body
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.book_model import BookModel
from models.prediction_model import PredictionModel
from schemas.prediction_schema import PredictionCreate, PredictionResponse
from typing import List
from fastapi.responses import JSONResponse


machine_learning_route = APIRouter()


@machine_learning_route.get("/api/v1/ml/features")
def get_features():
    session: Session = SessionLocal()
    try:
        livros = session.query(
            BookModel.id,
            BookModel.preco,
            BookModel.estrelas,
            BookModel.disponibilidade,
            BookModel.categoria,
        ).all()

        features = []
        for livro in livros:
            features.append(
                {
                    "id": livro.id,
                    "preco": livro.preco,
                    "estrelas": livro.estrelas,
                    "disponibilidade": 1 if "In stock" in livro.disponibilidade else 0,
                    "categoria": livro.categoria,
                }
            )

        return {"features": features, "total": len(features)}

    except Exception as e:
        return JSONResponse(content={"erro": str(e)}, status_code=500)
    finally:
        session.close()


@machine_learning_route.get("/api/v1/ml/training-data")
def get_training_data():
    session: Session = SessionLocal()
    try:
        livros = session.query(BookModel).all()

        dataset = [
            {
                "id": livro.id,
                "titulo": livro.titulo,
                "preco": livro.preco,
                "estrelas": livro.estrelas,
                "disponibilidade": livro.disponibilidade,
                "categoria": livro.categoria,
                "link": livro.link,
            }
            for livro in livros
        ]

        return {"dataset": dataset, "total": len(dataset)}

    except Exception as e:
        return JSONResponse(content={"erro": str(e)}, status_code=500)
    finally:
        session.close()


@machine_learning_route.post("/api/v1/ml/predictions", status_code=201)
def receber_predicoes(predicoes: List[PredictionCreate] = Body(...)):
    session: Session = SessionLocal()
    try:
        predicoes_salvas = []

        for pred in predicoes:
            livro = (
                session.query(BookModel).filter(BookModel.id == pred.book_id).first()
            )
            if not livro:
                return JSONResponse(
                    content={"erro": f"Livro com id {pred.book_id} não encontrado."},
                    status_code=400,
                )

            nova_predicao = PredictionModel(
                book_id=pred.book_id,
                predicted_value=pred.predicted_value,
                model_name=pred.model_name,
            )
            session.add(nova_predicao)
            predicoes_salvas.append(nova_predicao)

        session.commit()
        session.refresh(nova_predicao)
        return JSONResponse(status_code=201, content={"message": "Criado"})

    except Exception as e:
        session.rollback()
        return JSONResponse(content={"erro": str(e)}, status_code=500)
    finally:
        session.close()


@machine_learning_route.get(
    "/api/v1/ml/predictions-list", response_model=List[PredictionResponse]
)
def listar_predicoes():
    session: Session = SessionLocal()
    try:
        predicoes = session.query(PredictionModel).all()
        return predicoes
    except Exception as e:
        return JSONResponse(content={"erro": str(e)}, status_code=500)
    finally:
        session.close()
