# schemas/apartment_schema.py (corregido: sin import circular, solo imports necesarios)
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from models.apartment_model import Apartment  # Import desde models, NO desde schemas

class ApartmentImageBase(BaseModel):
    url: str
    public_id: str
    alt: Optional[str] = None

class ApartmentImageCreate(BaseModel):
    alt: Optional[str] = None

class ApartmentImage(ApartmentImageBase):
    id: int

    class Config:
        from_attributes = True

class ApartmentBase(BaseModel):
    name: str
    description: str
    head: str  # Jefe del apartamento/departamento
    email: str
    phone: str
    capacity: int = 2
    price_per_night: float = 0.0
    amenities: Optional[List[str]] = None
    num_bedrooms: int = 1
    num_bathrooms: int = 1
    square_meters: Optional[float] = None
    is_active: bool = True

class ApartmentCreate(ApartmentBase):
    images: Optional[List[ApartmentImageCreate]] = None

class ApartmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    head: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    capacity: Optional[int] = None
    price_per_night: Optional[float] = None
    amenities: Optional[List[str]] = None
    num_bedrooms: Optional[int] = None
    num_bathrooms: Optional[int] = None
    square_meters: Optional[float] = None
    is_active: Optional[bool] = None
    images: Optional[List[ApartmentImageCreate]] = None

class Apartment(ApartmentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    images: List[ApartmentImage] = []

    class Config:
        from_attributes = True