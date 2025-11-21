from pydantic import BaseModel, EmailStr  # EmailStr viene de Pydantic, no de typing

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    message: str

class ContactResponse(BaseModel):
    message: str = "Mensaje enviado exitosamente"
    
    class Config:
        from_attributes = True  # Para Pydantic v1; si usas v2, cambia a model_config = {"from_attributes": True}