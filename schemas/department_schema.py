from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class DepartmentImageBase(BaseModel):
    url: str
    public_id: str
    alt: Optional[str] = None

class DepartmentImageCreate(BaseModel):
    alt: Optional[str] = None

class DepartmentImage(DepartmentImageBase):
    id: int

    class Config:
        from_attributes = True

class DepartmentBase(BaseModel):
    name: str
    description: str
    head: str  # Jefe del departamento
    email: str
    phone: str
    is_active: bool = True

class DepartmentCreate(DepartmentBase):
    images: Optional[List[DepartmentImageCreate]] = None

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    head: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    images: Optional[List[DepartmentImageCreate]] = None

class Department(DepartmentBase):
    id: int
    created_at: datetime
    images: List[DepartmentImage] = []

    class Config:
        from_attributes = True