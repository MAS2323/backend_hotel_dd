from sqlalchemy.orm import Session
from fastapi import UploadFile
from typing import Optional, List
from models.room_model import Room
from models.room_image_model import RoomImage
from schemas.room_schema import RoomCreate, RoomBase, RoomImageCreate
from core.cloudinary_config import upload_image
import cloudinary.uploader

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

def update_room(db: Session, room_id: int, room_update: RoomBase, files: List[UploadFile] = None, image_data_list: List[RoomImageCreate] = None):
    db_room = db.query(Room).filter(Room.id == room_id).first()
    if not db_room:
        return None
    
    # Update room fields
    for key, value in room_update.dict(exclude_unset=True).items():
        setattr(db_room, key, value)
    
    # Handle image updates/adds (delete old if needed, add new)
    if files and image_data_list:
        # Optional: Delete old images (loop and destroy)
        for old_img in db_room.images:
            cloudinary.uploader.destroy(old_img.public_id)
            db.delete(old_img)
        
        for file, img_data in zip(files, image_data_list):
            result = cloudinary.uploader.upload(
                file.file, folder="hotel_dd/rooms", resource_type="image", format="auto"
            )
            url = result['secure_url']
            public_id = result['public_id']
            
            db_image = RoomImage(
                url=url, 
                public_id=public_id, 
                alt=img_data.alt, 
                room_id=room_id
            )
            db.add(db_image)
        db.commit()
    
    db.commit()
    db.refresh(db_room)
    return db_room

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