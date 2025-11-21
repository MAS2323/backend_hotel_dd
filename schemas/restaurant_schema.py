# schemas/restaurant_schema.py (actualizado: agrega image_public_id a Restaurant y schemas relacionados; quita image_url de Create ya que se maneja en controller)
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class RestaurantBase(BaseModel):
    title: str
    description: str

class RestaurantCreate(RestaurantBase):
    pass  # Sin image_url, se maneja en controller con upload

class RestaurantUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class Restaurant(RestaurantBase):
    id: int
    image_url: str
    image_public_id: str
    created_at: datetime
    menu_items: List['MenuItem'] = []

    class Config:
        from_attributes = True

class MenuItemBase(BaseModel):
    name: str
    description: str
    price: float
    category: str
    image_url: Optional[str] = None

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    image_url: Optional[str] = None

class MenuItem(MenuItemBase):
    id: int
    restaurant_id: int
    image_public_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True