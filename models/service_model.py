# models/service_model.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from core.database import Base

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    desc = Column(String(500), nullable=False)
    icon_url = Column(String(500), nullable=False)
    icon_public_id = Column(String(255), nullable=False)  # ✅ NUEVO CAMPO
    created_at = Column(DateTime(timezone=True), server_default=func.now())