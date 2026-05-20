from rest_framework import serializers
from APPS.Reserva.models import Reserva


class SerializerReserva(serializers.ModelSerializer):
    # Campos del Cliente relacionado
    usuarioId = serializers.ReadOnlyField(source='id_cliente.id_usuario.id_usuario')
    usuarioNombre = serializers.ReadOnlyField(source='id_cliente.id_usuario.usuario')

    nombres = serializers.ReadOnlyField(source='id_cliente.nombres')
    apellidos = serializers.ReadOnlyField(source='id_cliente.apellidos')
    tipo_documento = serializers.ReadOnlyField(source='id_cliente.tipo_documento')
    cedula = serializers.ReadOnlyField(source='id_cliente.cedula')
    pais_pasaporte = serializers.ReadOnlyField(source='id_cliente.pais_pasaporte')
    pasaporte = serializers.ReadOnlyField(source='id_cliente.pasaporte')
    sexo = serializers.ReadOnlyField(source='id_cliente.sexo')
    fecha_nacimiento = serializers.ReadOnlyField(source='id_cliente.fecha_nacimiento')
    nacionalidad = serializers.ReadOnlyField(source='id_cliente.nacionalidad')
    procedencia = serializers.ReadOnlyField(source='id_cliente.procedencia')

    # Campos de la Habitacion relacionada
    habitacionId = serializers.ReadOnlyField(source='id_habitacion.id')
    habitacionNombre = serializers.SerializerMethodField()
    habitacionTipo = serializers.SerializerMethodField()

    # Mapear campo interno a formato frontend
    num_huespedes = serializers.IntegerField(source='CantidadHuespedes')

    class Meta:
        model = Reserva
        fields = [
            'id_reserva', 'id_cliente', 'id_habitacion', 'usuarioId', 'habitacionId',
            'usuarioNombre', 'habitacionNombre', 'habitacionTipo',
            'estado', 'Estado', 'fecha_ingreso', 'fecha_salida', 'dias', 'total',
            'nombres', 'apellidos', 'tipo_documento', 'cedula', 'pais_pasaporte', 'pasaporte',
            'sexo', 'fecha_nacimiento', 'nacionalidad', 'procedencia', 'num_huespedes',
            'metodo_pago', 'fecha_reserva'
        ]

    def get_habitacionNombre(self, obj):
        return f"Habitacion {obj.id_habitacion.Numero_Habitacion}"

    def get_habitacionTipo(self, obj):
        desc = obj.id_habitacion.Descripcion.lower()
        if 'matrimonial' in desc or 'queen' in desc or 'king' in desc:
            return 'Matrimonial'
        elif 'dos camas' in desc or '2 camas' in desc or 'doble' in desc:
            return 'Dos camas'
        elif 'cuatro camas' in desc or '4 camas' in desc:
            return 'Cuatro camas'
        elif 'triple' in desc or '3 camas' in desc:
            return 'Triple cama'
        return 'Estandar'
