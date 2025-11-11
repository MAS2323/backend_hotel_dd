from pydantic import BaseModel, validator
from typing import Optional

class ImageBase(BaseModel):
    alt: str
    desc: str
    category: str  # "galeria" o "hero"

    @validator('category')
    def validate_category(cls, v):
        if v not in ["galeria", "hero"]:
            raise ValueError('Category must be "galeria" or "hero"')
        return v

class ImageCreate(ImageBase):
    pass  # File handled separately

class ImageUpdate(BaseModel):
    alt: Optional[str] = None
    desc: Optional[str] = None
    category: Optional[str] = None

    @validator('category', pre=True, always=True)
    def validate_category_update(cls, v):
        if v is not None and v not in ["galeria", "hero"]:
            raise ValueError('Category must be "galeria" or "hero"')
        return v

class Image(ImageBase):
    id: int
    url: str
    public_id: str

    class Config:
        from_attributes = True