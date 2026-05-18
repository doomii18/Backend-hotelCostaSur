from rest_framework import serializers
from APPS.Reserva.models import Reserva


class SerializerReserva(serializers.ModelSerializer):
    # Dynamic readonly fields to match frontend object structure
    usuarioNombre = serializers.ReadOnlyField(source='id_usuario.usuario')
    habitacionNombre = serializers.ReadOnlyField(source='id_habitacion.nombre')
    habitacionTipo = serializers.ReadOnlyField(source='id_habitacion.tipo')
    usuarioId = serializers.IntegerField(source='id_usuario.id_usuario', read_only=True)
    habitacionId = serializers.IntegerField(source='id_habitacion.id_habitacion', read_only=True)

    class Meta:
        model = Reserva
        fields = [
            'id_reserva', 'id_usuario', 'id_habitacion', 'usuarioId', 'habitacionId',
            'usuarioNombre', 'habitacionNombre', 'habitacionTipo',
            'estado', 'fecha_ingreso', 'fecha_salida', 'dias', 'total',
            'nombres', 'apellidos', 'tipo_documento', 'cedula', 'pais_pasaporte', 'pasaporte',
            'sexo', 'fecha_nacimiento', 'nacionalidad', 'procedencia', 'num_huespedes',
            'metodo_pago', 'fecha_reserva'
        ]
