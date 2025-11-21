# main.py (actualizado para incluir el nuevo apartment_router y debug para restaurant_router)
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine, Base
from routers.user_router import user_router
from routers.room_router import room_router
from routers.booking_router import booking_router
from routers.gallery_router import gallery_router
from routers.hero_router import hero_router
from routers.testimonial_router import testimonial_router
from routers.admin_router import admin_router
from routers.service_router import public_service_router, admin_service_router
from routers.stats_router import stats_router
from routers.apartment_router import apartment_router  # ✅ Nuevo import
from routers.restaurant_router import restaurant_router  # ✅ Import del router de restaurante
from routers.contact_router import contact_router

from dotenv import load_dotenv
load_dotenv()  # ✅ Carga .env para todas las vars

app = FastAPI(title="Hotel-DD API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.router.redirect_slashes = True

# ==================== DEBUG CRÍTICO ====================
print("\n" + "="*70)
print("🔍 DEBUG: VERIFICACIÓN DE RUTAS ANTES DE REGISTRAR")
print("="*70)

# Verifica que admin_router NO tenga prefijo interno
print(f"admin_router.routes: {len(admin_router.routes)} rutas")
for i, r in enumerate(admin_router.routes):
    print(f"  {i+1}. {r.path} {r.methods}")

# Verifica que admin_service_router SÍ tenga prefijo interno
print(f"\nadmin_service_router.routes: {len(admin_service_router.routes)} rutas")
for i, r in enumerate(admin_service_router.routes):
    print(f"  {i+1}. {r.path} {r.methods}")

# ← NUEVO: Debug para restaurant_router
print(f"\nrestaurant_router.routes: {len(restaurant_router.routes)} rutas")
for i, r in enumerate(restaurant_router.routes):
    full_path = f"/restaurant{r.path}" if r.path != "/" else "/restaurant"
    print(f"  {i+1}. {full_path} {r.methods}")

print("\n" + "="*70 + "\n")
# ======================================================

# ==================== REGISTRO CRÍTICO ====================
# ORDEN: De MENOS específico a MÁS específico

app.include_router(admin_router, prefix="/admin")
app.include_router(admin_service_router) 

# 3. Routers PÚBLICOS (cada uno con su propio prefijo)
app.include_router(public_service_router)   # /services
app.include_router(user_router)             # /users
app.include_router(room_router)             # /rooms
app.include_router(booking_router)          # /bookings
app.include_router(gallery_router)          # /gallery
app.include_router(testimonial_router)      # /testimonials
app.include_router(hero_router)
app.include_router(apartment_router)        # ✅ Nuevo: /apartments
app.include_router(restaurant_router)       # ✅ Restaurante: /restaurant
app.include_router(stats_router)
app.include_router(contact_router)
# ==========================================================

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