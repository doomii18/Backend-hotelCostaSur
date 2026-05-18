from django.db import models


class Categoria(models.Model):
    id_categoria = models.IntegerField(primary_key=True)
    NombreCategoria = models.CharField(max_length=50)

    class Meta:
        db_table = 'Categorias'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.NombreCategoria
