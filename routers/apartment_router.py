# routers/apartment_router.py (renombrado, prefix cambiado a /apartments para consistencia)
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional, List
from core.database import get_db
from core.security import get_current_user
from schemas.apartment_schema import Apartment, ApartmentCreate, ApartmentUpdate, ApartmentImageCreate
from controllers.apartment_controller import create_apartment, get_apartments, get_apartment, update_apartment, delete_apartment

apartment_router = APIRouter(prefix="/apartments", tags=["apartments"])

@apartment_router.post("/", response_model=Apartment, status_code=status.HTTP_201_CREATED)
def create_apartment_endpoint(
    name: str = Form(...),
    description: str = Form(...),
    head: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    capacity: int = Form(2),
    price_per_night: float = Form(0.0),
    amenities: Optional[List[str]] = Form(None),
    num_bedrooms: int = Form(1),
    num_bathrooms: int = Form(1),
    square_meters: Optional[float] = Form(None),
    is_active: bool = Form(True),
    alt_list: List[str] = Form([]),
    files: List[UploadFile] = File([]),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    apartment_data = ApartmentCreate(
        name=name, description=description, head=head,
        email=email, phone=phone, capacity=capacity, price_per_night=price_per_night,
        amenities=amenities, num_bedrooms=num_bedrooms, num_bathrooms=num_bathrooms,
        square_meters=square_meters, is_active=is_active
    )
    image_data_list = [ApartmentImageCreate(alt=alt) for alt in alt_list] if alt_list else []
    return create_apartment(db, apartment_data, files if files else None, image_data_list)

@apartment_router.get("/", response_model=List[Apartment])
def read_apartments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_apartments(db, skip, limit)

@apartment_router.get("/{apartment_id}", response_model=Apartment)
def read_apartment(apartment_id: int, db: Session = Depends(get_db)):
    db_apartment = get_apartment(db, apartment_id)
    if db_apartment is None:
        raise HTTPException(status_code=404, detail="Apartment not found")
    return db_apartment

@apartment_router.put("/{apartment_id}", response_model=Apartment)
def update_apartment_endpoint(
    apartment_id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    head: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    capacity: Optional[int] = Form(None),
    price_per_night: Optional[float] = Form(None),
    amenities: Optional[List[str]] = Form(None),
    num_bedrooms: Optional[int] = Form(None),
    num_bathrooms: Optional[int] = Form(None),
    square_meters: Optional[float] = Form(None),
    is_active: Optional[bool] = Form(None),
    alt_list: List[str] = Form([]),
    files: List[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    apartment_update_dict = {}
    for key, value in [
        ("name", name), ("description", description),
        ("head", head), ("email", email), ("phone", phone),
        ("capacity", capacity), ("price_per_night", price_per_night),
        ("amenities", amenities), ("num_bedrooms", num_bedrooms),
        ("num_bathrooms", num_bathrooms), ("square_meters", square_meters),
        ("is_active", is_active)
    ]:
        if value is not None:
            apartment_update_dict[key] = value
    
    apartment_update = ApartmentUpdate(**apartment_update_dict)
    image_data_list = [ApartmentImageCreate(alt=alt) for alt in alt_list] if alt_list else []
    return update_apartment(db, apartment_id, apartment_update, files if files else None, image_data_list)

@apartment_router.delete("/{apartment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_apartment_endpoint(apartment_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    deleted = delete_apartment(db, apartment_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Apartment not found")
    return None