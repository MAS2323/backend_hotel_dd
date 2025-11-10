# models/image_model.py
from sqlalchemy import Column, Integer, String, Index, func
from core.database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(1000), nullable=False, index=False)
    public_id = Column(String(500), unique=True, index=True)
    alt = Column(String(255), index=True)
    desc = Column(String(500), index=True)

    __table_args__ = (
        Index('ix_images_url_prefix', func.substring(url, 1, 255), unique=True),
    )