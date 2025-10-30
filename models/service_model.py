# models/service_model.py (fixed)
from sqlalchemy import Column, Integer, String, Index, func
from core.database import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    icon_url = Column(String(1000), index=False)  # No full index; use prefix below
    title = Column(String(255), index=True)
    desc = Column(String(500), index=True)

    # Prefix index for icon_url (first 255 chars for uniqueness/search)
    __table_args__ = (
        Index('ix_services_icon_url_prefix', func.substring(icon_url, 1, 255), unique=False),
    )