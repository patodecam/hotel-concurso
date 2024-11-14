#Importaciones
from django.shortcuts import render
from .models import Usuario
from .serializers import ListaUsuarios,RegistroPreliminar,FinalizarRegistro
from rest_framework import generics, status,permissions
#from .tasks import fun
#from django.http import HttpResponse
from .tasks import send_verification_email_task,select_winner
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework.views import APIView
from django.utils.encoding import force_str
from rest_framework.permissions import IsAuthenticated, IsAdminUser

#Vista User List sin login
class ListaUsuariosView(generics.ListAPIView):
    queryset = Usuario.objects.all() 
    serializer_class = ListaUsuarios 


#Vista registro preliminar
class RegistroPreliminarView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegistroPreliminar

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            try:
                user, verification_link = serializer.save()  

                
                asunto = "Verificación de Correo"
                mensaje = f"Gracias por registrarte. Por favor, verifica tu correo usando el siguiente enlace: {verification_link}"  
                send_verification_email_task.delay(user.email, asunto,mensaje)

                return Response({
                    "message": "Registro exitoso. Por favor, revisa tu correo electrónico para verificar tu cuenta."
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                print(f"Error al enviar correo: {str(e)}")
                return Response({
                    "message": "Registro exitoso, pero ocurrió un error al enviar el correo de verificación.",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


#Vista de verificacion de email y configuracion nueva contraseña
class VerificarEmailView(APIView):
    def post(self, request, uidb64, token):
        try:
            
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Usuario.objects.get(pk=uid)

            
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()

                
                serializer = FinalizarRegistro(data=request.data)
                if serializer.is_valid():
                    new_password = serializer.validated_data.get('password')
                    user.set_password(new_password)
                    user.save()

                    return Response({
                        'message': "Correo verificado y contraseña establecida exitosamente."
                    }, status=status.HTTP_200_OK)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Token inválido o expirado.'}, status=status.HTTP_400_BAD_REQUEST)

        except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
            return Response({'error': 'El enlace de verificación es inválido.'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Usuario.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()

                new_password = request.data.get('password')

                if new_password:
                    user.set_password(new_password)
                    user.save()

                    return Response({
                        'message': "Correo verificado y contraseña establecida exitosamente."
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'La nueva contraseña es requerida.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Token inválido o expirado.'}, status=status.HTTP_400_BAD_REQUEST)

        except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
            return Response({'error': 'El enlace de verificación es inválido.'}, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request, uidb64, token):
        try:
            
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Usuario.objects.get(pk=uid)

            
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()

                
                serializer = FinalizarRegistro(data=request.data)
                if serializer.is_valid():
                    new_password = serializer.validated_data.get('password')
                    user.set_password(new_password)
                    user.save()

                    return Response({
                        'message': "Correo verificado y contraseña establecida exitosamente."
                    }, status=status.HTTP_200_OK)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Token inválido o expirado.'}, status=status.HTTP_400_BAD_REQUEST)

        except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
            return Response({'error': 'El enlace de verificación es inválido.'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Usuario.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()

                new_password = request.data.get('password')

                if new_password:
                    user.set_password(new_password)
                    user.save()

                    return Response({
                        'message': "Correo verificado y contraseña establecida exitosamente."
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'La nueva contraseña es requerida.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Token inválido o expirado.'}, status=status.HTTP_400_BAD_REQUEST)

        except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
            return Response({'error': 'El enlace de verificación es inválido.'}, status=status.HTTP_400_BAD_REQUEST)


#Vista lista de usuarios con login
class UserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]  # Solo el admin puede acceder

    def get(self, request):
        users = Usuario.objects.filter(is_staff=False, is_active=True) 
        serializer = ListaUsuarios(users, many=True)
        return Response(serializer.data)
    