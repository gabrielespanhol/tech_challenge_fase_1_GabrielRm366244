import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Chaves secretas (use algo mais seguro em produção)
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "minha_chave_secreta")
    JWT_REFRESH_SECRET_KEY: str = os.getenv(
        "JWT_REFRESH_SECRET_KEY", "minha_chave_refresh_secreta"
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


settings = Settings()
