from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from APPS.Sorteo.models import ParticipanteSorteo
from APPS.Sorteo.API.SerializerSorteo import SerializerSorteo


class SorteoViewSet(viewsets.ModelViewSet):
    queryset = ParticipanteSorteo.objects.all().order_by('-fecha_registro')
    serializer_class = SerializerSorteo

    # ── LISTAR (solo activos - Estado=True) ────────────────────
    @action(detail=False, methods=['get'], url_path='listar')
    def listar(self, request):
        participantes = ParticipanteSorteo.objects.filter(Estado=True).order_by('-fecha_registro')
        serializer = self.get_serializer(participantes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ── LISTAR TODOS (admin - activos e inactivos) ─────────────
    @action(detail=False, methods=['get'], url_path='listar-todos')
    def listar_todos(self, request):
        participantes = ParticipanteSorteo.objects.all().order_by('-fecha_registro')
        serializer = self.get_serializer(participantes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ── CREAR ──────────────────────────────────────────────────
    @action(detail=False, methods=['post'], url_path='crear')
    def crear(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            participante = serializer.save()
            return Response({
                'message': f'Gracias por participar, {participante.nombres}! Te contactaremos si ganas.',
                'data': self.get_serializer(participante).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ── ACTUALIZAR ─────────────────────────────────────────────
    @action(detail=False, methods=['put'], url_path='actualizar')
    def actualizar(self, request):
        id_participante = request.data.get('id')
        if not id_participante:
            return Response({'message': 'El campo id es obligatorio.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            participante = ParticipanteSorteo.objects.get(pk=id_participante)
            serializer = self.get_serializer(participante, data=request.data, partial=True)
            if serializer.is_valid():
                participante = serializer.save()
                return Response({
                    'message': f'Participante "{participante.nombres} {participante.apellidos}" actualizado exitosamente.',
                    'data': self.get_serializer(participante).data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ParticipanteSorteo.DoesNotExist:
            return Response({'message': 'Participante no encontrado.'},
                            status=status.HTTP_404_NOT_FOUND)

    # ── ANULAR (soft-delete) ───────────────────────────────────
    @action(detail=False, methods=['post'], url_path='anular')
    def anular(self, request):
        id_participante = request.data.get('id')
        if not id_participante:
            return Response({'message': 'El campo id es obligatorio.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            participante = ParticipanteSorteo.objects.get(pk=id_participante)
            participante.Estado = False
            participante.save()
            return Response({
                'message': f'Participante "{participante.nombres} {participante.apellidos}" anulado exitosamente.'
            }, status=status.HTTP_200_OK)
        except ParticipanteSorteo.DoesNotExist:
            return Response({'message': 'Participante no encontrado.'},
                            status=status.HTTP_404_NOT_FOUND)

    # ── RESTAURAR ──────────────────────────────────────────────
    @action(detail=False, methods=['post'], url_path='restaurar')
    def restaurar(self, request):
        id_participante = request.data.get('id')
        if not id_participante:
            return Response({'message': 'El campo id es obligatorio.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            participante = ParticipanteSorteo.objects.get(pk=id_participante)
            participante.Estado = True
            participante.save()
            return Response({
                'message': f'Participante "{participante.nombres} {participante.apellidos}" restaurado exitosamente.'
            }, status=status.HTTP_200_OK)
        except ParticipanteSorteo.DoesNotExist:
            return Response({'message': 'Participante no encontrado.'},
                            status=status.HTTP_404_NOT_FOUND)
