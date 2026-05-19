from django.db import models


class ParticipanteSorteo(models.Model):
    id = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=20)
    departamento = models.CharField(max_length=50)
    sexo = models.CharField(max_length=20)
    edad = models.IntegerField()
    ocupacion = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'participantes_sorteo'
        verbose_name = 'Participante Sorteo'
        verbose_name_plural = 'Participantes Sorteo'

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.email})"

