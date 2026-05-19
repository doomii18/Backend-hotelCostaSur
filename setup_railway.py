#!/usr/bin/env python
"""
Script para verificar y setear PostgreSQL en Railway
Ejecuta: python setup_railway.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Config.settings')
django.setup()

from django.conf import settings
from django.core.management import call_command
from django.db import connection
import psycopg2

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def check_database_config():
    """Verifica la configuración de la BD"""
    print_section("1. CONFIGURACIÓN DE BASE DE DATOS")

    db_config = settings.DATABASES['default']
    database_url = os.getenv('DATABASE_URL', 'No configurada')

    print(f"DATABASE_URL: {database_url[:50]}...")
    print(f"\nConfiguración:")
    print(f"  ENGINE: {db_config.get('ENGINE')}")
    print(f"  NAME: {db_config.get('NAME')}")
    print(f"  USER: {db_config.get('USER')}")
    print(f"  HOST: {db_config.get('HOST')}")
    print(f"  PORT: {db_config.get('PORT')}")

    return db_config

def test_connection():
    """Prueba la conexión a PostgreSQL"""
    print_section("2. PROBANDO CONEXIÓN")

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
        print(f"✅ Conexión exitosa!")
        print(f"PostgreSQL: {version[0]}\n")
        return True
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}\n")
        return False

def check_tables():
    """Verifica las tablas existentes"""
    print_section("3. ESTADO DE TABLAS")

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()

        if tables:
            print(f"✅ Tablas encontradas: {len(tables)}")
            for table in tables:
                print(f"   📋 {table[0]}")
            return len(tables) > 0
        else:
            print("⚠️  No hay tablas. Necesitas ejecutar migraciones.\n")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
        return False

def run_migrations():
    """Ejecuta las migraciones"""
    print_section("4. EJECUTANDO MIGRACIONES")

    try:
        print("Aplicando migraciones...")
        call_command('migrate', verbosity=2)
        print("\n✅ Migraciones completadas!")
        return True
    except Exception as e:
        print(f"❌ Error en migraciones: {str(e)}\n")
        return False

def seed_data():
    """Carga los datos iniciales"""
    print_section("5. SEMBRANDO DATOS INICIALES")

    try:
        from APPS.Categoria.models import Categoria
        from APPS.Habitacion.models import Habitacion
        from Seguridad.models import Usuario

        # Categorías
        print("Creando categorías...")
        categorias = [
            (1, 'Habitación Económica'),
            (2, 'Habitación Estándar'),
            (3, 'Suite Ejecutiva'),
        ]

        for id_cat, nombre in categorias:
            obj, created = Categoria.objects.get_or_create(
                id_categoria=id_cat,
                defaults={'NombreCategoria': nombre}
            )
            if created:
                print(f"   ✓ {nombre}")

        # Habitaciones
        print("\nCreando habitaciones (25)...")
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
            obj, created = Habitacion.objects.get_or_create(
                id=id_hab,
                defaults={
                    'id_categoria': cat,
                    'Numero_Habitacion': numero,
                    'precio': precio,
                    'Descripcion': desc,
                    'Estado': True
                }
            )

        print(f"   ✓ 25 habitaciones")
        print("\n✅ Datos cargados exitosamente!")
        return True
    except Exception as e:
        print(f"❌ Error al cargar datos: {str(e)}\n")
        return False

def verify_data():
    """Verifica que los datos estén completos"""
    print_section("6. VERIFICACIÓN DE DATOS")

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM habitaciones;")
            count = cursor.fetchone()[0]

            print(f"Total de habitaciones: {count}")

            if count == 25:
                print("✅ Todas las 25 habitaciones están presentes!")

                cursor.execute("""
                    SELECT id_categoria, COUNT(*) as cantidad
                    FROM habitaciones
                    GROUP BY id_categoria
                    ORDER BY id_categoria;
                """)

                categories = cursor.fetchall()
                print("\nDistribución por categoría:")
                for cat_id, cat_count in categories:
                    print(f"   Categoría {cat_id}: {cat_count} habitaciones")

                return True
            else:
                print(f"⚠️  Se encontraron {count} habitaciones (esperadas 25)")
                return False
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
        return False

def show_summary(results):
    """Muestra un resumen final"""
    print_section("RESUMEN FINAL")

    tests = [
        ("Conexión", results.get('connection', False)),
        ("Tablas", results.get('tables', False)),
        ("Migraciones", results.get('migrations', False)),
        ("Datos cargados", results.get('data', False)),
        ("Verificación", results.get('verification', False)),
    ]

    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")

    if all(results.values()):
        print("\n✅ BASE DE DATOS LISTA EN RAILWAY!")
        print("\nPuedes iniciar el servidor con:")
        print("   python manage.py runserver")
    else:
        print("\n⚠️  Hay algunos problemas. Revisa los detalles arriba.")

def main():
    print("\n🚀 SETUP POSTGRESQL EN RAILWAY")
    print("=" * 60)

    results = {}

    # Verificar config
    check_database_config()

    # Probar conexión
    results['connection'] = test_connection()
    if not results['connection']:
        print("❌ No se puede conectar. Verifica DATABASE_URL en .env")
        sys.exit(1)

    # Verificar tablas
    results['tables'] = check_tables()

    # Si no hay tablas, ejecutar migraciones
    if not results['tables']:
        response = input("\n¿Ejecutar migraciones? (s/n): ").lower()
        if response == 's':
            results['migrations'] = run_migrations()
        else:
            results['migrations'] = False
    else:
        results['migrations'] = True

    # Sembrear datos
    response = input("\n¿Cargar datos iniciales? (s/n): ").lower()
    if response == 's':
        results['data'] = seed_data()
    else:
        results['data'] = False

    # Verificar datos
    results['verification'] = verify_data()

    # Mostrar resumen
    show_summary(results)

    print("\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error general: {str(e)}")
        sys.exit(1)
