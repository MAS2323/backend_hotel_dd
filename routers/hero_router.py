from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from core.database import get_db
from schemas.image_schema import Image, ImageCreate, ImageUpdate
from controllers.image_controller import create_image, get_images, update_image, delete_image
import logging

logger = logging.getLogger(__name__)

hero_router = APIRouter(prefix="/hero", tags=["hero"])

@hero_router.get("/", response_model=list[Image])
def read_hero(
    skip: int = 0, 
    limit: int = 100, 
    category: Optional[str] = Query("hero", regex="^(galeria|hero)$"),
    db: Session = Depends(get_db)
):
    logger.info(f"GET /hero (skip={skip}, limit={limit}, category={category})")
    return get_images(db, skip, limit, category)

@hero_router.post("/", response_model=Image, status_code=status.HTTP_201_CREATED)
def create_hero_endpoint(
    alt: str = Form(...),
    desc: str = Form(...),
    category: str = Form("hero"),  # Por defecto "hero"
    file: UploadFile = File(..., description="Imagen a subir"),
    db: Session = Depends(get_db)
):
    logger.info(f"POST /hero: {alt} in {category}")
    image_data = ImageCreate(alt=alt, desc=desc, category=category)
    try:
        created_image = create_image(db, image_data, file)
        return created_image
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail="Failed to create image")

@hero_router.put("/{image_id}", response_model=Image)
def update_hero_endpoint(
    image_id: int,
    alt: Optional[str] = Form(None),
    desc: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    logger.info(f"PUT /hero/{image_id}")
    image_update = ImageUpdate(alt=alt, desc=desc, category=category)
    try:
        return update_image(db, image_id, image_update, file)
    except ValueError as e:
        raise HTTPException(404, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail="Failed to update image")

@hero_router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hero_endpoint(image_id: int, db: Session = Depends(get_db)):
    logger.info(f"DELETE /hero/{image_id}")
    try:
        delete_image(db, image_id)
        return None
    except ValueError as e:
        raise HTTPException(404, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail="Failed to delete image")

# No-slash versions
@hero_router.get("", response_model=list[Image])
def read_hero_no_slash(skip: int = 0, limit: int = 100, category: Optional[str] = Query("hero"), db: Session = Depends(get_db)):
    return get_images(db, skip, limit, category)

@hero_router.post("", response_model=Image, status_code=201)
def create_hero_no_slash(
    alt: str = Form(...), desc: str = Form(...), category: str = Form("hero"),
    file: UploadFile = File(..., description="Imagen a subir"),
    db: Session = Depends(get_db)
):
    image_data = ImageCreate(alt=alt, desc=desc, category=category)
    return create_image(db, image_data, file)