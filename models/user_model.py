# models/user_model.py (tu código actualizado: confirma back_populates="owner" para consistencia)
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base
from typing import List  # Para typing en relationships si es necesario

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships: back_populates coincide con el en Booking ("owner")
    bookings = relationship("Booking", back_populates="owner")
    testimonials = relationship("Testimonial", back_populates="user")  # Como indicaste en el comentario