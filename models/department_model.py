from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class DepartmentImage(Base):
    __tablename__ = "department_images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), nullable=False)
    public_id = Column(String(255), nullable=False)
    alt = Column(String(255), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"))

    # ✅ RELACIÓN INVERSA OBLIGATORIA
    department = relationship("Department", back_populates="images")