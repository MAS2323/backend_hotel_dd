from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class RoomImage(Base):
    __tablename__ = "room_images"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(1000), index=False)  # Cloudinary URL
    public_id = Column(String(500), unique=True, index=True)  # For delete
    alt = Column(String(255), index=True)  # Optional alt text
    room_id = Column(Integer, ForeignKey("rooms.id"))
    
    # Relationship back to Room
    room = relationship("Room", back_populates="images")