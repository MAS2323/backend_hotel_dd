from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class RoomImageBase(BaseModel):
    url: str
    public_id: str
    alt: Optional[str] = None

class RoomImageCreate(BaseModel):
    alt: Optional[str] = None

class RoomImage(RoomImageBase):
    id: int

    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    size: float  # Nuevo
    max_guests: int  # Nuevo
    bed_type: str  # Nuevo
    has_balcony: bool = False  # Nuevo
    has_tv: bool = True  # Nuevo
    is_available: bool = True

class RoomCreate(RoomBase):
    images: Optional[List[RoomImageCreate]] = None

class RoomUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    size: Optional[float] = None  # Nuevo
    max_guests: Optional[int] = None  # Nuevo
    bed_type: Optional[str] = None  # Nuevo
    has_balcony: Optional[bool] = None  # Nuevo
    has_tv: Optional[bool] = None  # Nuevo
    is_available: Optional[bool] = None
    images: Optional[List[RoomImageCreate]] = None

class Room(RoomBase):
    id: int
    created_at: datetime
    images: List[RoomImage] = []

    class Config:
        from_attributes = True