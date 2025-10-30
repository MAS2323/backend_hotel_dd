from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine, Base
from routers.user_router import user_router      # ✅ Import the router instance
from routers.room_router import room_router      # ✅ Import the router instance
from routers.booking_router import booking_router
from routers.gallery_router import  gallery_router
from routers.testimonial_router import  testimonial_router  
from routers.gallery_router import gallery_router
from routers.admin_router import admin_router
from routers.service_router import service_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hotel-DD API", description="Backend por capas para Hotel-DD", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.router.redirect_slashes = False
app.include_router(user_router)   # Now this is the APIRouter instance
app.include_router(room_router)
app.include_router(booking_router)
app.include_router(gallery_router)
app.include_router(testimonial_router)
app.include_router(gallery_router)
app.include_router(service_router)  # Public services
app.include_router(admin_router)

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API por capas de Hotel-DD! Visita /docs."}