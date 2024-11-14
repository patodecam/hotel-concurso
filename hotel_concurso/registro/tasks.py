import random
from celery import shared_task
from registro.models import Usuario
from .email_sender import enviar_correo

@shared_task(bind=True)
def send_verification_email_task(self,email, asunto, contenido):
    enviar_correo(email, asunto, contenido)
    #print("Correo enviado correctamente")
    return "Task Finished"

@shared_task(bind=True)
def select_winner():
    users = Usuario.objects.filter(is_active=True, is_staff=False)  # Usuarios activos no admin
    if not users.exists():
        return "No hay usuarios participantes"
    #Seleccion del ganador
    winner = random.choice(users)
    #Preparacion de la notificacion por correo
    email=winner.email
    asunto="Ganador concurso de viaje"
    contenido = (f"Hola {winner.first_name},\n\n"
                 "Has sido seleccionado como ganador del sorteo de viajes de la agencia turística.\n"
                 "¡Felicidades!\nPronto nos comunicaremos contigo para coordinar los detalles del premio.")
    
    enviar_correo(email, asunto, contenido)

    # Retornar datos del ganador
    return {
        "id": winner.id,
        "username": winner.username,
        "first_name": winner.first_name,
        "last_name": winner.last_name,
        "email": winner.email,
        "direccion": winner.direccion  
    }



    

