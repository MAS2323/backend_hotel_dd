from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class RoomImageBase(BaseModel):
    url: str
    public_id: str
    alt: Optional[str] = None

class RoomImageCreate(BaseModel):
    alt: Optional[str] = None  # File handled in router

class RoomImage(RoomImageBase):
    id: int

    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: Optional[bool] = True

class RoomCreate(RoomBase):
    images: Optional[List[RoomImageCreate]] = None  # For initial images

class RoomUpdate(RoomBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None
    images: Optional[List[RoomImageCreate]] = None  # For adding/updating images

class Room(RoomBase):
    id: int
    created_at: datetime  # ← campo obligatorio
    images: List[RoomImage] = []

    class Config:
        from_attributes = True