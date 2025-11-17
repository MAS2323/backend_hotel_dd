# schemas/booking_schema.py (actualizado: agrega BookingUpdate para partial updates)
from pydantic import BaseModel
from datetime import date
from typing import Optional

class BookingBase(BaseModel):
    guest_name: str
    guest_email: str
    phone: Optional[str] = None
    check_in: date
    check_out: date
    accommodation_type: str  # 'room' o 'apartment'
    accommodation_id: int

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    guest_name: Optional[str] = None
    guest_email: Optional[str] = None
    phone: Optional[str] = None
    check_in: Optional[date] = None
    check_out: Optional[date] = None
    accommodation_type: Optional[str] = None
    accommodation_id: Optional[int] = None
    total_price: Optional[float] = None
    status: Optional[str] = None

class Booking(BookingBase):
    id: int
    total_price: float
    status: str
    created_at: Optional[date] = None  # Si agregas timestamp en model

    class Config:
        from_attributes = True