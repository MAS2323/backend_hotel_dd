from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.booking_schema import Booking, BookingCreate
from controllers.booking_controller import create_booking, get_bookings

booking_router = APIRouter(prefix="/bookings", tags=["bookings"])

@booking_router.post("/", response_model=Booking, status_code=201)
def create_booking_endpoint(booking: BookingCreate, db: Session = Depends(get_db)):
    return create_booking(db, booking)

@booking_router.get("/", response_model=List[Booking])
def read_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_bookings(db, skip, limit)