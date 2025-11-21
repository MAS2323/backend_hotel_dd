# routers/restaurant_router.py (actualizado: cambia create/update restaurant a Form/File-based para multipart upload de imagen)
from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.restaurant_schema import (
    Restaurant, RestaurantUpdate,
    MenuItem, MenuItemCreate, MenuItemUpdate
)
from controllers.restaurant_controller import (
    get_restaurant, get_restaurants, create_restaurant, update_restaurant, delete_restaurant,
    get_menu_items, create_menu_item, update_menu_item, delete_menu_item
)

restaurant_router = APIRouter(prefix="/restaurant", tags=["restaurant"])

# Restaurant endpoints (Form/File-based para create/update con imagen)
@restaurant_router.get("/", response_model=Restaurant)
def read_restaurant(restaurant_id: int = 1, db: Session = Depends(get_db)):
    db_restaurant = get_restaurant(db, restaurant_id)
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_restaurant

@restaurant_router.get("/all", response_model=List[Restaurant])
def read_restaurants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_restaurants(db, skip, limit)

@restaurant_router.post("/", response_model=Restaurant, status_code=201)
def create_restaurant_endpoint(
    title: str = Form(..., description="Título del restaurante"),
    description: str = Form(..., description="Descripción"),
    file: UploadFile = File(..., description="Imagen del restaurante (requerida)"),
    db: Session = Depends(get_db)
):
    # Crear schema temporal para controller
    from schemas.restaurant_schema import RestaurantCreate
    temp_create = RestaurantCreate(title=title, description=description)
    return create_restaurant(db, temp_create, file)

@restaurant_router.put("/{restaurant_id}", response_model=Restaurant)
def update_restaurant_endpoint(
    restaurant_id: int,
    title: str = Form(None, description="Nuevo título (opcional)"),
    description: str = Form(None, description="Nueva descripción (opcional)"),
    file: UploadFile = File(None, description="Nueva imagen (opcional)"),
    db: Session = Depends(get_db)
):
    update_data = {k: v for k, v in {"title": title, "description": description}.items() if v is not None}
    from schemas.restaurant_schema import RestaurantUpdate
    restaurant_update = RestaurantUpdate(**update_data) if update_data else RestaurantUpdate()
    return update_restaurant(db, restaurant_id, restaurant_update, file)

@restaurant_router.delete("/{restaurant_id}", status_code=204)
def delete_restaurant_endpoint(restaurant_id: int, db: Session = Depends(get_db)):
    delete_restaurant(db, restaurant_id)
    return None

# Menu endpoints (sin cambios, ya Form/File-based)
@restaurant_router.get("/menu", response_model=List[MenuItem])
def read_menu(restaurant_id: int = 1, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_menu_items(db, restaurant_id, skip, limit)

@restaurant_router.post("/menu", response_model=MenuItem, status_code=201)
def create_menu_item_endpoint(
    name: str = Form(..., description="Nombre del plato"),
    description: str = Form(..., description="Descripción"),
    price: float = Form(..., description="Precio"),
    category: str = Form(..., description="Categoría"),
    file: UploadFile = File(..., description="Imagen del ítem (requerida)"),
    restaurant_id: int = 1,
    db: Session = Depends(get_db)
):
    menu_item = MenuItemCreate(name=name, description=description, price=price, category=category)
    return create_menu_item(db, menu_item, restaurant_id, file)

@restaurant_router.put("/menu/{menu_item_id}", response_model=MenuItem)
def update_menu_item_endpoint(
    menu_item_id: int,
    name: str = Form(None, description="Nuevo nombre (opcional)"),
    description: str = Form(None, description="Nueva descripción (opcional)"),
    price: float = Form(None, description="Nuevo precio (opcional)"),
    category: str = Form(None, description="Nueva categoría (opcional)"),
    file: UploadFile = File(None, description="Nueva imagen (opcional)"),
    db: Session = Depends(get_db)
):
    update_data = {k: v for k, v in {
        "name": name, "description": description, "price": price, "category": category
    }.items() if v is not None}
    menu_update = MenuItemUpdate(**update_data) if update_data else MenuItemUpdate()
    return update_menu_item(db, menu_item_id, menu_update, file)

@restaurant_router.delete("/menu/{menu_item_id}", status_code=204)
def delete_menu_item_endpoint(menu_item_id: int, db: Session = Depends(get_db)):
    delete_menu_item(db, menu_item_id)
    return None