# core/security.py
from datetime import timedelta, datetime
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import HTTPException
from .config import settings
import logging

# Configuración de hashing con Argon2 (sin límite de 72 bytes)
pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],  # Argon2 primero, bcrypt fallback
    deprecated="auto",
    argon2__default_rounds=10,  # Ajusta para seguridad (más = más lento)
)

class TokenData(BaseModel):
    username: Optional[str] = None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash de password con Argon2 (sin límite de longitud).
    Truncado opcional para bcrypt fallback.
    """
    if not password:
        raise ValueError("Password cannot be empty")
    
    try:
        # Si usa bcrypt fallback, trunca (pero Argon2 no necesita)
        if pwd_context.identify(password) == "bcrypt":  # Solo si detecta bcrypt
            password_bytes = password.encode('utf-8')
            if len(password_bytes) > 72:
                logging.warning(f"Password truncated to 72 bytes for bcrypt fallback: original length {len(password_bytes)}")
                password_bytes = password_bytes[:72]
                password = password_bytes.decode('utf-8')
        
        return pwd_context.hash(password)
    except ValueError as e:
        if "72 bytes" in str(e):
            raise HTTPException(status_code=422, detail="Contraseña demasiado larga para bcrypt. Usa menos de 72 caracteres.")
        raise

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_user(token: str, db):  # db será inyectado en routers
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    # Buscar user en DB (se implementa en user controllers/routers)
    return token_data  # Placeholder; expandir en routers