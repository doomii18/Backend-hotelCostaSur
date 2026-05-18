import json
from rest_framework import serializers
from APPS.Habitacion.models import Habitacion


class SerializerHabitacion(serializers.ModelSerializer):
    caracteristicas = serializers.SerializerMethodField()

    class Meta:
        model = Habitacion
        fields = '__all__'

    def get_caracteristicas(self, obj):
        try:
            # Parse database features from JSON array string
            return json.loads(obj.caracteristicas)
        except Exception:
            # Fallback to splitting if it's not valid JSON
            if obj.caracteristicas:
                return [x.strip() for x in obj.caracteristicas.split(',') if x.strip()]
            return []
