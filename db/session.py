import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Caminho absoluto baseado na localização deste arquivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DB_PATH = os.path.join(BASE_DIR, "..", "base_livros.db")
# DATABASE_URL = f"sqlite:///{os.path.abspath(DB_PATH)}"

DATABASE_URL = os.getenv("DATABASE_URL")

# # Criação do engine com suporte para SQLite multithread
# engine = create_engine(
#     DATABASE_URL, echo=False, connect_args={"check_same_thread": False}
# )

engine = create_engine(DATABASE_URL, echo=False)

# Configuração da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
