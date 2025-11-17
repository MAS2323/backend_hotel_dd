# models/apartment_image_model.py (renombrado)
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class ApartmentImage(Base):
    __tablename__ = "apartment_images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), nullable=False)
    public_id = Column(String(255), nullable=False)
    alt = Column(String(255), nullable=True)
    apartment_id = Column(Integer, ForeignKey("apartments.id"))

    # Relación inversa obligatoria
    apartment = relationship("Apartment", back_populates="images")