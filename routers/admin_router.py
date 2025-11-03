# routers/admin_router.py
from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from core.security import get_current_user
from schemas.user_schema import User
from controllers.user_controller import update_user_role
from schemas.service_schema import Service, ServiceCreate, ServiceUpdate
from controllers.service_controller import create_service, get_services, update_service, delete_service

admin_router = APIRouter(prefix="/admin", tags=["admin"])

# Admin dependency
def require_admin(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@admin_router.get("/users", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    return db.query(User).offset(skip).limit(limit).all()

@admin_router.put("/users/{user_id}/role", response_model=User)
def update_role_endpoint(user_id: int, role: str, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    return update_user_role(db, user_id, role)

@admin_router.post("/services", response_model=Service, status_code=201)
def create_service_endpoint(
    title: str = Form(...),
    desc: str = Form(...),
    icon_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    service_data = ServiceCreate(title=title, desc=desc)
    return create_service(db, service_data, icon_file)

@admin_router.get("/services", response_model=List[Service])
def read_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_services(db, skip, limit)

@admin_router.put("/services/{service_id}", response_model=Service)
def update_service_endpoint(
    service_id: int,
    title: Optional[str] = Form(None),
    desc: Optional[str] = Form(None),
    icon_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    service_update = ServiceUpdate(title=title, desc=desc)
    return update_service(db, service_id, service_update, icon_file)

@admin_router.delete("/services/{service_id}", status_code=204)
def delete_service_endpoint(service_id: int, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    delete_service(db, service_id)
    return {"message": "Deleted"}