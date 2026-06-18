from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Visita
from django.db.models import Sum

# Base de visitas previas del mes (datos históricos antes de implementar el contador)
VISITAS_MES_BASE = 1567

class VisitaAPIView(APIView):
    def get(self, request):
        today = timezone.now().date()
        current_month = today.month
        current_year = today.year
        
        visita_hoy, created = Visita.objects.get_or_create(fecha=today)
        
        visitas_mes = Visita.objects.filter(
            fecha__year=current_year,
            fecha__month=current_month
        ).aggregate(total=Sum('conteo'))['total'] or 0
        
        return Response({
            'visitas_hoy': visita_hoy.conteo,
            'visitas_mes': visitas_mes + VISITAS_MES_BASE
        }, status=status.HTTP_200_OK)

    def post(self, request):
        today = timezone.now().date()
        current_month = today.month
        current_year = today.year
        
        visita_hoy, created = Visita.objects.get_or_create(fecha=today)
        visita_hoy.conteo += 1
        visita_hoy.save()
        
        visitas_mes = Visita.objects.filter(
            fecha__year=current_year,
            fecha__month=current_month
        ).aggregate(total=Sum('conteo'))['total'] or 0
        
        return Response({
            'visitas_hoy': visita_hoy.conteo,
            'visitas_mes': visitas_mes + VISITAS_MES_BASE
        }, status=status.HTTP_200_OK)
