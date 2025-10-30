from pydantic import BaseModel

class TestimonialBase(BaseModel):
    quote: str
    author: str

class TestimonialCreate(TestimonialBase):
    pass

class Testimonial(TestimonialBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True