from django.contrib import admin
from APPS.Habitacion.models import Habitacion


@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ('id_habitacion', 'nombre', 'tipo', 'precio', 'disponible', 'televisor', 'aire')
    list_filter = ('tipo', 'disponible', 'televisor', 'aire')
    search_fields = ('nombre', 'tipo')
