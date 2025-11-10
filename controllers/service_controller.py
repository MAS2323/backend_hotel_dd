from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from typing import Optional
from models.service_model import Service
from schemas.service_schema import ServiceCreate, ServiceUpdate
import cloudinary.uploader
import logging

logger = logging.getLogger(__name__)

# controllers/service_controller.py
def create_service(db: Session, service_data: ServiceCreate, file: UploadFile = None):
    if not file:
        raise ValueError("Icon file is required")
    
    result = cloudinary.uploader.upload(
        file.file,
        folder="hotel_dd/services",
        resource_type="image",
        format="auto"
    )
    
    db_service = Service(
        title=service_data.title,
        desc=service_data.desc,
        icon_url=result['secure_url'],
        icon_public_id=result['public_id']
    )
    
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def get_services(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene lista de servicios con paginación
    """
    try:
        services = db.query(Service).offset(skip).limit(limit).all()
        logger.info(f"Se obtuvieron {len(services)} servicios")
        return services
    except Exception as e:
        logger.error(f"Error obteniendo servicios: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener servicios")

def get_service(db: Session, service_id: int):
    """
    Obtiene un servicio específico por ID
    """
    try:
        service = db.query(Service).filter(Service.id == service_id).first()
        if not service:
            logger.warning(f"Servicio {service_id} no encontrado")
        return service
    except Exception as e:
        logger.error(f"Error obteniendo servicio {service_id}: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener servicio")

def update_service(db: Session, service_id: int, service_update: ServiceUpdate, file: UploadFile = None):
    """
    Actualiza un servicio y opcionalmente su icono
    """
    try:
        # Buscar servicio
        db_service = db.query(Service).filter(Service.id == service_id).first()
        if not db_service:
            raise ValueError("Service not found")
        
        # Actualizar campos básicos (solo si tienen valor)
        update_data = service_update.model_dump(exclude_none=True)
        for field, value in update_data.items():
            setattr(db_service, field, value)
        
        # Manejar nuevo icono si se proporciona
        if file:
            # Eliminar imagen antigua de Cloudinary usando public_id
            if db_service.icon_public_id:
                try:
                    cloudinary.uploader.destroy(db_service.icon_public_id, resource_type="image")
                    logger.info(f"Icono anterior {db_service.icon_public_id} eliminado de Cloudinary")
                except Exception as e:
                    logger.warning(f"No se pudo eliminar icono anterior: {e}")
            
            # Subir nuevo icono
            result = cloudinary.uploader.upload(
                file.file,
                folder="hotel_dd/services",
                resource_type="image",
                format="auto"
            )
            
            db_service.icon_url = result['secure_url']
            db_service.icon_public_id = result['public_id']  # ✅ Actualizamos public_id
        
        db.commit()
        db.refresh(db_service)
        logger.info(f"Servicio {service_id} actualizado exitosamente")
        return db_service
        
    except ValueError as e:
        logger.error(f"Error de validación actualizando servicio {service_id}: {e}")
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Error inesperado actualizando servicio {service_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar servicio: {str(e)}")

def delete_service(db: Session, service_id: int):
    """
    Elimina un servicio y su icono de Cloudinary
    """
    try:
        db_service = db.query(Service).filter(Service.id == service_id).first()
        if not db_service:
            raise ValueError("Service not found")
        
        # Eliminar icono de Cloudinary usando public_id almacenado
        if db_service.icon_public_id:
            try:
                cloudinary.uploader.destroy(db_service.icon_public_id, resource_type="image")
                logger.info(f"Icono {db_service.icon_public_id} eliminado de Cloudinary")
            except Exception as e:
                logger.warning(f"No se pudo eliminar icono de Cloudinary: {e}")
        
        # Eliminar de la base de datos
        db.delete(db_service)
        db.commit()
        logger.info(f"Servicio {service_id} eliminado exitosamente")
        return {"message": "Service deleted successfully"}
        
    except ValueError as e:
        logger.error(f"Error de validación eliminando servicio {service_id}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado eliminando servicio {service_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar servicio: {str(e)}")