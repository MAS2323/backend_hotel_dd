from pydantic import BaseModel
from typing import Optional

class ImageBase(BaseModel):
    alt: str
    desc: str

class ImageCreate(ImageBase):
    file: Optional[str] = None  # Para upload inicial

class ImageUpdate(BaseModel):
    alt: Optional[str] = None
    desc: Optional[str] = None
    file: Optional[str] = None  # Opcional para re-upload

class Image(ImageBase):
    id: int
    url: str
    public_id: str

    class Config:
        from_attributes = True