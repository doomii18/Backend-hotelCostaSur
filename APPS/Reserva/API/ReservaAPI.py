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

    @action(detail=False, methods=['get'], url_path='mis-reservas')
    def mis_reservas(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response({'message': 'No autorizado.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # request.user.id contains the id of the authenticated user
        user_id = request.user.id
        reservas = Reserva.objects.filter(id_cliente__id_usuario=user_id).order_by('-fecha_reserva')
        serializer = self.get_serializer(reservas, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        # Extract inputs
        usuario_id = request.data.get('usuarioId')
        habitacion_id = request.data.get('habitacionId')

        if not usuario_id or not habitacion_id:
            return Response({
                'message': 'Campos obligatorios faltantes: usuarioId o habitacionId.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Transactional isolation
            with transaction.atomic():
                user = Usuario.objects.get(pk=usuario_id)
                room = Habitacion.objects.get(pk=habitacion_id)

                if not room.Estado:
                    return Response({
                        'message': f'La habitación {room.Numero_Habitacion} ya no está disponible.'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Find or create client profile
                cliente = Cliente.objects.filter(id_usuario=user).first()
                if not cliente:
                    # Generate a new unique ID since it's not an identity column
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

                # Create the transaction model mapping camelCase to T-SQL snake_case
                reserva = Reserva(
                    id_cliente=cliente,
                    id_habitacion=room,
                    fecha_ingreso=request.data.get('fechaIngreso'),
                    fecha_salida=request.data.get('fechaSalida'),
                    CantidadHuespedes=int(request.data.get('numHuespedes', 1)),
                    metodo_pago=request.data.get('metodoPago'),
                    dias=int(request.data.get('dias', 1)),
                    total=float(request.data.get('total', 0.0)),
                    estado='pendiente'
                )

                # Update room state
                room.Estado = False
                room.save()
                reserva.save()

                return Response({
                    'message': f'¡Reserva de la habitación {room.Numero_Habitacion} registrada con éxito! 🎉',
                    'id_reserva': reserva.id_reserva
                }, status=status.HTTP_201_CREATED)

        except Usuario.DoesNotExist:
            return Response({'message': 'El usuario ingresado no existe.'}, status=status.HTTP_404_NOT_FOUND)
        except Habitacion.DoesNotExist:
            return Response({'message': 'La habitación seleccionada no existe.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'Error al registrar reserva: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        """Cancel reservation and release room availability."""
        try:
            with transaction.atomic():
                reserva = self.get_object()
                room = reserva.id_habitacion
                room.Estado = True
                room.save()
                
                reserva_id = reserva.id_reserva
                reserva.delete()
                
                return Response({
                    'message': f'Reserva #{reserva_id} cancelada. Habitación {room.Numero_Habitacion} liberada.'
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Error al cancelar reserva: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='checkin')
    def checkin(self, request, pk=None):
        """Admin Action: Set check-in to active."""
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
            return Response({'message': f'Error al realizar Check-In: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='checkout')
    def checkout(self, request, pk=None):
        """Admin Action: Set check-out to completed, release room."""
        try:
            with transaction.atomic():
                reserva = self.get_object()
                reserva.estado = 'completado'
                reserva.save()

                room = reserva.id_habitacion
                room.Estado = True
                room.save()

                return Response({
                    'message': f'Check-Out registrado para la reserva #{reserva.id_reserva}. Habitación {room.Numero_Habitacion} liberada.'
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Error al realizar Check-Out: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

