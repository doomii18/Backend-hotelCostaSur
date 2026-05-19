#!/usr/bin/env python
"""
Script para limpiar y recargar toda la base de datos (para desarrollo/testing)
ADVERTENCIA: Elimina TODOS los datos. Solo usar en desarrollo.
"""
import os
import sys
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Config.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

def confirm_action(message):
    """Pide confirmación del usuario antes de ejecutar acciones destructivas"""
    response = input(f"\n⚠️  {message}\n¿Está seguro? (escriba 'sí' para confirmar): ").strip().lower()
    return response == 'sí'

def reset_database():
    """Reinicia completamente la base de datos"""
    print("\n" + "="*60)
    print("🔄 REINICIO COMPLETO DE BASE DE DATOS")
    print("="*60)

    if not confirm_action("Esto eliminará TODOS los datos y recreará las tablas."):
        print("❌ Operación cancelada")
        return False

    try:
        # 1. Eliminar todas las tablas
        print("\n🗑️  Eliminando todas las tablas...")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT tablename FROM pg_tables
                WHERE schemaname = 'public'
            """)
            tables = cursor.fetchall()

            for table in tables:
                table_name = table[0]
                cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
                print(f"   ✓ Tabla '{table_name}' eliminada")

        # 2. Ejecutar migraciones
        print("\n📊 Aplicando migraciones...")
        call_command('migrate', verbosity=2)

        # 3. Cargar datos iniciales
        print("\n🌱 Sembrando base de datos con datos iniciales...")
        from APPS.Categoria.models import Categoria
        from APPS.Habitacion.models import Habitacion
        from Seguridad.models import Usuario

        # Categorías
        categorias = [
            (1, 'Habitación Económica'),
            (2, 'Habitación Estándar'),
            (3, 'Suite Ejecutiva'),
        ]
        for id_cat, nombre in categorias:
            Categoria.objects.create(id_categoria=id_cat, NombreCategoria=nombre)
            print(f"   ✓ Categoría creada: {nombre}")

        # Usuario Admin
        admin = Usuario(
            usuario="HCS-ADMINISTRADOR",
            correo="admin@hotelcostasur.com",
            rol="admin"
        )
        admin.set_password("2026HOTELCOSTASUR")
        admin.save()
        print(f"   ✓ Usuario administrador creado")

        # Usuario Huésped
        huesped = Usuario(
            usuario="huesped1",
            correo="huesped@gmail.com",
            rol="user"
        )
        huesped.set_password("12345")
        huesped.save()
        print(f"   ✓ Usuario huésped creado")

        # Habitaciones
        habitaciones_data = [
            (1, 1, 1, 500, "2 camas, Matrimonial e Individual, Baño privado"),
            (2, 1, 2, 500, "2 camas, Matrimonial e Individual, Baño privado"),
            (3, 1, 3, 400, "Cama matrimonial, Baño privado"),
            (4, 1, 4, 500, "2 camas Individuales, Baño privado"),
            (5, 1, 5, 400, "Cama matrimonial, Baño privado"),
            (6, 1, 6, 400, "Cama matrimonial, Baño privado"),
            (7, 2, 7, 550, "2 camas Individuales, Baño privado, Televisor"),
            (8, 2, 8, 550, "2 camas Individuales, Baño privado, Televisor"),
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
            (19, 2, 19, 700, "2 camas matrimoniales, Baño privado"),
            (20, 2, 20, 900, "4 camas individuales, Baño privado"),
            (21, 2, 21, 700, "3 camas individuales, Baño privado"),
            (22, 2, 22, 550, "2 camas Individuales, Baño privado, Televisor"),
            (23, 3, 23, 1100, "Cama Queen, Baño privado, Aire Acondicionado, Televisor"),
            (24, 3, 24, 1100, "Cama Queen, Baño privado, Aire Acondicionado, Televisor"),
            (25, 3, 25, 1100, "Cama Queen, Baño privado, Aire Acondicionado, Televisor"),
        ]

        for id_hab, id_cat, numero, precio, desc in habitaciones_data:
            cat = Categoria.objects.get(id_categoria=id_cat)
            Habitacion.objects.create(
                id=id_hab,
                id_categoria=cat,
                Numero_Habitacion=numero,
                precio=precio,
                Descripcion=desc,
                Estado=True
            )

        print(f"   ✓ 25 habitaciones creadas")

        print("\n✅ Base de datos reiniciada exitosamente!")
        return True

    except Exception as e:
        print(f"\n❌ Error durante reinicio: {str(e)}")
        return False

def show_summary():
    """Muestra un resumen de la base de datos actual"""
    print("\n" + "="*60)
    print("📊 RESUMEN DE BASE DE DATOS")
    print("="*60)

    try:
        from APPS.Categoria.models import Categoria
        from APPS.Habitacion.models import Habitacion
        from Seguridad.models import Usuario

        categorias = Categoria.objects.all().count()
        habitaciones = Habitacion.objects.all().count()
        usuarios = Usuario.objects.all().count()

        print(f"\n📋 Categorías: {categorias}")
        print(f"🛏️  Habitaciones: {habitaciones}")
        print(f"👤 Usuarios: {usuarios}")

        if habitaciones > 0:
            print("\n🏨 Habitaciones por categoría:")
            for cat in Categoria.objects.all():
                count = cat.habitaciones.count()
                precio_promedio = sum(h.precio for h in cat.habitaciones.all()) / count if count > 0 else 0
                print(f"   {cat.NombreCategoria}: {count} habitaciones (${precio_promedio:.2f} promedio)")

    except Exception as e:
        print(f"\n❌ Error al obtener resumen: {str(e)}")

if __name__ == '__main__':
    try:
        print("\n🔧 HERRAMIENTA DE RESET DE BASE DE DATOS - HOTEL COSTA SUR")
        print("⚠️  SOLO USAR EN DESARROLLO - ELIMINARÁ TODOS LOS DATOS\n")

        if reset_database():
            show_summary()
            print("\n" + "="*60)
            print("✅ Puedes iniciar el servidor con: python manage.py runserver")
            print("="*60 + "\n")
        else:
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error general: {str(e)}")
        sys.exit(1)
