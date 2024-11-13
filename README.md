# Sorteo Masivo 

Este proyecto es una **aplicación web full-stack** diseñada para gestionar sorteos masivos, permitiendo a los usuarios inscribirse y participar de manera fácil y segura. El objetivo principal es realizar sorteos automáticos y notificar a los ganadores, ofreciendo una experiencia eficiente tanto para los organizadores como para los participantes.

## Características Principales

- **Registro de Usuarios**: Los participantes pueden registrarse proporcionando información personal básica como nombre, correo electrónico y contraseña.
- **Inscripción en Sorteos**: Los usuarios pueden inscribirse en diferentes sorteos con un solo clic.
- **Selección Aleatoria del Ganador**: Utilizando una tarea asíncrona con Celery y Redis, se selecciona un ganador al azar entre todos los inscritos.
- **Notificación por Correo Electrónico**: El ganador recibe automáticamente un correo con los detalles del premio.
- **Interfaz Administrativa**: Permite a los administradores gestionar sorteos, supervisar la participación y verificar ganadores.
- **Frontend Interactivo**: Una interfaz de usuario moderna y responsiva desarrollada con Vue.js/Nuxt para facilitar la inscripción y la visualización de resultados.

## Tecnologías Utilizadas

- **Backend**: Django, Django Rest Framework (DRF), Celery, Redis
- **Frontend**: Vue.js/Nuxt.js
- **Base de Datos**: PostgreSQL
- **Autenticación**: Tokens JWT para asegurar la comunicación entre cliente y servidor.
- **Gestión de Tareas Asíncronas**: Celery para tareas de largo plazo, como la selección del ganador y envío de correos.
- **Notificaciones por Correo**: Integración con un servidor SMTP para enviar notificaciones automáticas.

