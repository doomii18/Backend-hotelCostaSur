from django.db import models
from APPS.Categoria.models import Categoria


class Habitacion(models.Model):
    id_habitacion = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    id_categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        db_column='id_categoria',
        related_name='habitaciones'
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    caracteristicas = models.TextField()  # Serialized JSON array in the database
    disponible = models.BooleanField(default=True)
    televisor = models.BooleanField(default=False)
    aire = models.BooleanField(default=False)

    class Meta:
        db_table = 'habitaciones'
        verbose_name = 'Habitación'
        verbose_name_plural = 'Habitaciones'

    def __str__(self):
        return f"{self.nombre} - {self.tipo}"
