# models/apartment_model.py (corregido con import de DateTime)
from sqlalchemy import Column, Integer, String, Boolean, Float, Text, JSON, DateTime  # ✅ Agregado DateTime
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class Apartment(Base):
    __tablename__ = "apartments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # Nombre del apartamento
    description = Column(Text, nullable=False)  # Descripción detallada
    head = Column(String(100), nullable=False)  # Jefe o responsable
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    capacity = Column(Integer, nullable=False, default=2)  # Capacidad de huéspedes
    price_per_night = Column(Float, nullable=False, default=0.0)  # Precio por noche
    amenities = Column(JSON, nullable=True)  # Amenidades como JSON: ["wifi", "cocina", "balcon"]
    num_bedrooms = Column(Integer, nullable=False, default=1)  # Número de habitaciones
    num_bathrooms = Column(Integer, nullable=False, default=1)  # Número de baños
    square_meters = Column(Float, nullable=True)  # Metros cuadrados
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación con imágenes
    images = relationship("ApartmentImage", back_populates="apartment", cascade="all, delete-orphan")