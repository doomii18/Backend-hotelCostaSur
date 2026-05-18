from rest_framework import viewsets, status
from rest_framework.response import Response
from APPS.Sorteo.models import ParticipanteSorteo
from APPS.Sorteo.API.SerializerSorteo import SerializerSorteo


class SorteoViewSet(viewsets.ModelViewSet):
    queryset = ParticipanteSorteo.objects.all().order_by('-fecha_registro')
    serializer_class = SerializerSorteo

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            participante = serializer.save()
            return Response({
                'message': f'¡Gracias por participar, {participante.nombres}! 🎉 Te contactaremos si ganas.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
