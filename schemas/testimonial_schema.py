# schemas/testimonial_schema.py (actualizado: cambia quote a content)
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TestimonialBase(BaseModel):
    content: str
    author: str

class TestimonialCreate(TestimonialBase):
    pass

class Testimonial(TestimonialBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True