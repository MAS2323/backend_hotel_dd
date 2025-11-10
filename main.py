from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from core.database import engine
from routers.user_router import user_router
from routers.room_router import room_router
from routers.booking_router import booking_router
from routers.gallery_router import gallery_router
from routers.testimonial_router import testimonial_router
from routers.admin_router import admin_router
from routers.service_router import public_service_router, admin_service_router

# Import models
from models.user_model import User
from models.booking_model import Booking
from models.testimonial_model import Testimonial
from core.database import Base

app = FastAPI(title="Hotel-DD API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.router.redirect_slashes = False

# ==================== DEBUG ROUTERS ====================
print("\n" + "="*60)
print("🔍 DEBUG: IMPORTACIÓN DE ROUTERS")
print("="*60)
print(f"public_service_router: {public_service_router}")
print(f"admin_service_router: {admin_service_router}")
print(f"Rutas en admin_service_router: {len(admin_service_router.routes)}")
for i, route in enumerate(admin_service_router.routes):
    print(f"  {i+1}. {route.path} {route.methods}")
print("="*60 + "\n")
# ======================================================

# Register routers
app.include_router(user_router)
app.include_router(room_router)
app.include_router(booking_router)
app.include_router(gallery_router)
app.include_router(testimonial_router)
app.include_router(admin_router)
app.include_router(public_service_router)



app.include_router(admin_service_router, prefix="/admin")  # /admin/
app.include_router(admin_router, prefix="/admin")  # /admin

@app.get("/")
def read_root():
    return {"message": "¡API de Hotel-DD funcionando! Visita /docs"}

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente al inicio.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)