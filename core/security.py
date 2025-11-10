from datetime import timedelta, datetime
from typing import Optional, Union, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from fastapi import HTTPException, Depends, status
from .config import settings
import logging
from sqlalchemy.orm import Session
from models.user_model import User
from core.database import get_db

# Configuración de hashing con Argon2 (sin límite de 72 bytes)
pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],  # Argon2 primero, bcrypt fallback
    deprecated="auto",
    argon2__default_rounds=10,  # Ajusta para seguridad (más = más lento)
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash de password con Argon2 (maneja passwords largos sin truncar).
    """
    if not password:
        raise ValueError("Password cannot be empty")
    
    # Simplificado: Argon2 no necesita truncado ni identify (que es para hashes, no plains)
    return pwd_context.hash(password)

def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None, role: Optional[str] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    to_encode = {"exp": expire, "sub": subject}
    if role:
        to_encode["role"] = role
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # Fetch user from DB to get role (and verify existence/active)
        user = db.query(User).filter(User.username == username).first()
        if user is None or not user.is_active:
            raise credentials_exception
        # Return TokenData with role from DB
        return TokenData(username=username, role=user.role)
    except JWTError:
        raise credentials_exception