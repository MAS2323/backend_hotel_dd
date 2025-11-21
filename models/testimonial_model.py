# models/testimonial_model.py (sin cambios, pero confirmando content)
from sqlalchemy import Column, Integer, Text, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class Testimonial(Base):
    __tablename__ = "testimonials"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    author = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Opcional si anonimo
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="testimonials")