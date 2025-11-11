from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from typing import Optional
from models.image_model import Image
from schemas.image_schema import ImageCreate, ImageUpdate
from core.cloudinary_config import upload_image
import logging
from cloudinary.uploader import destroy

logger = logging.getLogger(__name__)

def create_image(db: Session, image_data: ImageCreate, file: UploadFile):  # Single
    try:
        if not file.filename:
            raise ValueError("Archivo requerido")

        logger.info(f"Creating image: {image_data.alt} in category {image_data.category}")
        folder = f"hotel_dd/{image_data.category}"
        url, public_id = upload_image(file.file, folder=folder)

        if db.query(Image).filter(Image.url == url).first():
            raise ValueError("URL ya existe")

        db_image = Image(
            url=url,
            public_id=public_id,
            alt=image_data.alt,
            desc=image_data.desc,
            category=image_data.category
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        logger.info(f"✅ Created image ID {db_image.id} in {image_data.category}")
        return db_image
    except ValueError as e:
        if db.is_active:
            db.rollback()
        raise e
    except Exception as e:
        if db.is_active:
            db.rollback()
        logger.error(f"Create error: {e}")
        raise HTTPException(500, detail="Failed to create image")

def get_images(db: Session, skip: int = 0, limit: int = 100, category: Optional[str] = None):
    try:
        query = db.query(Image)
        if category:
            query = query.filter(Image.category == category)
        images = query.offset(skip).limit(limit).all()
        logger.info(f"Fetched {len(images)} images {'in ' + category if category else 'all categories'}")
        return images
    except Exception as e:
        logger.error(f"Fetch error: {e}")
        raise HTTPException(500, detail="Failed to fetch images")

def update_image(db: Session, image_id: int, image_update: ImageUpdate, file: Optional[UploadFile] = None):
    try:
        db_image = db.query(Image).filter(Image.id == image_id).first()
        if not db_image:
            raise ValueError("Image not found")

        updated = False
        if image_update.alt is not None:
            db_image.alt = image_update.alt
            updated = True
        if image_update.desc is not None:
            db_image.desc = image_update.desc
            updated = True
        if image_update.category is not None:
            db_image.category = image_update.category
            updated = True

        if file and file.filename:
            # Delete old
            try:
                destroy(db_image.public_id, resource_type="image")
                logger.info("Deleted old image")
            except Exception as e:
                logger.warning(f"Delete old failed: {e}")

            # Upload new con nueva carpeta si category cambió
            folder = f"hotel_dd/{db_image.category}"  # Usa la category actualizada
            new_url, new_public_id = upload_image(file.file, folder=folder)
            if db.query(Image).filter(Image.id != image_id, Image.url == new_url).first():
                raise ValueError("New URL already exists")

            db_image.url = new_url
            db_image.public_id = new_public_id
            updated = True

        if not updated:
            return db_image

        db.commit()
        db.refresh(db_image)
        logger.info(f"✅ Updated image {image_id}")
        return db_image
    except ValueError as e:
        if db.is_active:
            db.rollback()
        raise e
    except Exception as e:
        if db.is_active:
            db.rollback()
        logger.error(f"Update error: {e}")
        raise HTTPException(500, detail="Failed to update image")

def delete_image(db: Session, image_id: int):
    try:
        db_image = db.query(Image).filter(Image.id == image_id).first()
        if not db_image:
            raise ValueError("Image not found")

        destroy(db_image.public_id, resource_type="image")
        logger.info("Deleted from Cloudinary")

        db.delete(db_image)
        db.commit()
        logger.info(f"✅ Deleted image {image_id}")
    except ValueError as e:
        raise e
    except Exception as e:
        if db.is_active:
            db.rollback()
        logger.error(f"Delete error: {e}")
        raise HTTPException(500, detail="Failed to delete image")