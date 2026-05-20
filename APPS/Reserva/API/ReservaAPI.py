from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Max
from APPS.Reserva.models import Reserva
from APPS.Habitacion.models import Habitacion
from Seguridad.models import Usuario, Cliente
from APPS.Reserva.API.SerializerReserva import SerializerReserva


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all().order_by('-fecha_reserva')
    serializer_class = SerializerReserva

    # ── LISTAR (solo activas - Estado=True) ────────────────────
    @action(detail=False, methods=['get'], url_path='listar')
    def listar(self, request):
        reservas = Reserva.objects.filter(Estado=True).order_by('-fecha_reserva')
        serializer = self.get_serializer(reservas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ── LISTAR TODOS (admin - activas e inactivas) ─────────────
    @action(detail=False, methods=['get'], url_path='listar-todos')
    def listar_todos(self, request):
        reservas = Reserva.objects.all().order_by('-fecha_reserva')
        serializer = self.get_serializer(reservas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ── MIS RESERVAS (por usuario autenticado) ─────────────────
    @action(detail=False, methods=['get'], url_path='mis-reservas')
    def mis_reservas(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response({'message': 'No autorizado.'}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = request.user.id
        reservas = Reserva.objects.filter(
            id_cliente__id_usuario=user_id, Estado=True
        ).order_by('-fecha_reserva')
        serializer = self.get_serializer(reservas, many=True)
        return Response(serializer.data)

    # ── CREAR ──────────────────────────────────────────────────
    @action(detail=False, methods=['post'], url_path='crear')
    def crear(self, request):
        usuario_id = request.data.get('usuarioId')
        habitacion_id = request.data.get('habitacionId')

        if not usuario_id or not habitacion_id:
            return Response({
                'message': 'Campos obligatorios faltantes: usuarioId o habitacionId.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                user = Usuario.objects.get(pk=usuario_id)
                room = Habitacion.objects.get(pk=habitacion_id)

                if not room.Estado:
                    return Response({
                        'message': f'La habitacion {room.Numero_Habitacion} ya no esta disponible.'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Buscar o crear perfil de cliente
                cliente = Cliente.objects.filter(id_usuario=user).first()
                if not cliente:
                    max_id = Cliente.objects.aggregate(Max('id'))['id__max'] or 0
                    cliente = Cliente.objects.create(
                        id=max_id + 1,
                        id_usuario=user,
                        tipo_documento=request.data.get('tipoDocumento'),
                        cedula=request.data.get('cedula'),
                        pais_pasaporte=request.data.get('paisPasaporte'),
                        pasaporte=request.data.get('pasaporte'),
                        nombres=request.data.get('nombres'),
                        apellidos=request.data.get('apellidos'),
                        sexo=request.data.get('sexo'),
                        fecha_nacimiento=request.data.get('fechaNacimiento'),
                        nacionalidad=request.data.get('nacionalidad'),
                        procedencia=request.data.get('procedencia'),
                        Estado=True
                    )

                reserva = Reserva(
                    id_cliente=cliente,
                    id_habitacion=room,
                    fecha_ingreso=request.data.get('fechaIngreso'),
                    fecha_salida=request.data.get('fechaSalida'),
                    CantidadHuespedes=int(request.data.get('numHuespedes', 1)),
                    metodo_pago=request.data.get('metodoPago'),
                    dias=int(request.data.get('dias', 1)),
                    total=float(request.data.get('total', 0.0)),
                    estado='pendiente',
                    Estado=True
                )

                # Marcar habitacion como ocupada
                room.Estado = False
                room.save()
                reserva.save()

                return Response({
                    'message': f'Reserva de la habitacion {room.Numero_Habitacion} registrada con exito!',
                    'id_reserva': reserva.id_reserva
                }, status=status.HTTP_201_CREATED)

        except Usuario.DoesNotExist:
            return Response({'message': 'El usuario ingresado no existe.'},
                            status=status.HTTP_404_NOT_FOUND)
        except Habitacion.DoesNotExist:
            return Response({'message': 'La habitacion seleccionada no existe.'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'Error al registrar reserva: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ── ACTUALIZAR ─────────────────────────────────────────────
    @action(detail=False, methods=['put'], url_path='actualizar')
    def actualizar(self, request):
        id_reserva = request.data.get('id_reserva')
        if not id_reserva:
            return Response({'message': 'El campo id_reserva es obligatorio.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            reserva = Reserva.objects.get(pk=id_reserva)
            # Campos actualizables
            if 'fecha_ingreso' in request.data:
                reserva.fecha_ingreso = request.data['fecha_ingreso']
            if 'fecha_salida' in request.data:
                reserva.fecha_salida = request.data['fecha_salida']
            if 'dias' in request.data:
                reserva.dias = int(request.data['dias'])
            if 'total' in request.data:
                reserva.total = float(request.data['total'])
            if 'numHuespedes' in request.data:
                reserva.CantidadHuespedes = int(request.data['numHuespedes'])
            if 'metodo_pago' in request.data:
                reserva.metodo_pago = request.data['metodo_pago']
            if 'estado' in request.data:
                reserva.estado = request.data['estado']
            reserva.save()
            return Response({
                'message': f'Reserva #{reserva.id_reserva} actualizada exitosamente.',
                'data': self.get_serializer(reserva).data
            }, status=status.HTTP_200_OK)
        except Reserva.DoesNotExist:
            return Response({'message': 'Reserva no encontrada.'},
                            status=status.HTTP_404_NOT_FOUND)

    # ── ANULAR (soft-delete + liberar habitacion) ──────────────
    @action(detail=False, methods=['post'], url_path='anular')
    def anular(self, request):
        id_reserva = request.data.get('id_reserva')
        if not id_reserva:
            return Response({'message': 'El campo id_reserva es obligatorio.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                reserva = Reserva.objects.get(pk=id_reserva)
                reserva.Estado = False
                reserva.estado = 'cancelado'
                reserva.save()

                # Liberar la habitacion
                room = reserva.id_habitacion
                room.Estado = True
                room.save()

                return Response({
                    'message': f'Reserva #{reserva.id_reserva} anulada. Habitacion {room.Numero_Habitacion} liberada.'
                }, status=status.HTTP_200_OK)
        except Reserva.DoesNotExist:
            return Response({'message': 'Reserva no encontrada.'},
                            status=status.HTTP_404_NOT_FOUND)

    # ── RESTAURAR ──────────────────────────────────────────────
    @action(detail=False, methods=['post'], url_path='restaurar')
    def restaurar(self, request):
        id_reserva = request.data.get('id_reserva')
        if not id_reserva:
            return Response({'message': 'El campo id_reserva es obligatorio.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                reserva = Reserva.objects.get(pk=id_reserva)
                reserva.Estado = True
                reserva.estado = 'pendiente'
                reserva.save()

                # Re-ocupar la habitacion
                room = reserva.id_habitacion
                room.Estado = False
                room.save()

                return Response({
                    'message': f'Reserva #{reserva.id_reserva} restaurada exitosamente.'
                }, status=status.HTTP_200_OK)
        except Reserva.DoesNotExist:
            return Response({'message': 'Reserva no encontrada.'},
                            status=status.HTTP_404_NOT_FOUND)

    # ── CHECK-IN ───────────────────────────────────────────────
    @action(detail=True, methods=['post'], url_path='checkin')
    def checkin(self, request, pk=None):
        try:
            with transaction.atomic():
                reserva = self.get_object()
                reserva.estado = 'activo'
                reserva.save()

                room = reserva.id_habitacion
                room.Estado = False
                room.save()

                return Response({
                    'message': f'Check-In registrado para la reserva #{reserva.id_reserva}.'
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Error al realizar Check-In: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ── CHECK-OUT ──────────────────────────────────────────────
    @action(detail=True, methods=['post'], url_path='checkout')
    def checkout(self, request, pk=None):
        try:
            with transaction.atomic():
                reserva = self.get_object()
                reserva.estado = 'completado'
                reserva.save()

                room = reserva.id_habitacion
                room.Estado = True
                room.save()

                return Response({
                    'message': f'Check-Out registrado para la reserva #{reserva.id_reserva}. Habitacion {room.Numero_Habitacion} liberada.'
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Error al realizar Check-Out: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
