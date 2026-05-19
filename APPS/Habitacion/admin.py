from django.contrib import admin
from APPS.Habitacion.models import Habitacion


@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'Numero_Habitacion', 'id_categoria', 'precio', 'Estado')
    list_filter = ('id_categoria', 'Estado')
    search_fields = ('Numero_Habitacion', 'Descripcion')

