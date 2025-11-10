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

class Service(ServiceBase):  # ✅ Changed: Inherit from ServiceBase for title/desc
    id: int
    icon_url: str
    icon_public_id: str
    created_at: Optional[datetime] = None  # ✅ Made Optional to match model (nullable)

    class Config:
        from_attributes = True  # Good for v2