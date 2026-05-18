from django.contrib import admin
from Seguridad.models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'usuario', 'correo', 'rol', 'fecha_registro')
    list_filter = ('rol',)
    search_fields = ('usuario', 'correo')
