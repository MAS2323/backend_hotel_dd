from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional, List
from core.database import get_db
from core.security import get_current_user
from schemas.department_schema import Department, DepartmentCreate, DepartmentUpdate, DepartmentImageCreate
from controllers.department_controller import create_department, get_departments, get_department, update_department, delete_department

department_router = APIRouter(prefix="/departments", tags=["departments"])

@department_router.post("/", response_model=Department, status_code=status.HTTP_201_CREATED)
def create_department_endpoint(
    name: str = Form(...),
    description: str = Form(...),
    head: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    is_active: bool = Form(True),
    alt_list: List[str] = Form([]),
    files: List[UploadFile] = File([]),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    department_data = DepartmentCreate(
        name=name, description=description, head=head,
        email=email, phone=phone, is_active=is_active
    )
    image_data_list = [DepartmentImageCreate(alt=alt) for alt in alt_list] if alt_list else []
    return create_department(db, department_data, files if files else None, image_data_list)

@department_router.get("/", response_model=List[Department])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_departments(db, skip, limit)

@department_router.get("/{department_id}", response_model=Department)
def read_department(department_id: int, db: Session = Depends(get_db)):
    db_department = get_department(db, department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department

@department_router.put("/{department_id}", response_model=Department)
def update_department_endpoint(
    department_id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    head: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(None),
    alt_list: List[str] = Form([]),
    files: List[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    department_update_dict = {}
    for key, value in [
        ("name", name), ("description", description),
        ("head", head), ("email", email), ("phone", phone),
        ("is_active", is_active)
    ]:
        if value is not None:
            department_update_dict[key] = value
    
    department_update = DepartmentUpdate(**department_update_dict)
    image_data_list = [DepartmentImageCreate(alt=alt) for alt in alt_list] if alt_list else []
    return update_department(db, department_id, department_update, files if files else None, image_data_list)

@department_router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department_endpoint(department_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    deleted = delete_department(db, department_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return None