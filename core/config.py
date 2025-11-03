# core/config.py
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # DB Components (from .env)
    username: str = "root"  # Default for dev; override in .env
    password: str = ""      # Empty default; set in .env
    host: str = "localhost"
    database: str = "hotel_dd"
    
    # Cloudinary
    cloud_name: str = "masonewe"  # Default; overridden by env
    api_key: str = "622884861543834"
    api_secret: str = "21BOdAnPzxEGzJ3mY2NuO1D6rEw"
    upload_prefix: str = "holet_dd"  # Para carpetas como "holet_dd/gallery"
    
    SECRET_KEY: str = "HHXXXYYYZZZ1234567890changethis"  # Cambia por una clave segura (e.g., generada con secrets.token_hex(32))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Computed DB URL (don't set in .env; let code build it)
    @property
    def sqlalchemy_database_url(self) -> str:
        return f"mysql+pymysql://{self.username}:{self.password}@{self.host}/{self.database}"
    
    # Other settings (from .env)
    secret_key: str = "HHXXXYYYZZZ1234567890changethis"  # Change this!
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # If you have DATABASE_URL as a fallback/override
    database_url: Optional[str] = None  # Set in .env if you prefer full URL over components
    
    class Config:
        env_file = ".env"  # Loads from .env in project root

settings = Settings()

# Optional: Override database_url if components are used
if not settings.database_url:
    settings.database_url = settings.sqlalchemy_database_url
    
    

cloud_name: str = "masonewe"
api_key: str = "62288486154383"
api_secret: str = "21BOdAnPzxEGzJ3mY2NuO1D6rEw"