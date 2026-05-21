import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Config.settings')
django.setup()

from APPS.Categoria.models import Categoria
from APPS.Habitacion.models import Habitacion
from Seguridad.models import Usuario

def seed():
    print("Iniciando la siembra de la base de datos (Seeding)...")

    # 1. Crear Categorías exactas para el frontend
    categorias_data = [
        (1, 'estandar'),
        (2, 'familiares'),
        (3, 'aire'),
    ]

    for id_cat, nombre in categorias_data:
        obj, created = Categoria.objects.update_or_create(
            id_categoria=id_cat,
            defaults={'NombreCategoria': nombre}
        )
        if created:
            print(f"Categoría creada: {nombre}")

    # 2. Crear Usuarios por defecto (Admin y Huésped de prueba)
    admin_hash = "7f8bc5fb7c514742a0c4f828a2a4b85c18b76fb083b4b88d4078ad691ccbf568"
    admin_user, created = Usuario.objects.update_or_create(
        usuario="HCS-ADMINISTRADOR",
        defaults={
            "correo": "admin@hotelcostasur.com",
            "contrasena": admin_hash,
            "rol": "admin"
        }
    )

    huesped_hash = "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5"
    huesped_user, created = Usuario.objects.update_or_create(
        usuario="huesped1",
        defaults={
            "correo": "huesped@gmail.com",
            "contrasena": huesped_hash,
            "rol": "user"
        }
    )

    # 3. Crear Habitaciones exactas según el requerimiento del usuario
    # Datos: [id_hab, id_cat, numero, precio, tipo, caracteristicas, disponible, televisor, aire]
    habitaciones_data = [
        (1, 1, 1, 500, "Dos camas", ["2 camas", "Matrimonial e Individual", "Baño privado"], True, False, False),
        (2, 1, 2, 500, "Dos camas", ["2 camas", "Matrimonial e Individual", "Baño privado"], True, False, False),
        (3, 1, 3, 400, "Matrimonial", ["Cama matrimonial", "Baño privado"], True, False, False),
        (4, 1, 4, 500, "Dos camas", ["2 camas Individuales", "Baño privado"], True, False, False),
        (5, 1, 5, 400, "Matrimonial", ["Cama matrimonial", "Baño privado"], True, False, False),
        (6, 1, 6, 400, "Matrimonial", ["Cama matrimonial", "Baño privado"], True, False, False),
        (7, 2, 7, 550, "Dos camas con TV", ["2 camas Individuales", "Baño privado", "Televisor"], True, True, False),
        (8, 2, 8, 550, "Dos camas con TV", ["2 camas Individuales", "Baño privado", "Televisor"], True, True, False),
        (9, 1, 9, 450, "Matrimonial con TV", ["Cama matrimonial", "Baño privado", "Televisor"], True, True, False),
        (10, 1, 10, 450, "Matrimonial con TV", ["Cama matrimonial", "Baño privado", "Televisor"], True, True, False),
        (11, 1, 11, 450, "Matrimonial con TV", ["Cama matrimonial", "Baño privado", "Televisor"], True, True, False),
        (12, 1, 12, 450, "Matrimonial con TV", ["Cama matrimonial", "Baño privado", "Televisor"], True, True, False),
        (13, 1, 13, 450, "Matrimonial con TV", ["Cama matrimonial", "Baño privado", "Televisor"], True, True, False),
        (14, 1, 14, 450, "Matrimonial con TV", ["Cama matrimonial", "Baño privado", "Televisor"], True, True, False),
        (15, 1, 15, 400, "Matrimonial", ["Cama matrimonial", "Baño privado"], True, False, False),
        (16, 1, 16, 500, "Doble cama sin TV", ["2 camas Individuales", "Baño privado"], True, False, False),
        (17, 1, 17, 400, "Matrimonial", ["Cama matrimonial", "Baño privado"], True, False, False),
        (18, 1, 18, 400, "Matrimonial", ["Cama matrimonial", "Baño privado"], True, False, False),
        (19, 2, 19, 700, "Dos camas matrimoniales", ["2 camas matrimoniales", "Baño privado"], True, False, False),
        (20, 2, 20, 900, "Cuatro camas", ["4 camas individuales", "Baño privado"], True, False, False),
        (21, 2, 21, 700, "Triple cama", ["3 camas individuales", "Baño privado"], True, False, False),
        (22, 2, 22, 550, "Doble cama con TV", ["2 camas Individuales", "Baño privado", "Televisor"], True, True, False),
        (23, 3, 23, 1100, "Cama Matrimonial", ["Cama Queen", "Baño privado", "Aire Acondicionado"], True, True, True),
        (24, 3, 24, 1100, "Cama Matrimonial", ["Cama Queen", "Baño privado", "Aire Acondicionado"], False, True, True),
        (25, 3, 25, 1100, "Cama Matrimonial", ["Cama Queen", "Baño privado", "Aire Acondicionado"], True, True, True)
    ]

    for id_hab, id_cat, numero, precio, tipo, carac, disponible, tv, aire in habitaciones_data:
        cat = Categoria.objects.get(id_categoria=id_cat)
        
        # Guardamos la metadata extra en la descripción como JSON para evitar modificar el modelo
        metadata = {
            "tipo": tipo,
            "caracteristicas": carac,
            "televisor": tv,
            "aire": aire
        }
        
        obj, created = Habitacion.objects.update_or_create(
            id=id_hab,
            defaults={
                'id_categoria': cat,
                'Numero_Habitacion': numero,
                'precio': precio,
                'Descripcion': json.dumps(metadata, ensure_ascii=False),
                'Estado': disponible
            }
        )
        if created:
            print(f"Habitación {numero} creada.")
        else:
            print(f"Habitación {numero} actualizada.")

    print("¡Base de datos sembrada con éxito!")

if __name__ == '__main__':
    seed()
