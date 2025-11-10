# schemas/user_schema.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime  # <-- Added this import

class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    password: str = Field(..., min_length=6, max_length=72) 
    # If you have role from previous

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=72)
    email: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool
    role: str  # Agregado (de modelo DB)
    created_at: Optional[datetime] = None  # <-- Now datetime is imported; use datetime (not datetime.datetime for type)

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    is_active: bool
    role: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        
class RoleUpdate(BaseModel):
    role: str = Field(..., max_length=20)  # Valida longitud como en modelo DB

    class Config:
        from_attributes = True  # Opcional, para consistencia
# Add Token if needed
class Token(BaseModel):
    access_token: str
    token_type: str