# controllers/booking_controller.py (actualizado: agrega update_booking y delete_booking)
from sqlalchemy.orm import Session
from sqlalchemy import update
from models.booking_model import Booking
from schemas.booking_schema import BookingCreate, BookingUpdate
from models.room_model import Room  # Asume import de Room model
from models.apartment_model import Apartment  # Asume import de Apartment model
from datetime import datetime
from fastapi import HTTPException

def create_booking(db: Session, booking: BookingCreate):
    # Obtener precio basado en type e id
    if booking.accommodation_type == 'room':
        acc = db.query(Room).filter(Room.id == booking.accommodation_id).first()
        price_per_night = acc.price if acc else 0
    elif booking.accommodation_type == 'apartment':
        acc = db.query(Apartment).filter(Apartment.id == booking.accommodation_id).first()
        price_per_night = acc.price_per_night if acc else 0
    else:
        raise ValueError("Tipo de alojamiento inválido")

    # Calcular noches y total
    check_in_dt = datetime.combine(booking.check_in, datetime.min.time())
    check_out_dt = datetime.combine(booking.check_out, datetime.min.time())
    nights = (check_out_dt - check_in_dt).days
    total_price = nights * price_per_night if nights > 0 else 0

    # Crear booking con campos ajustados (agrega guest_name, etc., user_id=None para guests)
    db_booking = Booking(
        guest_name=booking.guest_name,
        guest_email=booking.guest_email,
        phone=booking.phone,
        check_in=check_in_dt,
        check_out=check_out_dt,
        accommodation_type=booking.accommodation_type,
        accommodation_id=booking.accommodation_id,
        total_price=total_price,
        status="pending",
        user_id=None  # Para guests anónimos
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    # Opcional: join para obtener nombres de accommodations
    return db.query(Booking).offset(skip).limit(limit).all()

def update_booking(db: Session, booking_id: int, booking_update: BookingUpdate):
    db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    update_data = booking_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == 'check_in' or field == 'check_out':
            setattr(db_booking, field, datetime.combine(value, datetime.min.time()))
        else:
            setattr(db_booking, field, value)
    
    # Recalcular total si cambian fechas o accommodation
    if 'check_in' in update_data or 'check_out' in update_data or 'accommodation_type' in update_data or 'accommodation_id' in update_data:
        if db_booking.accommodation_type == 'room':
            acc = db.query(Room).filter(Room.id == db_booking.accommodation_id).first()
            price_per_night = acc.price if acc else 0
        elif db_booking.accommodation_type == 'apartment':
            acc = db.query(Apartment).filter(Apartment.id == db_booking.accommodation_id).first()
            price_per_night = acc.price_per_night if acc else 0
        else:
            price_per_night = 0
        nights = (db_booking.check_out - db_booking.check_in).days
        db_booking.total_price = nights * price_per_night
    
    db.commit()
    db.refresh(db_booking)
    return db_booking

def delete_booking(db: Session, booking_id: int):
    db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(db_booking)
    db.commit()
    return {"message": "Booking deleted successfully"}