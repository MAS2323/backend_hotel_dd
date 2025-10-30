# schemas/service_schema.py
from pydantic import BaseModel
from typing import Optional

class ServiceBase(BaseModel):
    title: str
    desc: str

class ServiceCreate(ServiceBase):
    pass  # icon_file handled in router as UploadFile

class ServiceUpdate(ServiceBase):
    pass

class Service(ServiceBase):
    id: int
    icon_url: str  # URL from Cloudinary

    class Config:
        from_attributes = True