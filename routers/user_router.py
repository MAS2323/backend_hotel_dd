# routers/user_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from core.security import create_access_token, verify_password, get_current_user, settings, get_password_hash
from schemas.user_schema import User, UserCreate, Token
from controllers.user_controller import create_user, get_user, get_user_by_username
from datetime import timedelta

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Your logic here, e.g.:
    hashed_password = get_password_hash(user.password)
    db_user = create_user(db, obj_in=user, hashed_password=hashed_password)
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# routers/user_router.py (extracto del endpoint register)
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
    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user(db, skip=skip, limit=limit)

# Add other routes (e.g., GET /{username}, DELETE /me)