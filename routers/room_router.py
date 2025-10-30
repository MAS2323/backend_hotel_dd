from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from typing import List
from core.database import get_db
from core.security import get_current_user
from schemas.room_schema import Room, RoomCreate, RoomBase, RoomImageCreate
from controllers.room_controller import create_room, get_rooms, get_room, update_room, delete_room

room_router = APIRouter(prefix="/rooms", tags=["rooms"])

@room_router.post("/", response_model=Room, status_code=status.HTTP_201_CREATED)
def create_room_endpoint(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    is_available: bool = Form(True),
    alt_list: List[str] = Form([]),  # List of alts for images
    files: List[UploadFile] = File(...),  # Multiple files
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    room_data = RoomCreate(name=name, description=description, price=price, is_available=is_available)
    image_data_list = [RoomImageCreate(alt=alt) for alt in alt_list] if alt_list else []
    return create_room(db, room_data, files if files else None, image_data_list)

@room_router.get("/", response_model=List[Room])
def read_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_rooms(db, skip, limit)

@room_router.get("/{room_id}", response_model=Room)
def read_room(room_id: int, db: Session = Depends(get_db)):
    db_room = get_room(db, room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room

@room_router.put("/{room_id}", response_model=Room)
def update_room_endpoint(
    room_id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    is_available: Optional[bool] = Form(None),
    alt_list: List[str] = Form([]),
    files: List[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    room_update = RoomBase(name=name, description=description, price=price, is_available=is_available)
    image_data_list = [RoomImageCreate(alt=alt) for alt in alt_list] if alt_list else []
    return update_room(db, room_id, room_update, files if files else None, image_data_list)

@room_router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room_endpoint(room_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    deleted = delete_room(db, room_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return None