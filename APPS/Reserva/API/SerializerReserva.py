from rest_framework import serializers
from APPS.Reserva.models import Reserva
import json


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
    habitacionNumero = serializers.ReadOnlyField(source='id_habitacion.Numero_Habitacion')
    habitacionDescripcion = serializers.SerializerMethodField()
    precioPorNoche = serializers.ReadOnlyField(source='id_habitacion.precio')

    # Mapear campo interno a formato frontend
    huespedes = serializers.IntegerField(source='CantidadHuespedes', read_only=True)

    # Alias frontend-friendly
    id = serializers.IntegerField(source='id_reserva', read_only=True)
    fechaIngreso = serializers.DateField(source='fecha_ingreso')
    fechaSalida = serializers.DateField(source='fecha_salida')

    class Meta:
        model = Reserva
        fields = [
            'id', 'id_reserva', 'id_cliente', 'id_habitacion', 'usuarioId', 'habitacionId',
            'usuarioNombre', 'habitacionNombre', 'habitacionTipo', 'habitacionNumero',
            'habitacionDescripcion', 'precioPorNoche',
            'estado', 'Estado', 'fecha_ingreso', 'fecha_salida', 'fechaIngreso', 'fechaSalida',
            'dias', 'total', 'huespedes',
            'nombres', 'apellidos', 'tipo_documento', 'cedula', 'pais_pasaporte', 'pasaporte',
            'sexo', 'fecha_nacimiento', 'nacionalidad', 'procedencia',
            'metodo_pago', 'fecha_reserva'
        ]

    def get_habitacionNombre(self, obj):
        return f"Habitacion {obj.id_habitacion.Numero_Habitacion}"

    def get_habitacionDescripcion(self, obj):
        desc = obj.id_habitacion.Descripcion
        try:
            parsed = json.loads(desc)
            return parsed.get('tipo', desc)
        except Exception:
            return desc

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
