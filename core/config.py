from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    database_url: Optional[str] = None  # Construye si no está
    host: str = "localhost"
    username: str = "MAS ONEWE"
    password: str = "2323mas"
    database: str = "hotel_dd"

    # Cloudinary
    cloud_name: str = "masonewead"
    api_key: str = "622884861543834adasd"
    api_secret: str = "21BOdAnPzxEGzJ3mY2NuO1D6rEw"

    # JWT
    SECRET_KEY: str = "HHXXXYYYZZZ1234567890changethisddsa"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # SendGrid
    sendgrid_api_key: str = ""

    # ✅ Nuevos: Para Gmail fallback
    gmail_email: str = "masoneweernesto@gmail.com"
    gmail_app_password: str = "gmvpqypoxxzrjrwf"

    class Config:
        env_file = ".env"

# Instancia global
settings = Settings()

# Override database_url si no está
if not settings.database_url:
    settings.database_url = f"mysql+pymysql://{settings.username}:{settings.password}@{settings.host}/{settings.database}"