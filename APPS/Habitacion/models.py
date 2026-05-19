from django.db import models
from APPS.Categoria.models import Categoria


class Habitacion(models.Model):
    id = models.IntegerField(primary_key=True)
    id_categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        db_column='id_categoria',
        related_name='habitaciones'
    )
    Numero_Habitacion = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    Descripcion = models.TextField()
    Estado = models.BooleanField(default=True)  # maps to BIT in SQL (Estado)

    class Meta:
        db_table = 'habitaciones'
        verbose_name = 'Habitación'
        verbose_name_plural = 'Habitaciones'

    def __str__(self):
        return f"Habitacion {self.Numero_Habitacion}"

