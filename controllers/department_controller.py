from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from typing import Optional, List
from models.department_model import Department
from models.department_image_model import DepartmentImage
from schemas.department_schema import DepartmentCreate, DepartmentBase, DepartmentImageCreate, DepartmentUpdate
from core.cloudinary_config import upload_image
import cloudinary.uploader
import logging

logger = logging.getLogger(__name__)

def create_department(db: Session, department: DepartmentCreate, files: List[UploadFile] = None, image_data_list: List[DepartmentImageCreate] = None):
    db_department = Department(**department.dict(exclude={"images"}))
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    
    if files and image_data_list:
        for file, img_data in zip(files, image_data_list):
            result = cloudinary.uploader.upload(
                file.file,
                folder="hotel_dd/departments",
                resource_type="image"
            )
            db_image = DepartmentImage(
                url=result['secure_url'],
                public_id=result['public_id'],
                alt=img_data.alt,
                department_id=db_department.id
            )
            db.add(db_image)
        db.commit()
    
    return db_department

def get_departments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Department).offset(skip).limit(limit).all()

def get_department(db: Session, department_id: int):
    return db.query(Department).filter(Department.id == department_id).first()

def update_department(
    db: Session, 
    department_id: int, 
    department_update: DepartmentUpdate, 
    files: Optional[List[UploadFile]] = None, 
    image_data_list: Optional[List[DepartmentImageCreate]] = None
) -> Optional[Department]:
    try:
        db_department = db.query(Department).filter(Department.id == department_id).first()
        if not db_department:
            logger.warning(f"Departamento {department_id} no encontrado")
            return None
        
        update_data = department_update.model_dump(exclude_none=True)
        
        if update_data:
            for key, value in update_data.items():
                setattr(db_department, key, value)
        
        # Manejo de imágenes (sin cambios)
        if files and image_data_list:
            if len(files) != len(image_data_list):
                raise HTTPException(status_code=400, detail="Número de archivos no coincide con metadatos")
            
            for file, img_data in zip(files, image_data_list):
                if not file or not file.file:
                    continue
                
                result = cloudinary.uploader.upload(
                    file.file, 
                    folder="hotel_dd/departments", 
                    resource_type="image", 
                    format="auto"
                )
                
                db_image = DepartmentImage(
                    url=result['secure_url'], 
                    public_id=result['public_id'], 
                    alt=img_data.alt or f"Departamento {department_id}", 
                    department_id=department_id
                )
                db.add(db_image)
        
        db.commit()
        db.refresh(db_department)
        logger.info(f"Departamento {department_id} actualizado exitosamente")
        return db_department
        
    except Exception as e:
        logger.error(f"Error actualizando departamento {department_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar: {str(e)}")

def delete_department(db: Session, department_id: int):
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if db_department:
        # Delete associated images from Cloudinary/DB
        for img in db_department.images:
            cloudinary.uploader.destroy(img.public_id)
            db.delete(img)
        db.delete(db_department)
        db.commit()
    return db_department