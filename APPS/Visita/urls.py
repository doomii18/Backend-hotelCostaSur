from django.urls import path
from .views import VisitaAPIView

urlpatterns = [
    path('', VisitaAPIView.as_view(), name='visitas'),
]
