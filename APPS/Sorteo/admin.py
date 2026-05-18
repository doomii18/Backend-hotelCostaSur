from django.contrib import admin
from APPS.Sorteo.models import ParticipanteSorteo


@admin.register(ParticipanteSorteo)
class ParticipanteSorteoAdmin(admin.ModelAdmin):
    list_display = ('id_participante', 'nombres', 'apellidos', 'email', 'departamento', 'ocupacion', 'fecha_registro')
    list_filter = ('departamento', 'sexo')
    search_fields = ('nombres', 'apellidos', 'email', 'telefono')
