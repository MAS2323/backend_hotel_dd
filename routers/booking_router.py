# routers/booking_router.py (actualizado: agrega PUT /{id} y DELETE /{id})
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.booking_schema import Booking, BookingCreate, BookingUpdate
from controllers.booking_controller import create_booking, get_bookings, update_booking, delete_booking

booking_router = APIRouter(prefix="/bookings", tags=["bookings"])

@booking_router.post("/", response_model=Booking, status_code=201)
def create_booking_endpoint(booking: BookingCreate, db: Session = Depends(get_db)):
    return create_booking(db, booking)

@booking_router.get("/", response_model=List[Booking])
def read_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_bookings(db, skip, limit)

@booking_router.put("/{booking_id}", response_model=Booking)
def update_booking_endpoint(booking_id: int, booking: BookingUpdate, db: Session = Depends(get_db)):
    return update_booking(db, booking_id, booking)

@booking_router.delete("/{booking_id}", status_code=204)
def delete_booking_endpoint(booking_id: int, db: Session = Depends(get_db)):
    delete_booking(db, booking_id)
    return None  # No content for DELETE