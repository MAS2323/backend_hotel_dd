from sqlalchemy.orm import Session
from models.testimonial_model import Testimonial
from schemas.testimonial_schema import TestimonialCreate

def get_testimonials(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Testimonial).offset(skip).limit(limit).all()

def create_testimonial(db: Session, testimonial: TestimonialCreate, user_id: int):
    db_testimonial = Testimonial(**testimonial.dict(), user_id=user_id)
    db.add(db_testimonial)
    db.commit()
    db.refresh(db_testimonial)
    return db_testimonial


