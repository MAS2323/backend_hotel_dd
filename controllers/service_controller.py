from sqlalchemy.orm import Session
from fastapi import UploadFile, File
from models.service_model import Service
from schemas.service_schema import ServiceCreate, ServiceUpdate
from core.cloudinary_config import upload_image
import cloudinary.uploader

def create_service(db: Session, service_data: ServiceCreate, file: UploadFile = File(...)):
    result = cloudinary.uploader.upload(
        file.file, folder="hotel_dd/services", resource_type="image", format="auto"
    )
    icon_url = result['secure_url']
    if db.query(Service).filter(Service.icon_url == icon_url).first():
        raise ValueError("Icon URL already exists")
    db_service = Service(icon_url=icon_url, **service_data.dict(exclude={"icon_file"}))
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def get_services(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Service).offset(skip).limit(limit).all()

def update_service(db: Session, service_id: int, service_update: ServiceUpdate, file: UploadFile = None):
    db_service = db.query(Service).filter(Service.id == service_id).first()
    if not db_service:
        raise ValueError("Service not found")
    
    update_data = service_update.dict(exclude_unset=True, exclude={"icon_file"})
    for field, value in update_data.items():
        setattr(db_service, field, value)
    
    if file:
        cloudinary.uploader.destroy(db_service.icon_url.split('/')[-1].split('.')[0])  # Extract public_id if needed
        result = cloudinary.uploader.upload(file.file, folder="hotel_dd/services", resource_type="image", format="auto")
        db_service.icon_url = result['secure_url']
    
    db.commit()
    db.refresh(db_service)
    return db_service

def delete_service(db: Session, service_id: int):
    db_service = db.query(Service).filter(Service.id == service_id).first()
    if not db_service:
        raise ValueError("Service not found")
    
    # Delete from Cloudinary (extract public_id from URL)
    public_id = db_service.icon_url.split('/')[-1].split('.')[0]  # Simple extract; use full if saved
    cloudinary.uploader.destroy(public_id)
    
    db.delete(db_service)
    db.commit()
    return {"message": "Service deleted"}