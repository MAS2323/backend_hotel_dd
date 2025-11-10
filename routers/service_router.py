# routers/service_router.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form  # ✅ Added Form
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from schemas.service_schema import Service, ServiceCreate, ServiceUpdate  # Keep for responses
from controllers.service_controller import (
    create_service, get_services, update_service, delete_service
)
from core.security import get_current_user, TokenData
import logging

logger = logging.getLogger(__name__)

# ==================== ROUTER PÚBLICO ====================
public_service_router = APIRouter(
    prefix="/services",
    tags=["services"],
    responses={404: {"description": "Not found"}}
)

@public_service_router.get(
    "/",
    response_model=List[Service],
    summary="Obtener todos los servicios (público)"
)
def read_services(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Endpoint público para listar servicios"""
    return get_services(db, skip=skip, limit=limit)

# ==================== ROUTER ADMIN ====================
admin_service_router = APIRouter(
    prefix="/admin/services",  # ✅ PREFIJO COMPLETO Y ÚNICO
    tags=["admin services"],
    dependencies=[Depends(get_current_user)],  # Auth en TODAS las rutas
    responses={403: {"description": "Not enough permissions"}}
)

def require_admin(current_user: TokenData = Depends(get_current_user)):
    """Dependencia para validar rol de admin"""
    if not current_user or current_user.role != "admin":
        logger.warning(f"User {current_user.sub if current_user else 'unknown'} tried to access admin endpoint")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

@admin_service_router.get(
    "/",
    response_model=List[Service],
    summary="Listar servicios (admin)"
)
def read_admin_services(
    skip: int = 0,
    limit: int = 100,
    current_user: TokenData = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Endpoint admin para listar todos los servicios"""
    logger.info(f"Admin {current_user.sub} fetching services")
    return get_services(db, skip=skip, limit=limit)

@admin_service_router.post(
    "/",
    response_model=Service,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo servicio"
)
def create_admin_service(
    title: str = Form(..., description="Título del servicio"),  # ✅ Changed: Form for multipart
    desc: str = Form(..., description="Descripción del servicio"),
    file: UploadFile = File(..., description="Icono del servicio (requerido)"),
    current_user: TokenData = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Crear un nuevo servicio con icono"""
    # ✅ Pass raw str to controller (no ServiceCreate needed here)
    try:
        return create_service(db, title=title, desc=desc, file=file)
    except ValueError as e:  # ✅ Changed: Catch ValueError for validation
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@admin_service_router.put(
    "/{service_id}",
    response_model=Service,
    summary="Actualizar servicio"
)
def update_admin_service(
    service_id: int,
    title: Optional[str] = Form(None, description="Nuevo título (opcional)"),  # ✅ Form optional
    desc: Optional[str] = Form(None, description="Nueva descripción (opcional)"),
    file: Optional[UploadFile] = File(None, description="Nuevo icono (opcional)"),
    current_user: TokenData = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Actualizar un servicio existente"""
    # ✅ Pass raw values; controller handles None
    try:
        return update_service(db, service_id=service_id, title=title, desc=desc, file=file)
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=404, detail=str(e))  # 404 for not found
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@admin_service_router.delete(
    "/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar servicio"
)
def delete_admin_service(
    service_id: int,
    current_user: TokenData = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Eliminar un servicio y su icono de Cloudinary"""
    try:
        delete_service(db, service_id=service_id)
        return None  # ✅ Changed: None for 204 (no body)
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")