from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class RoomImage(Base):
    __tablename__ = "room_images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), nullable=False)
    public_id = Column(String(255), nullable=False)
    alt = Column(String(255), nullable=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))

    # ✅ RELACIÓN INVERSA OBLIGATORIA
    room = relationship("Room", back_populates="images")