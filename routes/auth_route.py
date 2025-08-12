from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.session import get_db
from models.user_model import User
from schemas.user_schema import UserCreate, UserLogin, UserResponse, Token
from scripts.auth import get_current_user
from scripts.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)

auth_route = APIRouter(prefix="/api/v1/auth")


@auth_route.post(
    "/createUser", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Checa se usuário já existe
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Usuário já existe")

    # Cria novo usuário
    hashed_pw = hash_password(user.password)
    db_user = User(username=user.username, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Criado"})


@auth_route.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas"
        )

    access_token = create_access_token({"sub": str(db_user.id)})
    refresh_token = create_refresh_token({"sub": str(db_user.id)})
    return Token(access_token=access_token, refresh_token=refresh_token)


@auth_route.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str):
    try:
        payload = decode_refresh_token(refresh_token)
        user_id = payload.get("sub")
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
        )

    new_access = create_access_token({"sub": str(user_id)})
    new_refresh = create_refresh_token({"sub": str(user_id)})
    return Token(access_token=new_access, refresh_token=new_refresh)
