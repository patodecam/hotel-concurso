from django.urls import path
from .views import ListaUsuariosView,RegistroPreliminarView ,VerificarEmailView,UserListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('registro/', RegistroPreliminarView.as_view(), name='registro'),
    path('usuarios/', ListaUsuariosView.as_view(), name='lista-usuarios'),
    path('verify/<str:uidb64>/<str:token>/', VerificarEmailView.as_view(), name='verify'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListView.as_view(), name='user_list'),

    
]