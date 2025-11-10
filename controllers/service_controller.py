# controllers/service_controller.py
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from typing import Optional, List
from models.service_model import Service
from core.cloudinary_config import upload_image  # ✅ Import helper
import logging

logger = logging.getLogger(__name__)

def create_service(db: Session, title: str, desc: str, file: UploadFile):  # ✅ Changed: Raw str params, no ServiceCreate
    """
    Crea un nuevo servicio con icono en Cloudinary
    """
    try:
        # Validar campos (básico)
        if not title or not desc:
            raise ValueError("Título y descripción son requeridos")
        if not file:
            raise ValueError("Se requiere un archivo de icono")

        # Subir imagen a Cloudinary usando helper
        logger.info(f"Subiendo icono a Cloudinary para servicio '{title}'")
        icon_url, icon_public_id = upload_image(file.file, folder="hotel_dd/services")  # ✅ Use helper
        
        # Verificar duplicado (opcional)
        existing = db.query(Service).filter(Service.icon_url == icon_url).first()
        if existing:
            # Cleanup (destroy would need import, but skip for now or add)
            raise ValueError("Este icono ya existe para otro servicio")
        
        # Crear servicio
        db_service = Service(
            title=title,
            desc=desc,
            icon_url=icon_url,
            icon_public_id=icon_public_id
        )
        
        db.add(db_service)
        db.commit()
        db.refresh(db_service)
        logger.info(f"✅ Servicio '{db_service.title}' creado exitosamente con ID {db_service.id}")
        return db_service
        
    except ValueError as e:
        logger.error(f"❌ Error de validación creando servicio: {e}")
        if db.is_active:  # ✅ Better: Check if session active before rollback
            db.rollback()
        raise e  # Re-raise for router to catch as ValueError
    except Exception as e:
        logger.error(f"❌ Error inesperado creando servicio: {e}")
        if db.is_active:
            db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear servicio: {str(e)}")

def get_services(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene lista de servicios con paginación
    """
    try:
        services = db.query(Service).offset(skip).limit(limit).all()
        logger.info(f"📋 Se obtuvieron {len(services)} servicios (skip={skip}, limit={limit})")
        return services  # ✅ ORM objects; response_model=List[Service] converts via from_attributes
    except Exception as e:
        logger.error(f"❌ Error obteniendo servicios: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener servicios")

def get_service(db: Session, service_id: int):
    """
    Obtiene un servicio específico por ID
    """
    try:
        service = db.query(Service).filter(Service.id == service_id).first()
        if not service:
            logger.warning(f"⚠️ Servicio {service_id} no encontrado")
            raise ValueError(f"Servicio con ID {service_id} no existe")  # ✅ Changed: ValueError for consistency
        return service
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"❌ Error obteniendo servicio {service_id}: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener servicio")

def update_service(
    db: Session, 
    service_id: int, 
    title: Optional[str] = None,  # ✅ Raw optionals, no ServiceUpdate
    desc: Optional[str] = None,
    file: Optional[UploadFile] = None
):
    """
    Actualiza un servicio y opcionalmente su icono
    """
    try:
        # Buscar servicio
        db_service = get_service(db, service_id)  # ✅ Reuse helper for not-found check
        
        # Solo actualizar si hay cambios
        updated = False
        if title is not None:
            db_service.title = title
            updated = True
        if desc is not None:
            db_service.desc = desc
            updated = True
        if not updated and not file:
            logger.info(f"No hay cambios para aplicar en servicio {service_id}")
            return db_service
            
        logger.info(f"Actualizando servicio {service_id}: title={title}, desc={desc}, file={file is not None}")
        
        # Manejar nuevo icono
        if file:
            # Eliminar antigua
            if db_service.icon_public_id:
                try:
                    from cloudinary.uploader import destroy  # ✅ Local import to avoid global
                    destroy(db_service.icon_public_id, resource_type="image")
                    logger.info(f"🗑️ Icono anterior eliminado")
                except Exception as e:
                    logger.warning(f"⚠️ No se pudo eliminar icono anterior: {e}")
            
            # Subir nuevo
            icon_url, icon_public_id = upload_image(file.file, folder="hotel_dd/services")
            db_service.icon_url = icon_url
            db_service.icon_public_id = icon_public_id
            updated = True  # Force update
        
        if updated:
            db.commit()
            db.refresh(db_service)
            logger.info(f"✅ Servicio {service_id} actualizado exitosamente")
        
        return db_service
        
    except ValueError as e:
        logger.error(f"❌ Error de validación: {e}")
        if db.is_active:
            db.rollback()
        raise e
    except Exception as e:
        logger.error(f"❌ Error inesperado actualizando servicio: {e}")
        if db.is_active:
            db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar servicio: {str(e)}")

def delete_service(db: Session, service_id: int):
    """
    Elimina un servicio y su icono de Cloudinary
    """
    try:
        db_service = get_service(db, service_id)  # ✅ Reuse for not-found
        
        # Eliminar icono
        if db_service.icon_public_id:
            try:
                from cloudinary.uploader import destroy
                destroy(db_service.icon_public_id, resource_type="image")
                logger.info(f"🗑️ Icono eliminado")
            except Exception as e:
                logger.warning(f"⚠️ No se pudo eliminar icono: {e}")
        
        # Eliminar de DB
        db.delete(db_service)
        db.commit()
        logger.info(f"✅ Servicio {service_id} eliminado exitosamente")
        
    except ValueError as e:
        raise e  # For 404 in router
    except Exception as e:
        logger.error(f"❌ Error eliminando servicio {service_id}: {e}")
        if db.is_active:
            db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar servicio: {str(e)}")