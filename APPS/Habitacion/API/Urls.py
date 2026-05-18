from django.urls import path, include
from rest_framework.routers import DefaultRouter
from APPS.Habitacion.API.HabitacionAPI import HabitacionViewSet

router = DefaultRouter()
router.register(r'', HabitacionViewSet, basename='habitacion')

urlpatterns = [
    path('', include(router.urls)),
]
