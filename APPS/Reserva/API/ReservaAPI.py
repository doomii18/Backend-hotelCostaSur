from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db import transaction
from django.db.models import Max
from APPS.Reserva.models import Reserva
from APPS.Habitacion.models import Habitacion
from Seguridad.Usuarios.models import Usuario, Cliente
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
        
        # 1. Check if user is authenticated
        if not usuario_id and request.user and request.user.is_authenticated:
            usuario_id = request.user.id
            
        habitacion_id = request.data.get('habitacionId')
        if not habitacion_id:
            return Response({'message': 'Campo obligatorio faltante: habitacionId.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                room = Habitacion.objects.get(pk=habitacion_id)

                user = None
                
                # 2. Try to get user by ID if provided
                if usuario_id:
                    try:
                        user = Usuario.objects.get(pk=usuario_id)
                    except Usuario.DoesNotExist:
                        return Response({'message': 'Usuario no encontrado. Debe registrarse primero.'}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({'message': 'Debe iniciar sesion y registrarse para reservar.'}, status=status.HTTP_401_UNAUTHORIZED)
                
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
                else:
                    # Update client info with latest data
                    cliente.tipo_documento = request.data.get('tipoDocumento', cliente.tipo_documento)
                    cliente.cedula = request.data.get('cedula', cliente.cedula)
                    cliente.pais_pasaporte = request.data.get('paisPasaporte', cliente.pais_pasaporte)
                    cliente.pasaporte = request.data.get('pasaporte', cliente.pasaporte)
                    cliente.nombres = request.data.get('nombres', cliente.nombres)
                    cliente.apellidos = request.data.get('apellidos', cliente.apellidos)
                    cliente.sexo = request.data.get('sexo', cliente.sexo)
                    cliente.fecha_nacimiento = request.data.get('fechaNacimiento', cliente.fecha_nacimiento)
                    cliente.nacionalidad = request.data.get('nacionalidad', cliente.nacionalidad)
                    cliente.procedencia = request.data.get('procedencia', cliente.procedencia)
                    cliente.save()

                reserva = Reserva(
                    id_cliente=cliente,
                    id_habitacion=room,
                    fecha_ingreso=request.data.get('fechaIngreso'),
                    fecha_salida=request.data.get('fechaSalida'),
                    CantidadHuespedes=int(request.data.get('numHuespedes', request.data.get('huespedes', 1))),
                    metodo_pago=request.data.get('metodoPago'),
                    dias=int(request.data.get('dias', 1)),
                    total=float(request.data.get('total', 0.0)),
                    estado='pendiente',
                    Estado=True
                )

                reserva.save()

                return Response({
                    'message': f'Reserva de la habitacion {room.Numero_Habitacion} registrada con exito!',
                    'id_reserva': reserva.id_reserva
                }, status=status.HTTP_201_CREATED)

        except Habitacion.DoesNotExist:
            return Response({'message': 'La habitacion seleccionada no existe.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'Error al registrar reserva: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            if 'fechaIngreso' in request.data:
                reserva.fecha_ingreso = request.data['fechaIngreso']
            if 'fechaSalida' in request.data:
                reserva.fecha_salida = request.data['fechaSalida']
            if 'dias' in request.data:
                reserva.dias = int(request.data['dias'])
            if 'total' in request.data:
                reserva.total = float(request.data['total'])
            if 'numHuespedes' in request.data:
                reserva.CantidadHuespedes = int(request.data['numHuespedes'])
            if 'huespedes' in request.data:
                reserva.CantidadHuespedes = int(request.data['huespedes'])
            if 'metodo_pago' in request.data:
                reserva.metodo_pago = request.data['metodo_pago']
            if 'metodoPago' in request.data:
                reserva.metodo_pago = request.data['metodoPago']
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

    # ── SOFT-DELETE (destroy override) ─────────────────────────
    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                reserva = self.get_object()
                reserva.Estado = True
                reserva.estado = 'cancelado'
                reserva.save()

                # Liberar la habitacion
                room = reserva.id_habitacion
                room.Estado = True
                room.save()

                return Response({
                    'message': f'Reserva #{reserva.id_reserva} cancelada. Habitacion {room.Numero_Habitacion} liberada.'
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Error: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                reserva.Estado = True
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

                return Response({
                    'message': f'Reserva #{reserva.id_reserva} restaurada exitosamente.'
                }, status=status.HTTP_200_OK)
        except Reserva.DoesNotExist:
            return Response({'message': 'Reserva no encontrada.'},
                            status=status.HTTP_404_NOT_FOUND)

    # ── CHECK-IN ───────────────────────────────────────────────
    @action(detail=False, methods=['post', 'put'], url_path='checkin/(?P<reserva_id>\\d+)')
    def checkin(self, request, reserva_id=None):
        try:
            with transaction.atomic():
                reserva = Reserva.objects.get(pk=reserva_id)
                reserva.estado = 'activo'
                reserva.save()

                room = reserva.id_habitacion
                room.Estado = False
                room.save()

                return Response({
                    'message': f'Check-In registrado para la reserva #{reserva.id_reserva}.'
                }, status=status.HTTP_200_OK)
        except Reserva.DoesNotExist:
            return Response({'message': 'Reserva no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'Error al realizar Check-In: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ── CHECK-OUT ──────────────────────────────────────────────
    @action(detail=False, methods=['post', 'put'], url_path='checkout/(?P<reserva_id>\\d+)')
    def checkout(self, request, reserva_id=None):
        try:
            with transaction.atomic():
                reserva = Reserva.objects.get(pk=reserva_id)
                reserva.estado = 'completado'
                reserva.save()

                room = reserva.id_habitacion
                room.Estado = True
                room.save()

                return Response({
                    'message': f'Check-Out registrado para la reserva #{reserva.id_reserva}. Habitacion {room.Numero_Habitacion} liberada.'
                }, status=status.HTTP_200_OK)
        except Reserva.DoesNotExist:
            return Response({'message': 'Reserva no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'Error al realizar Check-Out: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ── FECHAS NO DISPONIBLES ─────────────────────────────────
    @action(detail=False, methods=['get'], url_path='fechas-no-disponibles/(?P<habitacion_id>\\d+)')
    def fechas_no_disponibles(self, request, habitacion_id=None):
        if not habitacion_id:
            return Response({'message': 'Se requiere el ID de la habitacion.'}, status=status.HTTP_400_BAD_REQUEST)
        
        exclude_id = request.query_params.get('exclude', None)
        
        # Obtener todas las reservas activas/pendientes para esta habitacion
        reservas = Reserva.objects.filter(
            id_habitacion=habitacion_id,
            Estado=True,
            estado__in=['pendiente', 'activo']
        )
        
        if exclude_id:
            reservas = reservas.exclude(id_reserva=exclude_id)
        
        fechas_ocupadas = []
        import datetime
        for r in reservas:
            if r.fecha_ingreso and r.fecha_salida:
                curr_date = r.fecha_ingreso
                while curr_date <= r.fecha_salida:
                    fechas_ocupadas.append(curr_date.strftime('%Y-%m-%d'))
                    curr_date += datetime.timedelta(days=1)
                    
        return Response({'fechas': list(set(fechas_ocupadas))}, status=status.HTTP_200_OK)
