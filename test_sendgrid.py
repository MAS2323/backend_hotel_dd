from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('SENDGRID_API_KEY')
print("Key cargada:", "Sí" if api_key else "No")
if api_key:
    print(f"Key preview (primeros 10 chars): {api_key[:10]}...")

sg = SendGridAPIClient(api_key)

message = Mail(
    from_email='masoneweernesto@gmail.com',  # Verificado
    to_emails='hotelddguineaecuatorial@gmail.com',
    subject='Test SendGrid - Fix 401',
    plain_text_content='¡Prueba exitosa desde Python! Hora: ' + os.popen('date').read().strip()
)

try:
    response = sg.send(message)
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    if response.body:
        print(f"Body: {response.body.decode('utf-8')}")
    if response.status_code == 202:
        print("✅ ¡Email enviado! Revisa inbox.")
    else:
        print("❌ Error: Verifica key/permisos/sender.")
except Exception as e:
    print(f"Error detallado: {type(e).__name__}: {str(e)}")