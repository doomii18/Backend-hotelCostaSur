import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Config.settings')
django.setup()

from APPS.Categoria.models import Categoria
from APPS.Habitacion.models import Habitacion
from Seguridad.models import Usuario

def seed():
    print("Iniciando la siembra de la base de datos (Seeding)...")

    # 1. Crear Categorías
    categorias_data = [
        (1, 'Habitación Económica'),
        (2, 'Habitación Estándar'),
        (3, 'Suite Ejecutiva'),
    ]

    for id_cat, nombre in categorias_data:
        obj, created = Categoria.objects.update_or_create(
            id_categoria=id_cat,
            defaults={'NombreCategoria': nombre}
        )
        if created:
            print(f"Categoría creada: {nombre}")

    # 2. Crear Usuarios por defecto (Admin y Huésped de prueba)
    # Contraseña admin: 2026HOTELCOSTASUR
    admin_hash = "7f8bc5fb7c514742a0c4f828a2a4b85c18b76fb083b4b88d4078ad691ccbf568"
    admin_user, created = Usuario.objects.update_or_create(
        usuario="HCS-ADMINISTRADOR",
        defaults={
            "correo": "admin@hotelcostasur.com",
            "contrasena": admin_hash,
            "rol": "admin"
        }
    )
    if created:
        print("Usuario administrador creado.")

    # Contraseña huésped: 12345
    huesped_hash = "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5"
    huesped_user, created = Usuario.objects.update_or_create(
        usuario="huesped1",
        defaults={
            "correo": "huesped@gmail.com",
            "contrasena": huesped_hash,
            "rol": "user"
        }
    )
    if created:
        print("Usuario huésped de prueba creado.")

    # 3. Crear Habitaciones (las 25 habitaciones del hotel)
    # Datos exactos del script SQL Server proporcionado
    habitaciones_data = [
        # Categoría 1: Habitación Económica
        (1, 1, 1, 500, "2 camas, Matrimonial e Individual, Baño privado"),
        (2, 1, 2, 500, "2 camas, Matrimonial e Individual, Baño privado"),
        (3, 1, 3, 400, "Cama matrimonial, Baño privado"),
        (4, 1, 4, 500, "2 camas Individuales, Baño privado"),
        (5, 1, 5, 400, "Cama matrimonial, Baño privado"),
        (6, 1, 6, 400, "Cama matrimonial, Baño privado"),
        (9, 1, 9, 450, "Cama matrimonial, Baño privado, Televisor"),
        (10, 1, 10, 450, "Cama matrimonial, Baño privado, Televisor"),
        (11, 1, 11, 450, "Cama matrimonial, Baño privado, Televisor"),
        (12, 1, 12, 450, "Cama matrimonial, Baño privado, Televisor"),
        (13, 1, 13, 450, "Cama matrimonial, Baño privado, Televisor"),
        (14, 1, 14, 450, "Cama matrimonial, Baño privado, Televisor"),
        (15, 1, 15, 400, "Cama matrimonial, Baño privado"),
        (16, 1, 16, 500, "2 camas Individuales, Baño privado"),
        (17, 1, 17, 400, "Cama matrimonial, Baño privado"),
        (18, 1, 18, 400, "Cama matrimonial, Baño privado"),

        # Categoría 2: Habitación Estándar
        (7, 2, 7, 550, "2 camas Individuales, Baño privado, Televisor"),
        (8, 2, 8, 550, "2 camas Individuales, Baño privado, Televisor"),
        (19, 2, 19, 700, "2 camas matrimoniales, Baño privado"),
        (20, 2, 20, 900, "4 camas individuales, Baño privado"),
        (21, 2, 21, 700, "3 camas individuales, Baño privado"),
        (22, 2, 22, 550, "2 camas Individuales, Baño privado, Televisor"),

        # Categoría 3: Suite Ejecutiva
        (23, 3, 23, 1100, "Cama Queen, Baño privado, Aire Acondicionado, Televisor"),
        (24, 3, 24, 1100, "Cama Queen, Baño privado, Aire Acondicionado, Televisor"),
        (25, 3, 25, 1100, "Cama Queen, Baño privado, Aire Acondicionado, Televisor"),
    ]

    for id_hab, id_cat, numero, precio, desc in habitaciones_data:
        cat = Categoria.objects.get(id_categoria=id_cat)
        obj, created = Habitacion.objects.update_or_create(
            id=id_hab,
            defaults={
                'id_categoria': cat,
                'Numero_Habitacion': numero,
                'precio': precio,
                'Descripcion': desc,
                'Estado': True
            }
        )
        if created:
            print(f"Habitación {numero} creada.")

    print("Base de datos sembrada con exito!")

if __name__ == '__main__':
    seed()
