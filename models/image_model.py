# models/image_model.py (fixed with prefix index)
from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import relationship
from sqlalchemy import func  # For substring
from core.database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(1000), index=False)  # No auto-index; use custom below
    public_id = Column(String(500), unique=True, index=True)  # Unique on public_id (shorter, safe)
    alt = Column(String(255), index=True)
    desc = Column(String(255), index=True)

    # Prefix index for url (first 255 chars for uniqueness/search; full URL stored)
    __table_args__ = (
        Index('ix_images_url_prefix', func.substring(url, 1, 255), unique=True),
    )