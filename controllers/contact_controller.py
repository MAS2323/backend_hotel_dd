import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
from datetime import datetime
import logging
import os
import time  # Para reintentos
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

def send_contact_email(contact, max_retries=3):
    sender_email = os.getenv('GMAIL_EMAIL', 'masoneweernesto@gmail.com')
    sender_password = os.getenv('GMAIL_APP_PASSWORD')
    receiver_email = 'hotelddguineaecuatorial@gmail.com'
    
    if not sender_password:
        raise ValueError("GMAIL_APP_PASSWORD no en .env")

    for attempt in range(max_retries):
        try:
            logger.info(f"Intento {attempt + 1}/{max_retries} de envío Gmail desde {sender_email}")
            
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = f"Nuevo contacto: {contact.name}"
            body = f"""
            Nombre: {contact.name}
            Email: {contact.email}
            Mensaje: {contact.message}
            Enviado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            msg.attach(MIMEText(body, 'plain'))
            
            # Conexión con timeout alto y reintentos
            server = smtplib.SMTP('smtp.gmail.com', 587, timeout=120)  # ✅ Timeout 120s
            server.set_debuglevel(1)  # Logs detallados (quita en prod)
            server.starttls(timeout=120)
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            
            logger.info(f"✅ Email Gmail enviado para {contact.email}")
            return {"message": "Mensaje enviado exitosamente"}
        
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"❌ Auth fallida (intento {attempt + 1}): {e}")
            raise HTTPException(status_code=401, detail="Error de credenciales: Verifica App Password y 2FA")
        
        except smtplib.SMTPConnectError as e:
            logger.error(f"❌ Conexión fallida (intento {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Backoff: 1s, 2s, 4s
                continue
            raise HTTPException(status_code=500, detail="Error de conexión: Verifica red/firewall (puerto 587)")
        
        except smtplib.SMTPSenderRefused as e:
            logger.error(f"❌ Envío rechazado (intento {attempt + 1}): {e}")
            raise HTTPException(status_code=500, detail="Email rechazado por Gmail: Verifica remitente")
        
        except Exception as e:
            logger.error(f"❌ Error general (intento {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise HTTPException(status_code=500, detail="Timeout en envío: Prueba VPN o red diferente")
    
    raise HTTPException(status_code=500, detail="Falló después de reintentos: Verifica config Gmail")