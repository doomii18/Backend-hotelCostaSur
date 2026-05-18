from django.contrib import admin
from APPS.Reserva.models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id_reserva', 'nombres', 'apellidos', 'fecha_ingreso', 'fecha_salida', 'estado', 'total')
    list_filter = ('estado', 'fecha_ingreso', 'fecha_salida')
    search_fields = ('nombres', 'apellidos', 'cedula', 'pasaporte')
