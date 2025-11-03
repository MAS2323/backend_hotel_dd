# models/booking_model.py (corregido con longitudes explícitas para MySQL)
from sqlalchemy import Column, Integer, DateTime, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    check_in = Column(DateTime)
    check_out = Column(DateTime)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    total_price = Column(Float)
    status = Column(String(20), default="pending")  # Fix: Especifica longitud para VARCHAR en MySQL

    # Relationships
    owner = relationship("User", back_populates="bookings")