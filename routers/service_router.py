# routers/service_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.service_schema import Service
from controllers.service_controller import get_services

service_router = APIRouter(prefix="/services", tags=["services"])  # Public prefix

@service_router.get("/", response_model=List[Service])
def read_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_services(db, skip, limit)