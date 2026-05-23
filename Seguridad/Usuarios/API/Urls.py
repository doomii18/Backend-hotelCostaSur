from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Seguridad.Usuarios.API.UsuarioAPI import UsuarioViewSet

router = DefaultRouter()
router.trailing_slash = '/?'
router.register(r'', UsuarioViewSet, basename='usuario')

urlpatterns = [
    path('', include(router.urls)),
]
