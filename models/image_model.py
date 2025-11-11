# models/image_model.py
from sqlalchemy import Column, Integer, String, Index, func
from core.database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), nullable=False)
    public_id = Column(String(255), nullable=False)
    alt = Column(String(255), nullable=True)
    desc = Column(String(255), nullable=True)
    category = Column(String(50), nullable=False, default="galeria")

    __table_args__ = (
        Index('ix_images_url_prefix', func.substring(url, 1, 255), unique=True),
    )