# controllers/restaurant_controller.py (actualizado: agrega manejo de file para create/update restaurant, similar a menu_item, y usa ensure_default_restaurant)
from sqlalchemy.orm import Session
from models.restaurant_model import Restaurant, MenuItem
from schemas.restaurant_schema import (
    RestaurantCreate, RestaurantUpdate, MenuItemCreate, MenuItemUpdate
)
from fastapi import HTTPException
from typing import List
from fastapi import UploadFile, HTTPException, Form  # ← Importa para router, pero usa en controller
from core.cloudinary_config import upload_image  # Asume helper
import logging

logger = logging.getLogger(__name__)

def get_restaurant(db: Session, restaurant_id: int = 1):  # Asume ID fijo para el restaurante principal
    return db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

def get_restaurants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Restaurant).offset(skip).limit(limit).all()

def create_restaurant(db: Session, restaurant: RestaurantCreate, file: UploadFile = None):
    try:
        # Validar
        if not file:
            raise ValueError("Se requiere una imagen para el restaurante")

        # Subir imagen
        logger.info(f"Subiendo imagen para restaurante '{restaurant.title}'")
        image_url, image_public_id = upload_image(file.file, folder="hotel_dd/restaurant")

        # Crear (campos explícitos para evitar kwargs duplicados)
        db_restaurant = Restaurant(
            title=restaurant.title,
            description=restaurant.description,
            image_url=image_url,
            image_public_id=image_public_id
        )
        db.add(db_restaurant)
        db.commit()
        db.refresh(db_restaurant)
        logger.info(f"✅ Restaurante '{db_restaurant.title}' creado con ID {db_restaurant.id}")
        return db_restaurant
    except ValueError as e:
        if db.is_active:
            db.rollback()
        raise e
    except Exception as e:
        logger.error(f"Error creando restaurante: {e}")
        if db.is_active:
            db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear restaurante: {str(e)}")

def update_restaurant(db: Session, restaurant_id: int, restaurant_update: RestaurantUpdate, file: UploadFile = None):
    db_restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    updated = False
    update_data = restaurant_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_restaurant, field, value)
        updated = True

    # Manejar imagen si hay file
    if file:
        # Eliminar antigua si existe
        if db_restaurant.image_public_id:
            try:
                from cloudinary.uploader import destroy
                destroy(db_restaurant.image_public_id, resource_type="image")
                logger.info("Imagen anterior del restaurante eliminada")
            except Exception as e:
                logger.warning(f"No se pudo eliminar imagen anterior del restaurante: {e}")

        # Subir nueva
        image_url, image_public_id = upload_image(file.file, folder="hotel_dd/restaurant")
        db_restaurant.image_url = image_url
        db_restaurant.image_public_id = image_public_id
        updated = True

    if updated:
        db.commit()
        db.refresh(db_restaurant)

    return db_restaurant

def delete_restaurant(db: Session, restaurant_id: int):
    db_restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    db.delete(db_restaurant)
    db.commit()
    return {"message": "Restaurant deleted"}

def ensure_default_restaurant(db: Session):
    """Crea un restaurante default si no existe con ID=1"""
    restaurant = get_restaurant(db, 1)
    if not restaurant:
        logger.info("Creando restaurante default...")
        default_restaurant_data = RestaurantCreate(
            title="Restaurante D&D",
            description="El restaurante del Hotel D&D ofrece una variedad de platos exquisitos en un ambiente acogedor.",
            # Nota: image_url no se usa aquí ya que se maneja en create con file, pero para default usamos placeholder
        )
        # Para default, crear sin file y setear placeholders
        db_default = Restaurant(
            title=default_restaurant_data.title,
            description=default_restaurant_data.description,
            image_url="https://via.placeholder.com/800x400?text=Restaurante+D&D",
            image_public_id="default_restaurant_placeholder"
        )
        db.add(db_default)
        db.commit()
        db.refresh(db_default)
        logger.info(f"✅ Restaurante default creado con ID {db_default.id}")
        return db_default
    return restaurant

# Menu Items (sin cambios)
def get_menu_items(db: Session, restaurant_id: int = 1, skip: int = 0, limit: int = 100):
    # Asegurar que el restaurante existe
    ensure_default_restaurant(db)
    return db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).offset(skip).limit(limit).all()

def create_menu_item(db: Session, menu_item: MenuItemCreate, restaurant_id: int = 1, file: UploadFile = None):
    try:
        # Asegurar que el restaurante existe
        ensure_default_restaurant(db)

        # Validar
        if not file:
            raise ValueError("Se requiere una imagen para el ítem del menú")

        # Subir imagen
        logger.info(f"Subiendo imagen para ítem '{menu_item.name}'")
        image_url, image_public_id = upload_image(file.file, folder="hotel_dd/menu_items")

        # Crear (campos explícitos para evitar kwargs duplicados con image_url en schema)
        db_menu_item = MenuItem(
            name=menu_item.name,
            description=menu_item.description,
            price=menu_item.price,
            category=menu_item.category,
            restaurant_id=restaurant_id,
            image_url=image_url,
            image_public_id=image_public_id
        )
        db.add(db_menu_item)
        db.commit()
        db.refresh(db_menu_item)
        logger.info(f"✅ Ítem '{db_menu_item.name}' creado con ID {db_menu_item.id}")
        return db_menu_item
    except ValueError as e:
        if db.is_active:
            db.rollback()
        raise e
    except Exception as e:
        logger.error(f"Error creando ítem: {e}")
        if db.is_active:
            db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear ítem: {str(e)}")

def update_menu_item(db: Session, menu_item_id: int, menu_item_update: MenuItemUpdate, file: UploadFile = None):
    # Asegurar que el restaurante existe (por si acaso)
    ensure_default_restaurant(db)
    
    db_menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
    if not db_menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    updated = False
    update_data = menu_item_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_menu_item, field, value)
        updated = True

    # Manejar imagen si hay file
    if file:
        # Eliminar antigua si existe
        if db_menu_item.image_public_id:
            try:
                from cloudinary.uploader import destroy
                destroy(db_menu_item.image_public_id, resource_type="image")
                logger.info("Imagen anterior eliminada")
            except Exception as e:
                logger.warning(f"No se pudo eliminar imagen anterior: {e}")

        # Subir nueva
        image_url, image_public_id = upload_image(file.file, folder="hotel_dd/menu_items")
        db_menu_item.image_url = image_url
        db_menu_item.image_public_id = image_public_id
        updated = True

    if updated:
        db.commit()
        db.refresh(db_menu_item)

    return db_menu_item

def delete_menu_item(db: Session, menu_item_id: int):
    db_menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
    if not db_menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    db.delete(db_menu_item)
    db.commit()
    return {"message": "Menu item deleted"}