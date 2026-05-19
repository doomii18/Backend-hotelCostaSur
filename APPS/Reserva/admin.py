from django.contrib import admin
from APPS.Reserva.models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id_reserva', 'id_cliente', 'fecha_ingreso', 'fecha_salida', 'estado', 'total')
    list_filter = ('estado', 'fecha_ingreso', 'fecha_salida')
    search_fields = ('id_cliente__nombres', 'id_cliente__apellidos', 'id_cliente__cedula', 'id_cliente__pasaporte')

