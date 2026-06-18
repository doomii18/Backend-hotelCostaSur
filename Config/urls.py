from django.contrib import admin
from django.urls import path, include
from Seguridad.Usuarios.API.UsuarioAPI import UsuarioViewSet
from APPS.Reserva.API.ReservaAPI import ReservaViewSet
from APPS.Habitacion.API.HabitacionAPI import HabitacionViewSet
from APPS.Sorteo.API.SorteoAPI import SorteoViewSet

from django.http import JsonResponse

def test_deploy_status(request):
    return JsonResponse({'status': 'running latest code', 'version': 'dcf7b75_updated'})

urlpatterns = [
    path('api/test-deploy-status/', test_deploy_status),
    path('admin/', admin.site.urls),
    path('api/usuarios/registro/', UsuarioViewSet.as_view({'post': 'register_user'})),
    path('api/usuarios/login/', UsuarioViewSet.as_view({'post': 'login_user'})),
    path('api/usuarios/', UsuarioViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/reservas/', ReservaViewSet.as_view({'get': 'list', 'post': 'crear'})),
    path('api/reservas/mis-reservas/', ReservaViewSet.as_view({'get': 'mis_reservas'})),
    path('api/reservas/fechas-no-disponibles/<int:habitacion_id>/', ReservaViewSet.as_view({'get': 'fechas_no_disponibles'})),
    path('api/habitaciones/', HabitacionViewSet.as_view({'get': 'list'})),
    path('api/sorteos/', SorteoViewSet.as_view({'post': 'crear'})),
    
    path('api/usuarios/', include('Seguridad.Usuarios.API.Urls')),
    path('api/categorias/', include('APPS.Categoria.API.Urls')),
    path('api/habitaciones/', include('APPS.Habitacion.API.Urls')),
    path('api/reservas/', include('APPS.Reserva.API.Urls')),
    path('api/sorteos/', include('APPS.Sorteo.API.Urls')),
    path('api/visitas/', include('APPS.Visita.urls')),
]
