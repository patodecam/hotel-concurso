#Importaciones
import re
from .models import Usuario
from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse

#lista de Usuarios.
class ListaUsuarios(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


#Registro Preliminar
class RegistroPreliminar(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username','first_name', 'last_name', 'email', 'rut', 'dv', 'direccion']

    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo ya está registrado.")
        return value

    def validate_first_name(self, value):
        if not re.match(r'^[a-zA-Z\s\'-]+$', value):
            raise serializers.ValidationError("El nombre solo debe contener letras, espacios y apóstrofes.")
        return value

    def validate_last_name(self, value):
        if not re.match(r'^[a-zA-Z\s\'-]+$', value):
            raise serializers.ValidationError("El apellido solo debe contener letras, espacios y apóstrofes.")
        return value

    def validar_rut(self, rut, dv):
        dv = str(dv).upper()
        digitos = list(map(int, reversed(rut)))
        factores = [2, 3, 4, 5, 6, 7]
        suma = 0
        for i, digito in enumerate(digitos):
            factor = factores[i % len(factores)]
            suma += digito * factor
        mod = 11 - (suma % 11)
        dv_esperado = 'K' if mod == 10 else '0' if mod == 11 else str(mod)
        return dv == dv_esperado

    def validate_rut(self, value):
        rut = str(value)
        dv = self.initial_data.get('dv', '').upper()  # Obtiene el DV de los datos iniciales
        if not re.match(r'^\d{1,8}$', rut) or not re.match(r'^[0-9K]$', dv):
            raise serializers.ValidationError("El RUT o el dígito verificador no son válidos.")

        if not self.validar_rut(rut, dv):
            raise serializers.ValidationError('El RUT ingresado no es válido.')
        return rut
    def validate_direccion(self, value):
        if not value:
            raise serializers.ValidationError("La dirección es obligatoria.")
        return value

    def create(self, validated_data):
        user = Usuario(**validated_data)
        user.is_active = False
        user.save()

        
        password = f"{user.id}{user.first_name}{user.last_name}{user.rut}"  
        user.set_password(password)  
        user.save(update_fields=['password'])  

       
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_link = self.context['request'].build_absolute_uri(
            reverse('verify', kwargs={'uidb64': uid, 'token': token})
        )
        verification_link = verification_link.replace('http://localhost:8000/api/verify/', 'http://localhost:8080/verify/')
        return user ,verification_link

#Finalizar el registro configuracion de la nueva contraseña
class FinalizarRegistro(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['password', 'confirm_password']

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("La contraseña debe contener al menos un carácter especial.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Las contraseñas ingresadas no coinciden."})
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])  
        instance.is_active = True  
        instance.save()
        return instance