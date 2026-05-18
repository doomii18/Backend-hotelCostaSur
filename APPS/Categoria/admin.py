from django.contrib import admin
from APPS.Categoria.models import Categoria


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id_categoria', 'NombreCategoria')
    search_fields = ('NombreCategoria',)
