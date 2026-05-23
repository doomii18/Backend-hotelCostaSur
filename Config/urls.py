from django.contrib import admin
from django.urls import path, include
from Seguridad.Usuarios.API.UsuarioAPI import UsuarioViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/registro', UsuarioViewSet.as_view({'post': 'register_user'})),
    path('api/usuarios/login', UsuarioViewSet.as_view({'post': 'login_user'})),
    path('api/usuarios/', include('Seguridad.Usuarios.API.Urls')),
    path('api/categorias/', include('APPS.Categoria.API.Urls')),
    path('api/habitaciones/', include('APPS.Habitacion.API.Urls')),
    path('api/reservas/', include('APPS.Reserva.API.Urls')),
    path('api/sorteos/', include('APPS.Sorteo.API.Urls')),
]
