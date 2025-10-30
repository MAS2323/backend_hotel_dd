from sqlalchemy.orm import Session
from fastapi import UploadFile, File
from models.image_model import Image
from schemas.image_schema import ImageCreate, ImageUpdate
from core.cloudinary_config import upload_image
import cloudinary.uploader

def create_image(db: Session, image_data: ImageCreate, file: UploadFile = File(...)):
    # Subir a Cloudinary
    result = cloudinary.uploader.upload(
        file.file, folder="hotel_dd/gallery", resource_type="image", format="auto"
    )
    url = result['secure_url']
    public_id = result['public_id']
    
    # Check for duplicate URL
    if db.query(Image).filter(Image.url == url).first():
        raise ValueError("URL already exists")
    
    # Crear registro en DB
    db_image = Image(url=url, public_id=public_id, **image_data.dict(exclude={"file"}))
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def get_images(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Image).offset(skip).limit(limit).all()

def update_image(db: Session, image_id: int, image_update: ImageUpdate, file: UploadFile = None):
    db_image = db.query(Image).filter(Image.id == image_id).first()
    if not db_image:
        raise ValueError("Image not found")
    
    # Actualizar metadata (siempre)
    update_data = image_data.dict(exclude_unset=True, exclude={"file"})
    for field, value in update_data.items():
        setattr(db_image, field, value)
    
    # Si hay nuevo file, re-upload y actualizar URL/public_id
    if file:
        # Opcional: Eliminar viejo de Cloudinary
        cloudinary.uploader.destroy(db_image.public_id)
        
        # Subir nuevo
        result = cloudinary.uploader.upload(
            file.file, folder="hotel_dd/gallery", resource_type="image", format="auto"
        )
        new_url = result['secure_url']
        new_public_id = result['public_id']
        
        # Check for duplicate new URL (excluding current)
        if db.query(Image).filter(Image.id != image_id).filter(Image.url == new_url).first():
            raise ValueError("New URL already exists")
        
        # Actualizar
        db_image.url = new_url
        db_image.public_id = new_public_id
    
    db.commit()
    db.refresh(db_image)
    return db_image

def delete_image(db: Session, image_id: int):
    db_image = db.query(Image).filter(Image.id == image_id).first()
    if not db_image:
        raise ValueError("Image not found")
    
    # Eliminar de Cloudinary
    cloudinary.uploader.destroy(db_image.public_id)
    
    # Eliminar de DB
    db.delete(db_image)
    db.commit()
    return {"message": "Image deleted successfully"}