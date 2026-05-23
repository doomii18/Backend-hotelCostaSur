from django.urls import path, include
from rest_framework.routers import DefaultRouter
from APPS.Reserva.API.ReservaAPI import ReservaViewSet

router = DefaultRouter()
router.register(r'', ReservaViewSet, basename='reserva')

urlpatterns = [
    path('', include(router.urls)),
]
