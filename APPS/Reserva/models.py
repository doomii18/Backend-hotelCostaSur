from django.db import models
from Seguridad.models import Cliente
from APPS.Habitacion.models import Habitacion


class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        db_column='id_cliente',
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
    CantidadHuespedes = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50, default='presencial')
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    Estado = models.BooleanField(default=True)  # Soft-delete: True=activa, False=anulada

    class Meta:
        db_table = 'reservas'
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f"Reserva {self.id_reserva} - Cliente: {self.id_cliente}"

