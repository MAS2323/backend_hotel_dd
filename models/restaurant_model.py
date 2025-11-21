# models/restaurant_model.py (actualizado: agrega image_public_id a MenuItem)
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
from typing import List

class Restaurant(Base):
    __tablename__ = "restaurants"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=False)
    image_url = Column(String(500), nullable=False)
    image_public_id = Column(String(255), nullable=False)  # ← NUEVO: para imagen del restaurante
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    menu_items = relationship("MenuItem", back_populates="restaurant")

class MenuItem(Base):
    __tablename__ = "menu_items"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(300), nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    image_url = Column(String(500), nullable=True)
    image_public_id = Column(String(255), nullable=True)  # ← NUEVO: para imagen del ítem
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    restaurant = relationship("Restaurant", back_populates="menu_items")