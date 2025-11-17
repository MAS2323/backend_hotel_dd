# controllers/apartment_controller.py (corregido: import Apartment en lugar de Department)
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from typing import Optional, List
from models.apartment_model import Apartment  # ✅ Corregido: import Apartment, no Department
from models.apartment_image_model import ApartmentImage
from schemas.apartment_schema import ApartmentCreate, ApartmentBase, ApartmentImageCreate, ApartmentUpdate
from core.cloudinary_config import upload_image
import cloudinary.uploader
import logging

logger = logging.getLogger(__name__)

def create_apartment(db: Session, apartment: ApartmentCreate, files: List[UploadFile] = None, image_data_list: List[ApartmentImageCreate] = None):
    db_apartment = Apartment(**apartment.dict(exclude={"images"}))
    db.add(db_apartment)
    db.commit()
    db.refresh(db_apartment)
    
    if files and image_data_list:
        for file, img_data in zip(files, image_data_list):
            result = cloudinary.uploader.upload(
                file.file,
                folder="hotel_dd/apartments",
                resource_type="image"
            )
            db_image = ApartmentImage(
                url=result['secure_url'],
                public_id=result['public_id'],
                alt=img_data.alt,
                apartment_id=db_apartment.id  # ✅ Corregido: apartment_id
            )
            db.add(db_image)
        db.commit()
    
    return db_apartment

def get_apartments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Apartment).offset(skip).limit(limit).all()

def get_apartment(db: Session, apartment_id: int):
    return db.query(Apartment).filter(Apartment.id == apartment_id).first()

def update_apartment(
    db: Session, 
    apartment_id: int, 
    apartment_update: ApartmentUpdate, 
    files: Optional[List[UploadFile]] = None, 
    image_data_list: Optional[List[ApartmentImageCreate]] = None
) -> Optional[Apartment]:
    try:
        db_apartment = db.query(Apartment).filter(Apartment.id == apartment_id).first()
        if not db_apartment:
            logger.warning(f"Apartamento {apartment_id} no encontrado")
            return None
        
        update_data = apartment_update.model_dump(exclude_none=True)
        
        if update_data:
            for key, value in update_data.items():
                setattr(db_apartment, key, value)
        
        # Manejo de imágenes (sin cambios)
        if files and image_data_list:
            if len(files) != len(image_data_list):
                raise HTTPException(status_code=400, detail="Número de archivos no coincide con metadatos")
            
            for file, img_data in zip(files, image_data_list):
                if not file or not file.file:
                    continue
                
                result = cloudinary.uploader.upload(
                    file.file, 
                    folder="hotel_dd/apartments", 
                    resource_type="image", 
                    format="auto"
                )
                
                db_image = ApartmentImage(
                    url=result['secure_url'], 
                    public_id=result['public_id'], 
                    alt=img_data.alt or f"Apartamento {apartment_id}", 
                    apartment_id=apartment_id
                )
                db.add(db_image)
        
        db.commit()
        db.refresh(db_apartment)
        logger.info(f"Apartamento {apartment_id} actualizado exitosamente")
        return db_apartment
        
    except Exception as e:
        logger.error(f"Error actualizando apartamento {apartment_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar: {str(e)}")

def delete_apartment(db: Session, apartment_id: int):
    db_apartment = db.query(Apartment).filter(Apartment.id == apartment_id).first()
    if db_apartment:
        # Delete associated images from Cloudinary/DB
        for img in db_apartment.images:
            cloudinary.uploader.destroy(img.public_id)
            db.delete(img)
        db.delete(db_apartment)
        db.commit()
    return db_apartment