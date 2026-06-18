from django.db import models

class Visita(models.Model):
    fecha = models.DateField(auto_now_add=True, unique=True, verbose_name="Fecha de visita")
    conteo = models.PositiveIntegerField(default=0, verbose_name="Número de visitas")

    class Meta:
        verbose_name = "Visita"
        verbose_name_plural = "Visitas"
        ordering = ['-fecha']

    def __str__(self):
        return f"Visitas del {self.fecha}: {self.conteo}"
