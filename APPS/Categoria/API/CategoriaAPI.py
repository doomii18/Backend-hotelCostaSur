from rest_framework import viewsets
from APPS.Categoria.models import Categoria
from APPS.Categoria.API.SerializerCategoria import SerializerCategoria


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = SerializerCategoria
