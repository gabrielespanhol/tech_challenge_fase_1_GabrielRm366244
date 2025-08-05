from fastapi import APIRouter, Body, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text, func
from db.session import SessionLocal
from models.book_model import BookModel
from schemas.book_schema import BookSchema
from scripts.web_scraping import extrair_todos_os_livros
from typing import List, Optional
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

book_route = APIRouter()


def parse_preco(preco_str):
    if isinstance(preco_str, str):
        try:
            preco_tratado = float(preco_str.replace("Â£", "").strip())
            return preco_tratado
        except:
            return 0.0
    return 0.0


@book_route.post("/api/v1/scraping/trigger")
def carregar_base():
    session: Session = SessionLocal()
    try:
        # Extrai todos os livros do site
        livros_extraidos = extrair_todos_os_livros()
        if not livros_extraidos:
            return JSONResponse(
                content={"mensagem": "Nenhum livro encontrado no scraping."},
                status_code=404,
            )

        # Obtém os links dos livros já cadastrados para evitar duplicatas
        links_existentes = {livro.link for livro in session.query(BookModel.link).all()}

        # Filtra os livros novos (não duplicados)
        livros_novos = [
            BookModel(
                titulo=livro["titulo"],
                preco=float(livro["preco"].replace("Â£", "").strip()),
                estrelas=int(livro["estrelas"]),
                disponibilidade=livro["disponibilidade"],
                categoria=livro["categoria"],
                imagem=livro["imagem"],
                link=livro["link"],
            )
            for livro in livros_extraidos
            if livro["link"] not in links_existentes
        ]

        # Se não há novos livros, responde com aviso
        if not livros_novos:
            return {
                "mensagem": "Nenhum novo livro para inserir. A base já está atualizada."
            }

        # Insere os livros em lote no banco
        session.bulk_save_objects(livros_novos)
        session.commit()

        return {
            "mensagem": "Base carregada com sucesso.",
            "livros_inseridos": len(livros_novos),
            "total_livros_scrapeados": len(livros_extraidos),
        }

    except SQLAlchemyError as e:
        session.rollback()
        return JSONResponse(
            content={"mensagem": f"Erro de banco de dados: {str(e)}"}, status_code=500
        )
    except Exception as e:
        session.rollback()
        return JSONResponse(
            content={"mensagem": f"Erro inesperado: {str(e)}"}, status_code=500
        )
    finally:
        session.close()


@book_route.delete("/api/v1/scraping/trigger/delete")
def truncate_base_livros():
    session: Session = SessionLocal()
    try:
        session.query(BookModel).delete()
        session.commit()
        return {
            "mensagem": "Base limpa com sucesso.",
        }

    except SQLAlchemyError as e:
        session.rollback()
        return JSONResponse(
            content={"mensagem": f"Erro de banco de dados: {str(e)}"}, status_code=500
        )
    except Exception as e:
        session.rollback()
        return JSONResponse(
            content={"mensagem": f"Erro inesperado: {str(e)}"}, status_code=500
        )
    finally:
        session.close()


@book_route.get("/api/v1/books", response_model=List[BookSchema])
def listar_livros(limit: Optional[int] = Query(default=None, ge=1)):
    session: Session = SessionLocal()
    try:
        query = session.query(BookModel)

        if limit:
            livros = query.limit(limit).all()
        else:
            livros = query.all()

        return livros

    except Exception as e:
        return JSONResponse(
            content={"mensagem": f"Erro ao listar os livros: {str(e)}"}, status_code=500
        )
    finally:
        session.close()


@book_route.get("/api/v1/books/search", response_model=List[BookSchema])
def buscar_livros(
    title: Optional[str] = Query(None), category: Optional[str] = Query(None)
):
    session: Session = SessionLocal()
    try:
        query = session.query(BookModel)

        if title:
            query = query.filter(BookModel.titulo.ilike(f"%{title}%"))
        if category:
            query = query.filter(BookModel.categoria.ilike(f"%{category}%"))

        livros = query.all()
        return livros

    except Exception as e:
        return JSONResponse(
            content={"mensagem": f"Erro na busca: {str(e)}"}, status_code=500
        )
    finally:
        session.close()


@book_route.get("/api/v1/books/top-rated")
def listar_top_livros(limit: int = 10):
    session: Session = SessionLocal()

    livros_top = (
        session.query(BookModel).order_by(BookModel.estrelas.desc()).limit(limit).all()
    )

    return livros_top


@book_route.get("/api/v1/books/price-range", response_model=List[BookSchema])
def filtrar_livros_por_preco(min: float = Query(0), max: float = Query(9999)):
    session: Session = SessionLocal()

    if min > max:
        raise HTTPException(
            status_code=400, detail="O valor mínimo não pode ser maior que o máximo."
        )

    livros = (
        session.query(BookModel)
        .filter(BookModel.preco >= min, BookModel.preco <= max)
        .order_by(BookModel.preco.asc())
        .all()
    )

    return livros


@book_route.get("/api/v1/books/{id}", response_model=BookSchema)
def obter_livro_por_id(id: int):
    session: Session = SessionLocal()
    try:
        livro = session.query(BookModel).filter(BookModel.id == id).first()
        if not livro:
            return JSONResponse(
                content={"mensagem": "Livro não encontrado"}, status_code=404
            )
        return livro
    except Exception as e:
        return JSONResponse(
            content={"mensagem": f"Erro ao buscar livro: {str(e)}"}, status_code=500
        )
    finally:
        session.close()


@book_route.get("/api/v1/categories")
def listar_categorias():
    session: Session = SessionLocal()
    try:
        categorias = session.query(BookModel.categoria).distinct().all()
        lista = [cat[0] for cat in categorias if cat[0]]
        return {"categorias": lista, "total": len(lista)}
    except Exception as e:
        return JSONResponse(
            content={"mensagem": f"Erro ao listar categorias: {str(e)}"},
            status_code=500,
        )
    finally:
        session.close()


@book_route.get("/api/v1/health")
def verificar_status():
    session: Session = SessionLocal()
    try:
        session.execute(text("SELECT 1"))  # Verifica conexão com o banco
        return {"status": "ok", "mensagem": "API online e banco acessível"}
    except Exception as e:
        return JSONResponse(
            content={
                "status": "erro",
                "mensagem": f"Falha ao conectar com o banco: {str(e)}",
            },
            status_code=500,
        )
    finally:
        session.close()


#  overview


@book_route.get("/api/v1/stats/overview")
def overview_geral():
    session: Session = SessionLocal()
    total_livros = session.query(BookModel).count()
    preco_medio = session.query(func.avg(BookModel.preco)).scalar()
    preco_medio_formatado = f"R$ {round(preco_medio, 2)}"

    # Distribuição de ratings (estrelas)
    distribuicao_rating = (
        session.query(BookModel.estrelas, func.count(BookModel.id))
        .group_by(BookModel.estrelas)
        .order_by(BookModel.estrelas)
        .all()
    )

    # Convertendo para dicionário: {estrelas: quantidade}
    distribuicao_dict = {
        estrela: quantidade for estrela, quantidade in distribuicao_rating
    }

    return {
        "total_de_livros": total_livros,
        "preco_medio": preco_medio_formatado,
        "distribuicao_de_rating": distribuicao_dict,
    }


@book_route.get("/api/v1/stats/categories")
def stats_por_categoria():
    session: Session = SessionLocal()

    resultados = (
        session.query(
            BookModel.categoria,
            func.count(BookModel.id).label("quantidade"),
            func.avg(BookModel.preco).label("preco_medio"),
            func.min(BookModel.preco).label("preco_min"),
            func.max(BookModel.preco).label("preco_max"),
        )
        .group_by(BookModel.categoria)
        .order_by(BookModel.categoria)
        .all()
    )

    categorias_stats = []
    for categoria, qtd, preco_medio, preco_min, preco_max in resultados:
        categorias_stats.append(
            {
                "categoria": categoria,
                "quantidade de livros": qtd,
                "preco_medio": f"R$ {round(preco_medio, 2)}",
                "preco_min": f"R$ {round(float(preco_min), 2)}",
                "preco_max": f"R$ {round(float(preco_max), 2)}",
            }
        )

    return {"categorias": categorias_stats}
