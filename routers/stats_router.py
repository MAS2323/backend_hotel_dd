# routers/stats_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user, TokenData
from models.room_model import Room  # Adjust imports for your models
from models.service_model import Service
from models.booking_model import Booking
from models.user_model import User  # If User model exists
import logging

logger = logging.getLogger(__name__)

stats_router = APIRouter(prefix="/admin/stats", tags=["Admin Stats"])

def require_admin(current_user: TokenData = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "Admin required")
    return current_user

@stats_router.get("/rooms")
def get_rooms_stats(db: Session = Depends(get_db), current_user: TokenData = Depends(require_admin)):
    count = db.query(Room).count()
    logger.info(f"Rooms stats requested: {count}")
    return {"total": count}

@stats_router.get("/services")
def get_services_stats(db: Session = Depends(get_db), current_user: TokenData = Depends(require_admin)):
    count = db.query(Service).count()
    return {"total": count}

@stats_router.get("/bookings")
def get_bookings_stats(db: Session = Depends(get_db), current_user: TokenData = Depends(require_admin)):
    count = db.query(Booking).count()
    return {"total": count}

@stats_router.get("/users")
def get_users_stats(db: Session = Depends(get_db), current_user: TokenData = Depends(require_admin)):
    count = db.query(User).count()
    return {"total": count}