from rest_framework import serializers
from APPS.Sorteo.models import ParticipanteSorteo


class SerializerSorteo(serializers.ModelSerializer):
    class Meta:
        model = ParticipanteSorteo
        fields = '__all__'
