from django.db import models
from Seguridad.models import Usuario
from APPS.Habitacion.models import Habitacion


class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        related_name='reservas'
    )
    id_habitacion = models.ForeignKey(
        Habitacion,
        on_delete=models.CASCADE,
        db_column='id_habitacion',
        related_name='reservas'
    )
    estado = models.CharField(max_length=20, default='pendiente')
    fecha_ingreso = models.DateField()
    fecha_salida = models.DateField()
    dias = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    tipo_documento = models.CharField(max_length=20)
    cedula = models.CharField(max_length=20, null=True, blank=True)
    pais_pasaporte = models.CharField(max_length=50, null=True, blank=True)
    pasaporte = models.CharField(max_length=50, null=True, blank=True)
    sexo = models.CharField(max_length=10)
    fecha_nacimiento = models.DateField()
    nacionalidad = models.CharField(max_length=50)
    procedencia = models.CharField(max_length=100)
    num_huespedes = models.IntegerField()
    metodo_pago = models.CharField(max_length=50)
    fecha_reserva = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reservas'
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f"Reserva {self.id_reserva} - {self.nombres} {self.apellidos}"
