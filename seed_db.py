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
        (4, 'Suite Premium'),
        (5, 'Habitación Familiar'),
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
    habitaciones_data = [
        # Económicas (Categoría 1)
        (101, 1, 101, 45.00, "1 Cama Individual, Baño Privado, Wi-Fi Gratis, Ventilador"),
        (102, 1, 102, 45.00, "1 Cama Individual, Baño Privado, Wi-Fi Gratis, Ventilador"),
        (103, 1, 103, 60.00, "2 Camas Individuales, Baño Privado, Wi-Fi Gratis, Ventilador"),
        (104, 1, 104, 60.00, "2 Camas Individuales, Baño Privado, Wi-Fi Gratis, Ventilador"),
        (105, 1, 105, 75.00, "3 Camas Individuales, Baño Privado, Wi-Fi Gratis, Ventilador"),

        # Estándar (Categoría 2)
        (201, 2, 201, 70.00, "1 Cama Queen, Baño Privado, Wi-Fi Gratis, Televisor LED 32\", Ventilador"),
        (202, 2, 202, 70.00, "1 Cama Queen, Baño Privado, Wi-Fi Gratis, Televisor LED 32\", Ventilador"),
        (203, 2, 203, 85.00, "2 Camas Matrimoniales, Baño Privado, Wi-Fi Gratis, Televisor LED 32\", Ventilador"),
        (204, 2, 204, 85.00, "2 Camas Matrimoniales, Baño Privado, Wi-Fi Gratis, Televisor LED 32\", Ventilador"),
        (205, 2, 205, 95.00, "3 Camas Individuales, Baño Privado, Wi-Fi Gratis, Televisor LED 32\", Ventilador"),

        # Suite Ejecutiva (Categoría 3)
        (301, 3, 301, 120.00, "1 Cama King Size, Baño de Lujo con Jacuzzi, Wi-Fi de Alta Velocidad, Televisor Smart 43\", Aire Acondicionado Split, Frigobar, Escritorio de Trabajo"),
        (302, 3, 302, 120.00, "1 Cama King Size, Baño de Lujo con Jacuzzi, Wi-Fi de Alta Velocidad, Televisor Smart 43\", Aire Acondicionado Split, Frigobar, Escritorio de Trabajo"),
        (303, 3, 303, 120.00, "1 Cama King Size, Baño de Lujo con Jacuzzi, Wi-Fi de Alta Velocidad, Televisor Smart 43\", Aire Acondicionado Split, Frigobar, Escritorio de Trabajo"),
        (304, 3, 304, 150.00, "2 Camas Queen Size, Baño de Lujo con Jacuzzi, Wi-Fi de Alta Velocidad, Televisor Smart 43\", Aire Acondicionado Split, Frigobar, Escritorio de Trabajo"),
        (305, 3, 305, 150.00, "2 Camas Queen Size, Baño de Lujo con Jacuzzi, Wi-Fi de Alta Velocidad, Televisor Smart 43\", Aire Acondicionado Split, Frigobar, Escritorio de Trabajo"),

        # Suite Premium (Categoría 4)
        (401, 4, 401, 180.00, "1 Cama California King Size, Baño de Mármol con Jacuzzi y Ducha Española, Terraza Privada con Vista al Mar, Wi-Fi de Alta Velocidad, Smart TV 55\", Aire Acondicionado Central, Frigobar Premium, Cafetera Nespresso, Batas y Zapatillas de Baño"),
        (402, 4, 402, 180.00, "1 Cama California King Size, Baño de Mármol con Jacuzzi y Ducha Española, Terraza Privada con Vista al Mar, Wi-Fi de Alta Velocidad, Smart TV 55\", Aire Acondicionado Central, Frigobar Premium, Cafetera Nespresso, Batas y Zapatillas de Baño"),
        (403, 4, 403, 180.00, "1 Cama California King Size, Baño de Mármol con Jacuzzi y Ducha Española, Terraza Privada con Vista al Mar, Wi-Fi de Alta Velocidad, Smart TV 55\", Aire Acondicionado Central, Frigobar Premium, Cafetera Nespresso, Batas y Zapatillas de Baño"),
        (404, 4, 404, 250.00, "1 Cama California King Size, Sala de Estar Independiente, Cocina Equipada, Baño con Jacuzzi Doble, Terraza Panorámica con Piscina Privada, Wi-Fi de Alta Velocidad, Smart TV 65\", Aire Acondicionado, Servicio a la Habitación 24/7"),
        (405, 4, 405, 250.00, "1 Cama California King Size, Sala de Estar Independiente, Cocina Equipada, Baño con Jacuzzi Doble, Terraza Panorámica con Piscina Privada, Wi-Fi de Alta Velocidad, Smart TV 65\", Aire Acondicionado, Servicio a la Habitación 24/7"),

        # Familiar (Categoría 5)
        (501, 5, 501, 110.00, "1 Cama Matrimonial y 2 Camas Individuales, Baño Amplio Familiar, Área de Juegos Infantil, Wi-Fi Gratis, Televisor LED 40\", Aire Acondicionado Split, Microondas y Frigobar"),
        (502, 5, 502, 110.00, "1 Cama Matrimonial y 2 Camas Individuales, Baño Amplio Familiar, Área de Juegos Infantil, Wi-Fi Gratis, Televisor LED 40\", Aire Acondicionado Split, Microondas y Frigobar"),
        (503, 5, 503, 110.00, "1 Cama Matrimonial y 2 Camas Individuales, Baño Amplio Familiar, Área de Juegos Infantil, Wi-Fi Gratis, Televisor LED 40\", Aire Acondicionado Split, Microondas y Frigobar"),
        (504, 5, 504, 140.00, "2 Camas Matrimoniales y 2 Camas Individuales (Habitaciones Conectadas), 2 Baños Completos, Sala de Estar Pequeña, Wi-Fi de Alta Velocidad, 2 Smart TV 40\", Aire Acondicionado, Cocina Pequeña"),
        (505, 5, 505, 140.00, "2 Camas Matrimoniales y 2 Camas Individuales (Habitaciones Conectadas), 2 Baños Completos, Sala de Estar Pequeña, Wi-Fi de Alta Velocidad, 2 Smart TV 40\", Aire Acondicionado, Cocina Pequeña")
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

    print("¡Base de datos sembrada con éxito! 🎉")

if __name__ == '__main__':
    seed()
