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

    def _parse_desc(self, obj):
        try:
            return json.loads(obj.Descripcion)
        except Exception:
            return {}

    def get_nombre(self, obj):
        return f"Habitación {obj.Numero_Habitacion}"

    def get_categoria(self, obj):
        # En la BD la categoría ya es 'estandar', 'familiares' o 'aire'
        return obj.id_categoria.NombreCategoria

    def get_disponible(self, obj):
        from django.utils import timezone
        from APPS.Reserva.models import Reserva
        
        today = timezone.localtime(timezone.now()).date()
        
        # Una habitación está disponible si no hay ninguna reserva activa o pendiente para hoy
        tiene_reserva_hoy = Reserva.objects.filter(
            id_habitacion=obj,
            Estado=True,  # No eliminada soft-delete
            estado__in=['pendiente', 'activo'],
            fecha_ingreso__lte=today,
            fecha_salida__gte=today
        ).exists()
        
        return not tiene_reserva_hoy

    def get_televisor(self, obj):
        return self._parse_desc(obj).get('televisor', False)

    def get_aire(self, obj):
        return self._parse_desc(obj).get('aire', False)

    def get_tipo(self, obj):
        return self._parse_desc(obj).get('tipo', 'Estandar')

    def get_caracteristicas(self, obj):
        parsed = self._parse_desc(obj)
        if 'caracteristicas' in parsed:
            return parsed['caracteristicas']
        
        # Fallback for old data
        if obj.Descripcion:
            return [x.strip() for x in obj.Descripcion.split(',') if x.strip()]
        return []
