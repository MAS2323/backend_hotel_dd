# models/testimonial_model.py
from sqlalchemy import Column, Integer, Text, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class Testimonial(Base):
    __tablename__ = "testimonials"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    author = Column(String(100))  # Column para nombre del autor (no relationship)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship - back_populates coincide con el field en User ("testimonials")
    user = relationship("User", back_populates="testimonials")  # Fix: relationship "user", back_populates="testimonials"