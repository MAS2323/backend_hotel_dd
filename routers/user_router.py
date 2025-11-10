from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models.user_model import User
from core.database import get_db
from core.security import (
    create_access_token, verify_password, get_current_user, settings, get_password_hash, TokenData
)
from schemas.user_schema import User, UserCreate, Token, UserOut
from controllers.user_controller import create_user, get_user, get_user_by_username
from datetime import timedelta

import logging

logger = logging.getLogger(__name__)

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = get_password_hash(user.password)
    except HTTPException:
        raise  # Propaga el 422 de security.py
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
    db_user = create_user(db, obj_in=user, hashed_password=hashed_password)
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    # ✅ FIX: Usa subject y role, no data
    access_token = create_access_token(
        subject=db_user.username,
        role=db_user.role,
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.get("/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 100, current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user(db, skip=skip, limit=limit)

@user_router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Intento de login para: {user.username}")
        # Busca el usuario existente
        db_user = get_user_by_username(db, username=user.username)
        logger.info(f"Usuario encontrado: {db_user is not None}")
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verifica password
        if not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Genera token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        # ✅ FIX: Usa subject y role, no data
        access_token = create_access_token(
            subject=db_user.username,
            role=db_user.role,
            expires_delta=access_token_expires
        )
        logger.info("Login exitoso")
        return {"access_token": access_token, "token_type": "bearer"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en login: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# Add other routes (e.g., GET /{username}, DELETE /me)