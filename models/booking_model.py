# models/booking_model.py (actualiza el model con extend_existing=True)
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from core.database import Base  # Asume que Base está en core.database

class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = {'extend_existing': True}  # Fix para redefiniciones

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    check_in = Column(DateTime)
    check_out = Column(DateTime)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    total_price = Column(Float)
    status = Column(String, default="pending")  # e.g., "pending", "confirmed", "cancelled"

    # Relaciones
    owner = relationship("User", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")