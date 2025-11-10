from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from core.security import get_current_user, TokenData
from controllers.user_controller import get_all_users, update_user_role
from schemas.user_schema import UserOut, RoleUpdate # Importa UserOut
import logging

logger = logging.getLogger(__name__)

admin_router = APIRouter()
def require_admin(current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    logger.info(f"Require admin check for user: {current_user.username}, role: {current_user.role}")
    if current_user.role != "admin":
        logger.warning(f"Access denied for {current_user.username}: role {current_user.role} != admin")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

@admin_router.get("/users", response_model=List[UserOut])  # ✅ FIX: Usa UserOut (sin password)
def read_users(skip: int = 0, limit: int = 100, current_user: TokenData = Depends(require_admin), db: Session = Depends(get_db)):
    logger.info("Admin users endpoint called successfully")
    return get_all_users(db, skip=skip, limit=limit)

# Endpoint para update role (si no lo tienes)
@admin_router.put("/users/{user_id}/role", response_model=dict)
def update_user_role_endpoint(
    user_id: int,
    role: RoleUpdate,  # ✅ Desde body JSON
    current_user: TokenData = Depends(require_admin),
    db: Session = Depends(get_db)
):
    logger.info(f"Updating role for user_id {user_id} to {role.role}")
    updated_user = update_user_role(db, user_id=user_id, role=role.role)
    return {
        "message": "Role updated successfully",
        "user": UserOut.from_orm(updated_user)  # Retorna UserOut sin password
    }
    


def require_admin(current_user: TokenData = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

@admin_router.get("/users")
def get_admin_users(current_user: TokenData = Depends(require_admin)):
    """Este endpoint será /admin/users cuando se registre"""
    return {"message": "Admin users endpoint"}
