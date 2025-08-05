import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Caminho absoluto baseado na localização deste arquivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# DEV: Banco SQLite local
DB_PATH = os.path.join(BASE_DIR, "..", "base_livros.db")
DATABASE_URL = f"sqlite:///{os.path.abspath(DB_PATH)}"

# Criação do engine com suporte para SQLite multithread
engine = create_engine(
    DATABASE_URL, echo=False, connect_args={"check_same_thread": False}
)

# PROD:
# DATABASE_URL = os.getenv("DATABASE_URL")
# engine = create_engine(DATABASE_URL, echo=False)

# Configuração da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency do FastAPI para obter a sessão do banco
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
