from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('Seguridad.API.Urls')),
    path('api/categorias/', include('APPS.Categoria.API.Urls')),
    path('api/habitaciones/', include('APPS.Habitacion.API.Urls')),
    path('api/reservas/', include('APPS.Reserva.API.Urls')),
    path('api/sorteos/', include('APPS.Sorteo.API.Urls')),
]
