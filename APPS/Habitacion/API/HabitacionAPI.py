from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from APPS.Habitacion.models import Habitacion
from APPS.Habitacion.API.SerializerHabitacion import SerializerHabitacion


class HabitacionViewSet(viewsets.ModelViewSet):
    queryset = Habitacion.objects.all().order_by('id')
    serializer_class = SerializerHabitacion

    # ── LISTAR (solo activas - Activo=True) ────────────────────
    @action(detail=False, methods=['get'], url_path='listar')
    def listar(self, request):
        habitaciones = Habitacion.objects.filter(Activo=True).order_by('id')
        serializer = self.get_serializer(habitaciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ── LISTAR TODOS (admin - activas e inactivas) ─────────────
    @action(detail=False, methods=['get'], url_path='listar-todos')
    def listar_todos(self, request):
        habitaciones = Habitacion.objects.all().order_by('id')
        serializer = self.get_serializer(habitaciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ── CREAR ──────────────────────────────────────────────────
    @action(detail=False, methods=['post'], url_path='crear')
    def crear(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            habitacion = serializer.save()
            return Response({
                'message': f'Habitacion {habitacion.Numero_Habitacion} creada exitosamente.',
                'data': self.get_serializer(habitacion).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ── ACTUALIZAR ─────────────────────────────────────────────
    @action(detail=False, methods=['put'], url_path='actualizar')
    def actualizar(self, request):
        id_habitacion = request.data.get('id')
        if not id_habitacion:
            return Response({'message': 'El campo id es obligatorio.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            habitacion = Habitacion.objects.get(pk=id_habitacion)
            serializer = self.get_serializer(habitacion, data=request.data, partial=True)
            if serializer.is_valid():
                habitacion = serializer.save()
                return Response({
                    'message': f'Habitacion {habitacion.Numero_Habitacion} actualizada exitosamente.',
                    'data': self.get_serializer(habitacion).data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Habitacion.DoesNotExist:
            return Response({'message': 'Habitacion no encontrada.'},
                            status=status.HTTP_404_NOT_FOUND)

    # ── ANULAR (soft-delete: Activo=False) ─────────────────────
    @action(detail=False, methods=['post'], url_path='anular')
    def anular(self, request):
        id_habitacion = request.data.get('id')
        if not id_habitacion:
            return Response({'message': 'El campo id es obligatorio.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            habitacion = Habitacion.objects.get(pk=id_habitacion)
            habitacion.Activo = False
            habitacion.save()
            return Response({
                'message': f'Habitacion {habitacion.Numero_Habitacion} anulada exitosamente.'
            }, status=status.HTTP_200_OK)
        except Habitacion.DoesNotExist:
            return Response({'message': 'Habitacion no encontrada.'},
                            status=status.HTTP_404_NOT_FOUND)

    # ── RESTAURAR ──────────────────────────────────────────────
    @action(detail=False, methods=['post'], url_path='restaurar')
    def restaurar(self, request):
        id_habitacion = request.data.get('id')
        if not id_habitacion:
            return Response({'message': 'El campo id es obligatorio.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            habitacion = Habitacion.objects.get(pk=id_habitacion)
            habitacion.Activo = True
            habitacion.save()
            return Response({
                'message': f'Habitacion {habitacion.Numero_Habitacion} restaurada exitosamente.'
            }, status=status.HTTP_200_OK)
        except Habitacion.DoesNotExist:
            return Response({'message': 'Habitacion no encontrada.'},
                            status=status.HTTP_404_NOT_FOUND)
