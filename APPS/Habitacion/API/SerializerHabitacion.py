import json
from rest_framework import serializers
from APPS.Habitacion.models import Habitacion


class SerializerHabitacion(serializers.ModelSerializer):
    nombre = serializers.SerializerMethodField()
    tipo = serializers.SerializerMethodField()
    categoria = serializers.SerializerMethodField()
    disponible = serializers.SerializerMethodField()
    televisor = serializers.SerializerMethodField()
    aire = serializers.SerializerMethodField()
    caracteristicas = serializers.SerializerMethodField()
    activo = serializers.BooleanField(source='Activo', read_only=True)

    class Meta:
        model = Habitacion
        fields = ['id', 'nombre', 'tipo', 'categoria', 'precio', 'caracteristicas',
                  'disponible', 'televisor', 'aire', 'activo']

    def get_nombre(self, obj):
        return f"Habitacion {obj.Numero_Habitacion}"

    def get_categoria(self, obj):
        cat_name = obj.id_categoria.NombreCategoria.lower()
        if 'estandar' in cat_name or 'estándar' in cat_name or 'econo' in cat_name or 'econó' in cat_name:
            return 'estandar'
        elif 'famili' in cat_name:
            return 'familiares'
        elif 'aire' in cat_name or 'suite' in cat_name or 'exec' in cat_name or 'premium' in cat_name:
            return 'aire'
        return cat_name

    def get_disponible(self, obj):
        return obj.Estado

    def get_televisor(self, obj):
        desc = obj.Descripcion.lower()
        return 'tv' in desc or 'televisor' in desc or 'smart' in desc

    def get_aire(self, obj):
        desc = obj.Descripcion.lower()
        return 'aire' in desc or 'climatizado' in desc or 'a/c' in desc or obj.id_categoria_id == 3

    def get_tipo(self, obj):
        desc = obj.Descripcion.lower()
        if 'matrimonial' in desc or 'queen' in desc or 'king' in desc:
            return 'Matrimonial'
        elif 'dos camas' in desc or '2 camas' in desc or 'doble' in desc:
            return 'Dos camas'
        elif 'cuatro camas' in desc or '4 camas' in desc:
            return 'Cuatro camas'
        elif 'triple' in desc or '3 camas' in desc:
            return 'Triple cama'
        return 'Estandar'

    def get_caracteristicas(self, obj):
        try:
            return json.loads(obj.Descripcion)
        except Exception:
            if obj.Descripcion:
                return [x.strip() for x in obj.Descripcion.split(',') if x.strip()]
            return []
