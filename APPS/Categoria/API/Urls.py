from django.urls import path, include
from rest_framework.routers import DefaultRouter
from APPS.Categoria.API.CategoriaAPI import CategoriaViewSet

router = DefaultRouter()
router.register(r'', CategoriaViewSet, basename='categoria')

urlpatterns = [
    path('', include(router.urls)),
]
