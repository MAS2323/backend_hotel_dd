from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from typing import List
from core.database import get_db
from schemas.image_schema import Image, ImageCreate, ImageUpdate
from controllers.image_controller import create_image, get_images, update_image, delete_image

gallery_router = APIRouter(prefix="/gallery", tags=["gallery"])

@gallery_router.post("/", response_model=Image, status_code=201)
def create_image_endpoint(
    alt: str = Form(...),
    desc: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    image_data = ImageCreate(alt=alt, desc=desc)
    return create_image(db, image_data, file)

@gallery_router.get("/", response_model=List[Image])
def read_gallery(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_images(db, skip, limit)

@gallery_router.put("/{image_id}", response_model=Image)
def update_image_endpoint(
    image_id: int,
    alt: Optional[str] = Form(None),
    desc: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    image_update = ImageUpdate(alt=alt, desc=desc)
    try:
        return update_image(db, image_id, image_update, file)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@gallery_router.delete("/{image_id}", status_code=204)
def delete_image_endpoint(image_id: int, db: Session = Depends(get_db)):
    try:
        delete_image(db, image_id)
        return {"message": "Deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))