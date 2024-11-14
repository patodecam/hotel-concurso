from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUsuarioManager(BaseUserManager):
    def create_user(self,email,username,password=None,**extra_fields):#extra_fields , permite pasar otros campos que sean necesesarios
        #Validacion de los campos
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario')
        
        # Normalizar el correo electrónico
        email = self.normalize_email(email)
        # Configurar is_active como False por defecto para usuarios normales (para la posteiror activacion de la cuenta por correo electronico)
        extra_fields.setdefault('is_active', False)

        # Crea una nueva instancia de Usuario
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Establece la contraseña
        user.save(using=self._db)     # Guarda el usuario en la base de datos
        return user

    #Crear SuperUsuario
    def create_superuser(self, email, username, password=None, **extra_fields):
        # Establece los campos necesarios para el superusuario
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # El superusuario se crea como activo

        # Verifica que el superusuario tenga los atributos necesarios
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


#Modelo personalizado de Usuario (Agregar region y comuna en menus seleccionables cargados desde la base de datos)
class Usuario(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=30,unique=True)
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    rut=models.CharField(max_length=12)
    dv = models.CharField(max_length=1)
    direccion = models.CharField(max_length=255)
    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)

    #Asisgnacion del manager perzonalizado
    objects = CustomUsuarioManager()

    #Campo para iniciar sesion en el admin
    USERNAME_FIELD = 'username'
    #Campos obligatorios para crear un SuperUsuario
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self) :
        return self.username
    
