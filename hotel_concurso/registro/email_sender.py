import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings

def enviar_correo(destinatario, asunto, contenido):
    email_emisor = settings.DEFAULT_FROM_EMAIL

    try:
        # Configuración del correo electrónico
        msg = MIMEMultipart()
        msg['From'] = email_emisor
        msg['To'] = destinatario
        msg['Subject'] = asunto

        # Adjuntar el contenido de texto
        msg.attach(MIMEText(contenido, 'plain'))  # 'plain' para texto simple

        # Configurar la conexión segura con el servidor de correo saliente (SMTP server)
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        # Enviar el correo electrónico
        server.sendmail(email_emisor, destinatario, msg.as_string())
        print("Mensaje enviado correctamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
    finally:
        server.quit()  # Terminar la conexión
