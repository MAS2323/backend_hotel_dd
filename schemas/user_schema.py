# schemas/user_schema.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime  # <-- Added this import

class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    email: str = Field(..., max_length=100)
    password: str = Field(..., min_length=6, max_length=72) 
    # If you have role from previous

class UserCreate(UserBase):
    password: str
    email: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: Optional[datetime] = None  # <-- Now datetime is imported; use datetime (not datetime.datetime for type)

    class Config:
        from_attributes = True

# Add Token if needed
class Token(BaseModel):
    access_token: str
    token_type: str