from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from typing import Optional, List
from models.room_model import Room
from models.room_image_model import RoomImage
from schemas.room_schema import RoomCreate, RoomBase, RoomImageCreate, RoomUpdate
from core.cloudinary_config import upload_image
import cloudinary.uploader
import logging

logger = logging.getLogger(__name__)
def create_room(db: Session, room: RoomCreate, files: List[UploadFile] = None, image_data_list: List[RoomImageCreate] = None):
    db_room = Room(**room.dict(exclude={"images"}))
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    
    if files and image_data_list:
        for file, img_data in zip(files, image_data_list):
            result = cloudinary.uploader.upload(
                file.file,
                folder="hotel_dd/rooms",
                resource_type="image"
            )
            db_image = RoomImage(
                url=result['secure_url'],
                public_id=result['public_id'],
                alt=img_data.alt,
                room_id=db_room.id
            )
            db.add(db_image)
        db.commit()
    
    return db_room
def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Room).offset(skip).limit(limit).all()

def get_room(db: Session, room_id: int):
    return db.query(Room).filter(Room.id == room_id).first()

def update_room(
    db: Session, 
    room_id: int, 
    room_update: RoomUpdate, 
    files: Optional[List[UploadFile]] = None, 
    image_data_list: Optional[List[RoomImageCreate]] = None
) -> Optional[Room]:
    """
    Actualiza una habitación y opcionalmente sus imágenes.
    Solo actualiza los campos que no sean None.
    """
    try:
        # Buscar habitación
        db_room = db.query(Room).filter(Room.id == room_id).first()
        if not db_room:
            logger.warning(f"Habitación {room_id} no encontrada")
            return None
        
        # ✅ SOLO actualizar campos con valores nuevos
        update_data = room_update.model_dump(exclude_none=True)
        
        if not update_data:
            logger.info(f"No hay cambios para aplicar en habitación {room_id}")
        else:
            logger.info(f"Actualizando habitación {room_id}: {update_data}")
            for key, value in update_data.items():
                setattr(db_room, key, value)
        
        # Manejo de imágenes (opcional)
        if files and image_data_list:
            # Validar que coincidan las cantidades
            if len(files) != len(image_data_list):
                raise HTTPException(
                    status_code=400, 
                    detail="Número de archivos no coincide con metadatos"
                )
            
            # Eliminar imágenes antiguas (descomentar si quieres reemplazar)
            # for old_img in db_room.images:
            #     cloudinary.uploader.destroy(old_img.public_id)
            #     db.delete(old_img)
            
            # Subir nuevas imágenes
            for file, img_data in zip(files, image_data_list):
                if not file or not file.file:
                    continue
                
                result = cloudinary.uploader.upload(
                    file.file, 
                    folder="hotel_dd/rooms", 
                    resource_type="image", 
                    format="auto"
                )
                
                db_image = RoomImage(
                    url=result['secure_url'], 
                    public_id=result['public_id'], 
                    alt=img_data.alt or f"Habitación {room_id}", 
                    room_id=room_id
                )
                db.add(db_image)
        
        # Commit único
        db.commit()
        db.refresh(db_room)
        logger.info(f"Habitación {room_id} actualizada exitosamente")
        return db_room
        
    except Exception as e:
        logger.error(f"Error actualizando habitación {room_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar: {str(e)}")

def delete_room(db: Session, room_id: int):
    db_room = db.query(Room).filter(Room.id == room_id).first()
    if db_room:
        # Delete associated images from Cloudinary/DB
        for img in db_room.images:
            cloudinary.uploader.destroy(img.public_id)
            db.delete(img)
        db.delete(db_room)
        db.commit()
    return db_room