from sqlalchemy.orm import Session
from schemas.user_schema import UserCreate, User
from models.user_model import User
from core.security import get_password_hash
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

def create_user(db: Session, obj_in: UserCreate, hashed_password: str = None):
    """
    Crea un nuevo usuario en la DB con password hasheado.
    obj_in: UserCreate con username, email, password (pero password no se guarda plano).
    hashed_password: Opcional; si no, se hashea desde obj_in.password.
    """
    # Si hashed_password no se proporciona, hashea obj_in.password
    if hashed_password is None:
        hashed_password = get_password_hash(obj_in.password)
    
    # Verifica si username/email ya existe (evita duplicados)
    existing_user = db.query(User).filter(
        (User.username == obj_in.username) | (User.email == obj_in.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username o email ya existe")

    # Crea el objeto User con datos de obj_in, hashed_password y defaults
    db_user = User(
        username=obj_in.username,
        email=obj_in.email,
        hashed_password=hashed_password,
        role="user",  # Default (ajusta si necesitas)
        is_active=True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"Usuario creado: {db_user.username}")
    return db_user

def get_user(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene todos los usuarios (para GET /users).
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users

def get_user_by_username(db: Session, username: str):
    """
    Obtiene usuario por username (para login).
    """
    try:
        return db.query(User).filter(User.username == username).first()
    except Exception as e:
        logger.error(f"Error querying user {username}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en DB: {str(e)}")

def update_user_role(db: Session, user_id: int, role: str):
    """
    Actualiza rol de usuario (para admin).
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = role
    db.commit()
    db.refresh(user)
    return user

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene todos los usuarios con paginación
    """
    return db.query(User).offset(skip).limit(limit).all()