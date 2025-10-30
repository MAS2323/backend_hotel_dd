# core/cloudinary_config.py (actualizado)
import cloudinary
import cloudinary.uploader
from core.config import settings

cloudinary.config(
    cloud_name=settings.cloud_name,
    api_key=settings.api_key,
    api_secret=settings.api_secret,
)

def upload_image(file, folder=None):
    """Sube imagen a Cloudinary y retorna URL segura."""
    if folder is None:
        folder = f"{settings.upload_prefix}/gallery"  # Usa prefix de settings
    try:
        result = cloudinary.uploader.upload(
            file, folder=folder, resource_type="image", format="auto"
        )
        return result['secure_url'], result['public_id']  # Retorna ambos para modelo
    except Exception as e:
        raise ValueError(f"Error subiendo imagen: {str(e)}")