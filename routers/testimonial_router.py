from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from core.security import get_current_user
from schemas.testimonial_schema import Testimonial, TestimonialCreate
from controllers.testimonial_controller import (
    get_testimonials, create_testimonial, delete_testimonial
)

testimonial_router = APIRouter(prefix="/testimonials", tags=["testimonials"])

@testimonial_router.post("/", response_model=Testimonial, status_code=201)
def create_testimonial_endpoint(
    testimonial: TestimonialCreate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    # ✅ Fix: Use current_user.sub (convert to int; handle potential KeyError if no sub)
    user_id = int(current_user.sub) if current_user.sub else None
    return create_testimonial(db, testimonial, user_id)  # Pass None for anon if needed

@testimonial_router.get("/", response_model=List[Testimonial])
def read_testimonials(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_testimonials(db, skip, limit)

@testimonial_router.delete("/{testimonial_id}", status_code=204)
def delete_testimonial_endpoint(
    testimonial_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # ✅ Fix: Same as above
    user_id = int(current_user.sub) if current_user.sub else None
    delete_testimonial(db, testimonial_id, user_id)
    return None