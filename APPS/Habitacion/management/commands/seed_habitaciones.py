from django.core.management.base import BaseCommand
from APPS.Habitacion.models import Habitacion
from APPS.Categoria.models import Categoria

class Command(BaseCommand):
    help = 'Seeds exactly 25 rooms into the database, deleting any others.'

    def handle(self, *args, **kwargs):
        # 1. Asegurar que las categorías existan con los nombres exactos requeridos
        cat1, _ = Categoria.objects.get_or_create(id_categoria=1, defaults={'NombreCategoria': 'Estandar', 'Estado': True})
        cat1.NombreCategoria = 'Estandar'
        cat1.save()

        cat2, _ = Categoria.objects.get_or_create(id_categoria=2, defaults={'NombreCategoria': 'Familiar', 'Estado': True})
        cat2.NombreCategoria = 'Familiar'
        cat2.save()

        cat3, _ = Categoria.objects.get_or_create(id_categoria=3, defaults={'NombreCategoria': 'Premium', 'Estado': True})
        cat3.NombreCategoria = 'Premium'
        cat3.save()

        habitaciones_data = [
            # Cat, ID, Num, Precio, Desc
            (1, 1, 1, 500, '2 camas, Matrimonial e Individual, Baño privado'),
            (1, 2, 2, 500, '2 camas, Matrimonial e Individual, Baño privado'),
            (1, 3, 3, 400, 'Cama matrimonial, Baño privado'),
            (1, 4, 4, 500, '2 camas Individuales, Baño privado'),
            (1, 5, 5, 400, 'Cama matrimonial, Baño privado'),
            (1, 6, 6, 400, 'Cama matrimonial, Baño privado'),
            (1, 9, 9, 450, 'Cama matrimonial, Baño privado, Televisor'),
            (1, 10, 10, 450, 'Cama matrimonial, Baño privado, Televisor'),
            (1, 11, 11, 450, 'Cama matrimonial, Baño privado, Televisor'),
            (1, 12, 12, 450, 'Cama matrimonial, Baño privado, Televisor'),
            (1, 13, 13, 450, 'Cama matrimonial, Baño privado, Televisor'),
            (1, 14, 14, 450, 'Cama matrimonial, Baño privado, Televisor'),
            (1, 15, 15, 400, 'Cama matrimonial, Baño privado'),
            (1, 16, 16, 500, '2 camas Individuales, Baño privado'),
            (1, 17, 17, 400, 'Cama matrimonial, Baño privado'),
            (1, 18, 18, 400, 'Cama matrimonial, Baño privado'),
            (2, 7, 7, 550, '2 camas Individuales, Baño privado, Televisor'),
            (2, 8, 8, 550, '2 camas Individuales, Baño privado, Televisor'),
            (2, 19, 19, 700, '2 camas matrimoniales, Baño privado'),
            (2, 20, 20, 900, '4 camas individuales, Baño privado'),
            (2, 21, 21, 700, '3 camas individuales, Baño privado'),
            (2, 22, 22, 550, '2 camas Individuales, Baño privado, Televisor'),
            (3, 23, 23, 1100, 'Cama Queen, Baño privado, Aire Acondicionado, Televisor'),
            (3, 24, 24, 1100, 'Cama Queen, Baño privado, Aire Acondicionado, Televisor'),
            (3, 25, 25, 1100, 'Cama Queen, Baño privado, Aire Acondicionado, Televisor'),
        ]

        valid_ids = []
        for cat_id, hab_id, num, precio, desc in habitaciones_data:
            valid_ids.append(hab_id)
            Habitacion.objects.update_or_create(
                id=hab_id,
                defaults={
                    'id_categoria_id': cat_id,
                    'Numero_Habitacion': num,
                    'precio': precio,
                    'Descripcion': desc,
                    'Estado': True,
                    'Activo': True
                }
            )

        # 2. Eliminar cualquier habitación que no esté en esta lista exacta
        extra_rooms = Habitacion.objects.exclude(id__in=valid_ids)
        deleted_count = extra_rooms.count()
        if deleted_count > 0:
            extra_rooms.delete()

        self.stdout.write(self.style.SUCCESS(f'Exito: 25 habitaciones insertadas/actualizadas. {deleted_count} habitaciones antiguas eliminadas.'))
