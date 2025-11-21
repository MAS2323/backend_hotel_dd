# controllers/testimonial_controller.py (actualizado: agrega delete_testimonial, usa content en lugar de quote)
from sqlalchemy.orm import Session
from models.testimonial_model import Testimonial
from schemas.testimonial_schema import TestimonialCreate, Testimonial
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

def get_testimonials(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Testimonial).offset(skip).limit(limit).all()

def create_testimonial(db: Session, testimonial: TestimonialCreate, user_id: int = None):  # ✅ Make optional
    db_testimonial = Testimonial(**testimonial.dict(), user_id=user_id)  # None is fine
    db.add(db_testimonial)
    db.commit()
    db.refresh(db_testimonial)
    user_msg = f" por usuario {user_id}" if user_id else " anónimo"
    logger.info(f"Testimonio creado{user_msg}: {db_testimonial.content[:50]}...")
    return db_testimonial

def delete_testimonial(db: Session, testimonial_id: int, current_user_id: int = None):  # ✅ Make optional
    db_testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not db_testimonial:
        raise HTTPException(status_code=404, detail="Testimonio no encontrado")
    
    # ✅ Fix: Handle None (e.g., allow anon delete if no user_id, or restrict)
    if current_user_id and db_testimonial.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="No autorizado para eliminar este testimonio")
    # If current_user_id is None, perhaps allow admin-only or skip check—adjust per your auth logic
    
    db.delete(db_testimonial)
    db.commit()
    logger.info(f"Testimonio {testimonial_id} eliminado")
    return {"message": "Testimonio eliminado exitosamente"}