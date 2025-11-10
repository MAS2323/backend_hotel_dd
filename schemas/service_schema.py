# schemas/service_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ServiceBase(BaseModel):
    title: str
    desc: str

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    desc: Optional[str] = None

class Service(ServiceBase):
    id: int
    icon_url: str
    icon_public_id: str  # ✅ Añadir esto
    created_at: datetime

    class Config:
        from_attributes = True