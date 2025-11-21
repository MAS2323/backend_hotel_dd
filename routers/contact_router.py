from fastapi import APIRouter
from schemas.contact_schema import ContactCreate, ContactResponse
from controllers.contact_controller import send_contact_email

contact_router = APIRouter(prefix="/contact", tags=["contact"])

@contact_router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(contact: ContactCreate):  # Removido db (no se usa)
    
    return send_contact_email(contact)