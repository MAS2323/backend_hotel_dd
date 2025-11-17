# models/booking_model.py (corregido: FK explícito, nullable, y relationship consistente con User)
from sqlalchemy import Column, Integer, DateTime, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from typing import Optional

class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)  # FK explícito con ondelete para guests
    guest_name = Column(String(100), nullable=False)
    guest_email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)
    accommodation_type = Column(String(20), nullable=False)  # 'room' o 'apartment'
    accommodation_id = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String(20), default="pending")

    # Relationship consistente: back_populates="bookings" (nombre del atributo en User)
    owner = relationship("User", back_populates="bookings")
    # Opcional: relationships a Room/Apartment si quieres joins
    room = relationship("Room", foreign_keys=[accommodation_id], primaryjoin="and_(Booking.accommodation_type=='room', Booking.accommodation_id==Room.id)")
    apartment = relationship("Apartment", foreign_keys=[accommodation_id], primaryjoin="and_(Booking.accommodation_type=='apartment', Booking.accommodation_id==Apartment.id)")