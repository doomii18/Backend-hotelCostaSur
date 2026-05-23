from django.urls import path, include
from rest_framework.routers import DefaultRouter
from APPS.Sorteo.API.SorteoAPI import SorteoViewSet

router = DefaultRouter()
router.register(r'', SorteoViewSet, basename='sorteo')

urlpatterns = [
    path('', include(router.urls)),
]
