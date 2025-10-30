from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from core.security import get_current_user
from schemas.testimonial_schema import Testimonial, TestimonialCreate
from controllers.testimonial_controller import create_testimonial, get_testimonials

testimonial_router = APIRouter(prefix="/testimonials", tags=["testimonials"])

@testimonial_router.post("/", response_model=Testimonial, status_code=201)
def create_testimonial_endpoint(
    testimonial: TestimonialCreate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    
    return create_testimonial(db, testimonial, current_user.id)

@testimonial_router.get("/", response_model=List[Testimonial])
def read_testimonials(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_testimonials(db, skip, limit)