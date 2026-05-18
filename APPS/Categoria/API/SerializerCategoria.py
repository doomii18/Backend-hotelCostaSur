from rest_framework import serializers
from APPS.Categoria.models import Categoria


class SerializerCategoria(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'
