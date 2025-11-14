from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    size = Column(Float, nullable=False)
    max_guests = Column(Integer, nullable=False, default=2)
    bed_type = Column(String(50), nullable=False)
    has_balcony = Column(Boolean, default=False)
    has_tv = Column(Boolean, default=True)
    amenities = Column(JSON, default=dict, nullable=True)  # { "5": true, ... }
    is_featured = Column(Boolean, default=False)  # ← NUEVO: Habitación Destacada
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    images = relationship("RoomImage", back_populates="room", cascade="all, delete-orphan")