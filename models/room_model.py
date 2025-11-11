from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    size = Column(Float, nullable=False)  # Nuevo: tamaño en m²
    max_guests = Column(Integer, nullable=False, default=2)  # Nuevo: máx. huéspedes
    bed_type = Column(String(50), nullable=False)  # Nuevo: e.g., "doble", "twin"
    has_balcony = Column(Boolean, default=False)  # Nuevo: con balcón
    has_tv = Column(Boolean, default=True)  # Nuevo: con TV
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)  # Ya existía

    # Relación con imágenes
    images = relationship("RoomImage", back_populates="room", cascade="all, delete-orphan")