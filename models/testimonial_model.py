from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Testimonial(Base):
    __tablename__ = "testimonials"

    id = Column(Integer, primary_key=True, index=True)
    quote = Column(String(500), index=True)  # <-- Added length for quote
    author = Column(String(100), index=True)  # <-- Added length for author
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="testimonials")