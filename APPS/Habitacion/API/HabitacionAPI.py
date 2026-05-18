from rest_framework import viewsets
from APPS.Habitacion.models import Habitacion
from APPS.Habitacion.API.SerializerHabitacion import SerializerHabitacion


class HabitacionViewSet(viewsets.ModelViewSet):
    queryset = Habitacion.objects.all().order_by('id_habitacion')
    serializer_class = SerializerHabitacion
