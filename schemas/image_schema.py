# schemas/image_schema.py
from pydantic import BaseModel
from typing import Optional

class ImageBase(BaseModel):
    alt: str
    desc: str

class ImageCreate(ImageBase):
    pass  # File handled separately

class ImageUpdate(BaseModel):
    alt: Optional[str] = None
    desc: Optional[str] = None

class Image(ImageBase):
    id: int
    url: str
    public_id: str

    class Config:
        from_attributes = True