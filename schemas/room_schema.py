from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict
import json  # ← Para parsear en endpoints si es necesario

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
    size: float
    max_guests: int
    bed_type: str
    has_balcony: bool = False
    has_tv: bool = True
    amenities: Optional[Dict[str, bool]] = None
    is_featured: bool = False  # ← NUEVO
    is_available: bool = True

class RoomCreate(RoomBase):
    images: Optional[List[RoomImageCreate]] = None

class RoomUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    size: Optional[float] = None
    max_guests: Optional[int] = None
    bed_type: Optional[str] = None
    has_balcony: Optional[bool] = None
    has_tv: Optional[bool] = None
    amenities: Optional[Dict[str, bool]] = None
    is_featured: Optional[bool] = None  # ← NUEVO
    is_available: Optional[bool] = None
    images: Optional[List[RoomImageCreate]] = None

class Room(RoomBase):
    id: int
    created_at: datetime
    images: List[RoomImage] = []

    class Config:
        from_attributes = True 