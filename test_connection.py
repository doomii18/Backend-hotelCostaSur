#!/usr/bin/env python
"""
Script para verificar la conexión a PostgreSQL y el estado de la base de datos
"""
import os
import django
import psycopg2
from psycopg2.extras import RealDictCursor

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Config.settings')
django.setup()

from django.conf import settings
from django.db import connection

def test_postgres_connection():
    """Prueba la conexión a PostgreSQL directamente"""
    print("\n" + "="*60)
    print("1. PROBANDO CONEXIÓN A PostgreSQL (nivel bajo)")
    print("="*60)

    # Obtener configuración de BD
    db_config = settings.DATABASES['default']
    print(f"\n📊 Configuración de BD:")
    print(f"   ENGINE: {db_config.get('ENGINE')}")
    print(f"   NAME: {db_config.get('NAME')}")
    print(f"   USER: {db_config.get('USER')}")
    print(f"   HOST: {db_config.get('HOST')}")
    print(f"   PORT: {db_config.get('PORT')}")

    try:
        conn = psycopg2.connect(
            database=db_config['NAME'],
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            host=db_config['HOST'],
            port=db_config['PORT']
        )
        cursor = conn.cursor()
        print("\n✅ Conexión a PostgreSQL: EXITOSA")

        # Probar query simple
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"\n🗄️  Versión PostgreSQL: {version[0]}\n")

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"\n❌ Error en conexión: {str(e)}")
        return False

def test_django_connection():
    """Prueba la conexión a través de Django ORM"""
    print("\n" + "="*60)
    print("2. PROBANDO CONEXIÓN A TRAVÉS DE DJANGO ORM")
    print("="*60)

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("\n✅ Conexión Django ORM: EXITOSA")
        return True
    except Exception as e:
        print(f"\n❌ Error en Django ORM: {str(e)}")
        return False

def check_tables():
    """Verifica las tablas existentes en la BD"""
    print("\n" + "="*60)
    print("3. TABLAS EN LA BASE DE DATOS")
    print("="*60)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()

            if not tables:
                print("\n⚠️  No se encontraron tablas. Ejecutar: python manage.py migrate")
            else:
                print(f"\n✅ Tablas encontradas ({len(tables)}):")
                for table in tables:
                    print(f"   📋 {table[0]}")
        return True
    except Exception as e:
        print(f"\n❌ Error al consultar tablas: {str(e)}")
        return False

def check_habitaciones_data():
    """Verifica los datos de habitaciones"""
    print("\n" + "="*60)
    print("4. DATOS DE HABITACIONES")
    print("="*60)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM habitaciones;
            """)
            count = cursor.fetchone()[0]
            print(f"\n📊 Total de habitaciones: {count}")

            if count > 0:
                cursor.execute("""
                    SELECT h.id, h.Numero_Habitacion, c.NombreCategoria, h.precio, h.Descripcion, h.Estado
                    FROM habitaciones h
                    LEFT JOIN "Categorias" c ON h.id_categoria = c.id_categoria
                    ORDER BY h.id
                    LIMIT 5;
                """)
                habitaciones = cursor.fetchall()
                print("\n✅ Primeras 5 habitaciones:")
                for hab in habitaciones:
                    print(f"   ID: {hab[0]}, Nro: {hab[1]}, Categoría: {hab[2]}, Precio: ${hab[3]}, Estado: {'✅' if hab[5] else '❌'}")
                print(f"   ... y {max(0, count - 5)} más")
        return True
    except Exception as e:
        print(f"\n⚠️  No hay datos de habitaciones o error: {str(e)}")
        return False

def check_categorias():
    """Verifica las categorías"""
    print("\n" + "="*60)
    print("5. CATEGORÍAS DE HABITACIONES")
    print("="*60)

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM \"Categorias\" ORDER BY id_categoria;")
            categorias = cursor.fetchall()

            if not categorias:
                print("\n⚠️  No hay categorías. Necesitas ejecutar seed_db.py")
            else:
                print(f"\n✅ Categorías encontradas ({len(categorias)}):")
                for cat in categorias:
                    print(f"   ID: {cat[0]}, Nombre: {cat[1]}")
        return True
    except Exception as e:
        print(f"\n❌ Error al consultar categorías: {str(e)}")
        return False

def main():
    print("\n" + "🔍 VERIFICADOR DE CONEXIÓN - HOTEL COSTA SUR".center(60, "="))

    results = {
        'PostgreSQL': test_postgres_connection(),
        'Django ORM': test_django_connection(),
        'Tablas': check_tables(),
        'Categorías': check_categorias(),
        'Habitaciones': check_habitaciones_data(),
    }

    print("\n" + "="*60)
    print("📋 RESUMEN DE VERIFICACIÓN")
    print("="*60)

    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test}: {status}")

    print("\n" + "="*60)
    print("PRÓXIMOS PASOS:")
    print("="*60)
    print("1. Si todo está ✅: Tu BD está lista")
    print("2. Si ❌ Tablas: Ejecuta: python manage.py migrate")
    print("3. Si ❌ Categorías/Habitaciones: Ejecuta: python seed_db.py")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
