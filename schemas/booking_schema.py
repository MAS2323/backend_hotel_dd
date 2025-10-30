from pydantic import BaseModel
from datetime import date
from typing import Optional

class BookingBase(BaseModel):
    name: str
    email: str
    check_in: date
    check_out: date
    room_type: str

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    user_id: Optional[int] = None

    class Config:
        from_attributes = True